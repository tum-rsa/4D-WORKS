# 4D-WORKS
Repository for the NFDI4Earth 4D-WORKS project.

Project website: [https://www.asg.ed.tum.de/en/rsa/research/4d-works/](https://www.asg.ed.tum.de/en/rsa/research/4d-works/)

## Schema

### Item

| Field Name | Type | Description  | Remark |
|------------|------|--------------|--------|
| pc4d:sensor | String | e.g., Zenmuse L2, Camera | | 
| pc4d:native_crs | String  | The CRS of stored point clouds, e.g., projected CRS | Requied |
| pc4d:datetime | datetime | Acquired datetime | Requied |
|time zone|||
| pc4d:acquisiton_mode | String | e.g., ULS, UPH, TLS |
| pc4d:orientation |  | e.g., nadir, oblique angles |
| pc4d:data_type | String | e.g., lidar, image, text | Requied |
| pc4d:point_count | Integer | Number of points|
| pc4d:avg_point_density | Number | Avg. point density with given radius |
| pc4d:spatial_resolution | Number | e.g., sampling interval |
| pc4d:measurement_error | Number | System error during measurement or sensor accuracy |
| pc4d:transformeta | Object | An object include | could be an object including all relevant meta infomation |
| pc4d:product_generated | Object | e.g., parameters used for different level of processing products |

**to add/adapt**

- duration, flight_height, flight_speed
- trajectory, scan positions, inclination 
- global transformation

#### Additional Field Information

**pc4d:transformeta**
| Field Name | Type | Description  |
|------------|------|--------------|
| reference_epoch | Link | e.g., link to other item |
| registration_error | Number | Exists if it's a co-registered point cloud |
| affine_transformation  | Matrix | A 4x4 or 3x4 matrix representing the affine transformation. Given as a numpy array. If this argument is given, the rotation and translation arguments are ignored. |
| rotation | Matrix | A 3x3 matrix specifying the rotation to apply |
| translation | Array | A vector specifying the translation to apply |
| reduction_point | Array | A translation vector to apply before applying rotation and scaling. This is used to increase the numerical accuracy of transformation. If a transformation is given, this argument is ignored. |


**pc4d:product_generated**
| Field Name | Type | Description  |
|------------|------|--------------|
| product_name | String | e.g., m3c2, DEM, etc |
| lastupdate | datetime |e.g., generated datetime|
| param | object/dict | e.g., product-related parameters |
| derived_from | Link | e.g., the data source |
| level of product | String | e.g., [processing level](https://github.com/stac-extensions/processing?tab=readme-ov-file#suggested-processing-levels) |

### Collection Summaries

- attributes list within one collection e.g., [intensity, R, G, B, cls_label]

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
    - Collection (Imagery)
- docs
  - schema
  - env (environment.yaml)
  - setup.py
  - how to run


- Item fields table
- deisgn user input as meta tabular/yaml
- implement functions property by property
- add image collection


## Ref

- https://github.com/radiantearth/stac-spec/blob/v1.1.0/best-practices.md
- https://github.com/radiantearth/stac-spec/blob/master/extensions/README.md
- https://github.com/stac-extensions/pointcloud?tab=readme-ov-file
- https://github.com/stac-extensions/mlm


## Acknowledgement
This work is funded by the German Research Foundation (DFG) through the project NFDI4Earth (4D-WORKS, DFG project no. 460036893, [https://www.nfdi4earth.de/](https://www.nfdi4earth.de/)) within the German National Research Data Infrastructure (NFDI, [https://www.nfdi.de/](https://www.nfdi.de/)). 
