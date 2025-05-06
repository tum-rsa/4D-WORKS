"""
stac_point_cloud.py

Toolkit for building STAC catalogs of point-cloud datasets.
"""
import os
import datetime
import laspy
import re
from shapely.geometry import mapping, Polygon
from pyproj import Transformer, CRS
from pystac import Catalog, Collection, Item, Asset, Extent, SpatialExtent, TemporalExtent, CatalogType

# -----------------------------------------
# STAC Catalog for Point Clouds
# -----------------------------------------
class PCCatalog:
    def __init__(self, id: str = None, title: str = None, description: str = None, path: str = None):
        if path:
            self.cat = Catalog.from_file(path)
        elif id and title and description:
            self.cat = Catalog(id=id, title=title, description=description)
        else:
            raise ValueError("Either 'path' or ('id', 'title', 'description') must be provided.")

    def add_collection(self, collection: Collection):
        self.cat.add_child(collection)
    
    def add_item(self, item: Item, collection_id: str = None):
        """
        Add an Item to a specific Collection by id, or to the root catalog if collection_id is None.
        """
        if collection_id:
            coll = self.cat.get_child(collection_id)
            if coll is None:
                raise KeyError(f"No collection with id '{collection_id}' found in catalog")
            coll.add_item(item)
        else:
            self.cat.add_item(item)

    def save(self, dest_path: str = "catalog.json"):
        self.cat.normalize_hrefs(os.path.dirname(dest_path) or "./")
        self.cat.save(catalog_type=CatalogType.SELF_CONTAINED)
        print(f"Catalog saved to {dest_path}")


def create_collection(id: str, title: str, description: str,
                      spatial_bounds: list[float], temporal_range: list[list[datetime.datetime]], 
                      license: str = "CC-BY-4.0"):
    extent = Extent(
        spatial=SpatialExtent([spatial_bounds]),
        temporal=TemporalExtent(temporal_range)
    )
    return Collection(
        id=id,
        title=title,
        description=description,
        extent=extent,
        license="CC-BY-4.0"
    )


def extract_bbox(laz_path: str):
    with laspy.open(laz_path) as f:
        hdr = f.header        
        # original bounds & CRS
        ox_min, oy_min = hdr.min[0], hdr.min[1]
        ox_max, oy_max = hdr.max[0], hdr.max[1]
        try:
            native_crs: CRS = hdr.parse_crs()
        except Exception:
            native_crs = CRS.from_epsg(4326)

        # transformer to WGS84
        transformer = Transformer.from_crs(native_crs, CRS.from_epsg(4326), always_xy=True)
        # transform corner coordinates
        xs = [ox_min, ox_min, ox_max, ox_max]
        ys = [oy_min, oy_max, oy_max, oy_min]
        lons, lats = transformer.transform(xs, ys)
        wgs_bbox = [min(lons), min(lats), max(lons), max(lats)]

    return wgs_bbox, native_crs.to_epsg()

def extract_datetime(laz_path: str):

    datetime_pattern = r"(\d{8})" # YYYYMMDD
    filename = os.path.basename(laz_path)
    match = re.search(datetime_pattern, filename)

    if match:
        date_str = match.group(1)
        try:
            # Convert YYYYMMDD to datetime
            year = int(date_str[0:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])
            return datetime.datetime(year, month, day)
        except (ValueError, IndexError):
            pass
    
    return None


def create_point_cloud_item(
        id: str,
        href: str,
        bbox: list[float],
        timestamp: datetime.datetime,
        props: dict = None,
    ) -> Item:

    properties = props.copy() if props else {}

    polygon = Polygon([
        (bbox[0], bbox[1]), 
        (bbox[0], bbox[3]),
        (bbox[2], bbox[3]), 
        (bbox[2], bbox[1]),
        (bbox[0], bbox[1])
    ])
    geom = mapping(polygon)

    item = Item(
        id=id,
        geometry=geom,
        bbox=bbox,
        datetime=timestamp,
        properties=properties
    )
    asset = Asset(href=href, media_type="application/vnd.laszip+copc", roles=["data"]) # media_type refer to https://github.com/radiantearth/stac-spec/blob/v1.1.0/best-practices.md#common-media-types-in-stac
    item.add_asset("point-cloud", asset)
    return item