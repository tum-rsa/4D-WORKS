# 4D-WORKS
Repository for the NFDI4Earth 4D-WORKS project.

Project website: [https://www.asg.ed.tum.de/en/rsa/research/4d-works/](https://www.asg.ed.tum.de/en/rsa/research/4d-works/)

## Schema

### Item

| Field Name | Type | Description  |
|------------|------|--------------|
|            |      |              |
|            |      |              |
|            |      |              |

### Collection

| Field Name | Type | Description  |
|------------|------|--------------|
|            |      |              |
|            |      |              |
|            |      |              |

### Catalog


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
- demo
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
