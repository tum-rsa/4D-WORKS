import pdal
import json
from shapely.geometry import box, mapping
from pystac import Item, Asset
from topo4d_ext import Topo4DExtension, DataType
from datetime import datetime
from pyproj import Transformer
import laspy
import json
from pathlib import Path
import os

def make_item_asset(asset_url: str, user_input: dict):

    asset_name = user_input.get('data_type', 'data')

    asset = Asset(
        href=asset_url,
        media_type="application/vnd.laszip+copc",
        roles=["data"]
    )

    return asset_name, asset

def extract_metadata_pdal(filepath: str):

    r = pdal.Reader.copc(filepath)
    i = pdal.Filter.info()

    pipeline: pdal.Pipeline = r | i

    count = pipeline.execute()
    info = pipeline.metadata['metadata'][i.type]

    try:
        
        bbox_info = info['bbox']
        bbox =[
            bbox_info['minx'], bbox_info['miny'], bbox_info['minz'],
            bbox_info['maxx'], bbox_info['maxy'], bbox_info['maxz']         
        ]

        srs_code = None
        if (info.get('srs') and 
            info['srs'].get('json') and 
            info['srs']['json'].get('id') and 
            info['srs']['json']['id'].get('code')):
            srs_code = info['srs']['json']['id']['code']

        if srs_code and srs_code != "":
            transformer = Transformer.from_crs(f"EPSG:{srs_code}", "EPSG:4326", always_xy=True)
            
            min_lon, min_lat = transformer.transform(bbox_info['minx'], bbox_info['miny'])
            max_lon, max_lat = transformer.transform(bbox_info['maxx'], bbox_info['maxy'])

            # bbox in WGS84
            polygon = box(min_lon, min_lat, max_lon, max_lat)
            geom = mapping(polygon)
            
        else:
            polygon = box(bbox_info['minx'], bbox_info['miny'], bbox_info['maxx'], bbox_info['maxy'])
            geom = mapping(polygon)

        point_count = info['num_points']
    except KeyError as e:
        print(f"KeyError: {e}")
        srs_code = None
        bbox = [0, 0, 0, 0]  # Default bbox
        geom = mapping(box(0, 0, 0, 0))  # Default geometry
        point_count = 0

    return {
        "crs": f"EPSG:{srs_code}" if srs_code else None,
        "bbox": bbox,
        "geometry": geom,
        "point_count": point_count,
    }

def safe_serialize(value):
    """Convert any value to JSON-serializable form."""
    if isinstance(value, bytes):
        return None  # skip raw byte data
    if hasattr(value, "tolist"):
        return value.tolist()
    elif isinstance(value, (set, tuple)):
        return list(value)
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)

def header_to_dict(header):
    return {
        key: safe_serialize(getattr(header, key))
        for key in dir(header)
        if not key.startswith('_') and not callable(getattr(header, key))
    }

def serialize_vlr(vlr):
    vlr_dict = {
        "user_id": vlr.user_id,
        "record_id": vlr.record_id,
    }
    # Optionally add description if present
    if hasattr(vlr, "description"):
        vlr_dict["description"] = vlr.description

    # Extract and serialize non-bytes fields
    for key in dir(vlr):
        if key in vlr_dict or key.startswith('_'):
            continue
        value = getattr(vlr, key)
        if callable(value) or isinstance(value, bytes):
            continue
        try:
            vlr_dict[key] = safe_serialize(value)
        except Exception:
            continue  # skip unserializable fields

    return vlr_dict

def extract_metadata_from_las(filepath, if_save=False):
    """Extract metadata from a LAS/LAZ file."""
    with laspy.open(filepath, "r") as las_file:
        header = header_to_dict(las_file.header)
        vlrs = [serialize_vlr(vlr) for vlr in las_file.header.vlrs]
        evlrs = [serialize_vlr(evlr) for evlr in las_file.header.evlrs]

    metadata = {
        "id": Path(filepath).stem.split('.')[0],
        "header": header,
        "vlrs": vlrs,
        "evlrs": evlrs,
    }

    if if_save:
        metadata_path = f"{Path(filepath).parent}/{Path(filepath).stem.split('.')[0]}_header.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

    return metadata