import os

from stac4d.stac_point_cloud import (
    PCCatalog, create_collection,
    create_point_cloud_item, extract_bbox, extract_datetime
)
import datetime

# Initialize catalog
cat = PCCatalog(
    id="isar-uav",
    title="Multi-temporal UAV Point Cloud of Isar river",
    description="UAV photogrammetry and LiDAR observations of the Isar river, Germany.",
)

# Create collections for each sensor
# TBD: spatial, temporal extents need to be updated based on the data
spatial_bounds = [11.305315, 47.526668, 11.316152, 47.531578]
temporal_photo = [[datetime.datetime(2024,8,12), datetime.datetime(2024,11,5)]]
temporal_lidar = [[datetime.datetime(2025,3,25), datetime.datetime(2025,3,25)]]

photo_coll = create_collection(
    id="uav-photogrammetry",
    title="UAV Photogrammetry Point Cloud",
    description="UPH",
    spatial_bounds=spatial_bounds,
    temporal_range=temporal_photo
)
lidar_coll = create_collection(
    id="uav-lidar",
    title="UAV LiDAR Point Cloud",
    description="ULS",
    spatial_bounds=spatial_bounds,
    temporal_range=temporal_lidar
)

# Add collections to catalog
cat.add_collection(photo_coll)
cat.add_collection(lidar_coll)

# Add photogrammetry items under its collection
data_dir = "demo/data"
for fp in [os.path.join(data_dir,"Isar_20240812_UPH_10cm.copc.laz"), os.path.join(data_dir,"Isar_20241105_UPH_10cm.copc.laz")]:
    bbox, orig_crs = extract_bbox(fp)
    filename = os.path.basename(fp).split(".")[0] # TBD: naming of each item?
    ts = extract_datetime(fp) # TBD: acquired timestamp or processing timestamp?
    item = create_point_cloud_item(
        id=filename,
        href=fp,
        bbox=bbox,
        timestamp=ts, # TBD: acquired timestamp or processing timestamp?
        props={
            "sensor": "photogrammetry",
            "native_crs": f"EPSG:{orig_crs}" if isinstance(orig_crs, int) else orig_crs,
               },
    )
    cat.add_item(item, collection_id="uav-photogrammetry")


data_dir = "demo/data"
for fp in [os.path.join(data_dir,"Isar_20250325_ULS_10cm.copc.laz")]:
    bbox, orig_crs = extract_bbox(fp)
    filename = os.path.basename(fp).split(".")[0] # TBD: naming of each item?
    ts = extract_datetime(fp) # TBD: acquired timestamp or processing timestamp?
    item = create_point_cloud_item(
        id=filename,
        href=fp,
        bbox=bbox,
        timestamp=ts, # TBD: acquired timestamp or processing timestamp?
        props={
            "sensor": "uav-lidar",
            "native_crs": f"EPSG:{orig_crs}" if isinstance(orig_crs, int) else orig_crs,
               },
    )
    cat.add_item(item, collection_id="uav-lidar")


# Save catalog
cat.save("demo/Isar/catalog.json")