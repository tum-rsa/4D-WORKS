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
from pystac import Catalog, Collection, Item, Asset, Extent, SpatialExtent, TemporalExtent, CatalogType, Summaries

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

    def add_collection(self, collection: Collection, summaries: Summaries = None):
        if summaries:
            collection.summaries = summaries
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
            update_collection(coll, item.datetime)
        else:
            self.cat.add_item(item)

    def save(self, dest_path: str = "catalog.json"): # the name of the catalog file cannot be changed
        self.cat.normalize_hrefs(os.path.dirname(dest_path) or "./")
        self.cat.save(catalog_type=CatalogType.SELF_CONTAINED)
        print(f"Catalog saved to {dest_path}")
        


def create_collection(id: str, 
                      title: str, 
                      description: str,
                      spatial_bounds: list[float], 
                      temporal_range: list[list[datetime.datetime]], 
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
        license=license,
        summaries=Summaries({
            "num_items": 0,
            "timestamp_list": [],           
            "temporal_resolution": " ",
        }),

    )


# to be used when the collection is already created
def update_collection(collection: Collection, new_item_timestamp: datetime.datetime):
    """
    Update the collection's summaries when a new item is added.

    Args:
        collection (Collection): The STAC collection to update.
        new_item_timestamp (datetime.datetime): The timestamp of the newly added item.
    """
    
    # Update the number of items in the collection
    if collection.summaries.get_list("num_items") is None:
        collection.summaries.add("num_items", [0])
    collection.summaries.get_list("num_items")[0] += 1

    # Update the timestamp list
    if collection.summaries.get_list("timestamp_list") is None:
        collection.summaries["timestamp_list"] = []
    collection.summaries.get_list("timestamp_list").append(new_item_timestamp.isoformat())
    collection.summaries.get_list("timestamp_list").sort()  

    # Update the temporal resolution
    # timestamp_list = collection.summaries.get_list("timestamp_list")
    # if len(timestamp_list) > 1:
    #     time_differences = [  # second as units
    #         (timestamp_list[i] - timestamp_list[i - 1]).total_seconds()
    #         for i in range(1, len(timestamp_list))
    #     ]
    #     # take the average of time differences
    #     collection.summaries.get_list("temporal_resolution") = sum(time_differences) / len(time_differences)
    # else:
    #     # if there's only one timestamp, can't calculate a resolution
    #     collection.summaries.get_list("temporal_resolution") = None



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