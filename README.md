# 4D-WORKS
Repository for the NFDI4Earth 4D-WORKS project.

Project website: [https://www.asg.ed.tum.de/en/rsa/research/4d-works/](https://www.asg.ed.tum.de/en/rsa/research/4d-works/)

## Schema



### Item

| Field Name | Type | Description  | Remark |
|------------|------|--------------|--------|
| pc4d:sensor | String | e.g., Zenmuse L2, Camera | | 
| pc4d:native_crs | String  |              | Requied |
| pc4d:datetime | datetime |              | Requied |
| pc4d:acquisiton_mode | String | e.g., ULS, UPH, TLS |
| pc4d:orientation |  ||
| pc4d:data_type | String | e.g., lidar, image, text | Requied |
| pc4d:point_count | Integer ||
| pc4d:avg_point_density | Number ||
| pc4d:spatial_resolution | Number | e.g., sampling interval |
| pc4d:measurement_error | Number ||
| pc4d:transform_matrix | Matrix (4x4) | e.g., co-registration transformation matrix |
| pc4d:reference_epoch | Link | e.g., link to other item |
| pc4d:registration_error | Number | |
| pc4d:product_generated | Object | e.g., parameters used for different level of processing products |

#### Additional Field Information

**pc4d:product_generated**
| Field Name | Type | Description  |
|------------|------|--------------|
| product_name | String | e.g., m3c2, DEM, etc |
| lastupdate | datetime ||
| param | object/dict | e.g., product-related parameters |
| derived_from | Link | e.g., the data source |


### Collection Summaries

#### by sensor
| Field Name | Type | Description  |
|------------|------|--------------|
| num_items | Integer | Number of items |
| timestamp_list | list of datetime |              |
| temporal_resolution | String | Temporal resolution of multiple acquisiton (e.g., monthly, weekly, 1hr) |



### Other extensions could be useful
- processing:level, String, https://github.com/stac-extensions/processing/tree/main?tab=readme-ov-file#suggested-processing-levels

## Todo

- stac4d
  - stac_point_cloud.py
- examples
  - create_catalog.py
  - query_catalog.py
- metadata schema
  - catelog-wise
    - collection-wise
      - item-wise
- demo ()
  - Catelog (Isar)
    - Collection (UPH)
      - 20240812
      - 20241105
      - 20250325
    - Collection (ULS)
      - 20250325
- docs
  - schema
  - env (environment.yaml)
  - setup.py
  - how to run


## Questions collection

- The datetime of each item should be the created datetime or acquired datetime?
- Naming rules of item, collection, and catalog.
- Do we want to develop new extension, or just best practice of using existing extension?
- Co-registration information as a json file? Should we store the after-registration point clouds or original ones?


## Ref

- https://github.com/radiantearth/stac-spec/blob/v1.1.0/best-practices.md
- https://github.com/radiantearth/stac-spec/blob/master/extensions/README.md
- https://github.com/stac-extensions/pointcloud?tab=readme-ov-file
- https://github.com/stac-extensions/mlm


## Acknowledgement
This work is funded by the German Research Foundation (DFG) through the project NFDI4Earth (4D-WORKS, DFG project no. 460036893, [https://www.nfdi4earth.de/](https://www.nfdi4earth.de/)) within the German National Research Data Infrastructure (NFDI, [https://www.nfdi.de/](https://www.nfdi.de/)). 
