# 4D-WORKS
Repository for the NFDI4Earth 4D-WORKS project.

Project website: [https://www.asg.ed.tum.de/en/rsa/research/4d-works/](https://www.asg.ed.tum.de/en/rsa/research/4d-works/)

## Fields

### Collection Summaries

| Field Name          | Type    | Description                                                             |
|---------------------|---------|-------------------------------------------------------------------------|
| num_items           | Integer | Number of items                                                         |
| timestamp_list      | Array   | list of datetime                                                        |
| temporal_resolution | String  | Temporal resolution of multiple acquisiton (e.g., monthly, weekly, 1hr) |
| attribute_list      | Array   | List of attributes, e.g., [intensity, R, G, B, cls_label]               |

### Item Properties

| Field Name              | Type     | Description                                                                                                                                          |
|-------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| pc4d:sensor             | String   | e.g., Zenmuse L2, Camera                                                                                                                             |
| pc4d:native_crs         | String   | **REQUIRED.** The CRS of stored point clouds, e.g., projected CRS                                                                                    |
| pc4d:datetime           | datetime | **REQUIRED.** Acquired datetime                                                                                                                      |
| pc4d:tz                 | String   | Time zone, UTC?                                                                                                                                      |
| pc4d:acquisition_mode   | String   | e.g., ULS, UPH, TLS                                                                                                                                  |
| pc4d:duration           | Number   | unit: seconds                                                                                                                                        |
| pc4d:trajectory         | Array    | List of scan position (X, Y, Z).  **UAV only.**                                                                                                      |
| pc4d:scan_positions     | Array    | List of scan positions (X, Y, Z)                                                                                                                     |
| pc4d:orientation        | String   | e.g., nadir, oblique angles                                                                                                                          |
| pc4d:data_type          | String   | **REQUIRED.** e.g., lidar, image, text                                                                                                               |
| pc4d:point_count        | Integer  | Number of points                                                                                                                                     |
| pc4d:avg_point_density  | Number   | Avg. point density with given radius                                                                                                                 |
| pc4d:spatial_resolution | Number   | e.g., sampling interval                                                                                                                              |
| pc4d:measurement_error  | Number   | System error during measurement or sensor accuracy                                                                                                   |
| pc4d:global_transfo     | Array    | Global transformation matrix, e.g., offset                                                                                                           |
| pc4d:trafometa          | Object   | An object include, could be an object including all relevant meta infomation                                                                         |
| pc4d:product_info       | Object   | Exists if this item is a generated product. This object describe relavant meta information of the product e.g., parameters used to generate products |


### trafometa Object
| Field Name            | Type   | Description                                                                                                                                                                                    |
|-----------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| reference_epoch       | Link   | e.g., link to other item                                                                                                                                                                       |
| registration_error    | Number | Exists if it's a co-registered point cloud                                                                                                                                                     |
| affine_transformation | Array  | A 4x4 or 3x4 matrix representing the affine transformation. Given as a numpy array. If this argument is given, the rotation and translation arguments are ignored.                             |
| rotation              | Array  | A 3x3 matrix specifying the rotation to apply                                                                                                                                                  |
| translation           | Array  | A vector specifying the translation to apply                                                                                                                                                   |
| reduction_point       | Array  | A translation vector to apply before applying rotation and scaling. This is used to increase the numerical accuracy of transformation. If a transformation is given, this argument is ignored. |

### product_info Object
| Field Name    | Type        | Description                                                                                                            |
|---------------|-------------|------------------------------------------------------------------------------------------------------------------------|
| product_name  | String      | e.g., m3c2, DEM, etc                                                                                                   |
| lastupdate    | datetime    | e.g., generated datetime                                                                                               |
| param         | object/dict | e.g., product-related parameters                                                                                       |
| derived_from  | Link        | e.g., the data source                                                                                                  |
| product_level | String      | e.g., [processing level](https://github.com/stac-extensions/processing?tab=readme-ov-file#suggested-processing-levels) |




### Other extensions could be useful
- processing:level, String, https://github.com/stac-extensions/processing/tree/main?tab=readme-ov-file#suggested-processing-levels

## Todo

- stac4d
  - stac_ext.py # apis to employ stac extension
  - builder.py # user interface to create a new catalog, e.g., use csv as user input
- examples
  - create_catalog.py
  - query_catalog.py
- metadata schema
  - STAC topo4d extension https://github.com/tum-rsa/pc4d
- demo
  - Catelog (Isar)
    - Collection (UPH)
      - 20240812
      - 20241105
      - 20250325
    - Collection (ULS)
      - 20250325
    - Collection (Imagery)
- roadmap
  - introduction
  - related works
  - what we are doing
    - STAC topo4d extension, usage by https://pystac.readthedocs.io/en/latest/tutorials/adding-new-and-custom-extensions.html
  - Use case
    - env (environment.yaml)
    - setup.py
    - how to run, e.g., a notebook to load data from a csv metafile from PANGAEA, and pass the metainformation to py4dgeo.
  - Summary


## Ref

- https://github.com/radiantearth/stac-spec/blob/v1.1.0/best-practices.md
- https://github.com/radiantearth/stac-spec/blob/master/extensions/README.md
- https://github.com/stac-extensions/pointcloud?tab=readme-ov-file
- https://github.com/stac-extensions/mlm


## Acknowledgement
This work is funded by the German Research Foundation (DFG) through the project NFDI4Earth (4D-WORKS, DFG project no. 460036893, [https://www.nfdi4earth.de/](https://www.nfdi4earth.de/)) within the German National Research Data Infrastructure (NFDI, [https://www.nfdi.de/](https://www.nfdi.de/)). 
