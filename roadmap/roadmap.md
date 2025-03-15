# 4D-Works project roadmap

## Related work: existing metadata practices in published literature and software
[here we insert our notes, illustrations, etc as mentioned in the kickoff. Illustrations to be kept in the final version should be in the assets folder too.]

### Metadata practices in published 4D datasets


### Metadata practices in satellite image time series (SITS)
1. Landsat (USGS)  
    - [Data download link](https://earthexplorer.usgs.gov/)
    - Example Dataset: LC08_L1TP_123032_20231005_20231012_01_T1 (Landsat 8 Collection 2 Level-1, acquired on October 5, 2023)
        ```
        LC08_L1TP_123032_20231005_20231012_01_T1/
        ├── LC08_L1TP_123032_20231005_20231012_01_T1_B1.TIF  # Band 1 (Coastal Aerosol)
        ├── LC08_L1TP_123032_20231005_20231012_01_T1_B2.TIF  # Band 2 (Blue)
        ├── ...  # Bands 3-9 and QA bands
        └── LC08_L1TP_123032_20231005_20231012_01_T1_MTL.txt  # Metadata file
        ```
    Metadata Breakdown (LC08_L1TP_123032_20231005_20231012_01_T1_MTL.txt):
    - Temporal:
        ```
        DATE_ACQUIRED = "2023-10-05"
        SCENE_CENTER_TIME = "03:22:14.7564530Z"
        ```
        Radiometric Calibration:
        ```
        RADIANCE_MULT_BAND_4 = 1.2478E-02
        RADIANCE_ADD_BAND_4 = -62.38818
        REFLECTANCE_MULT_BAND_4 = 2.0000E-05
        ```
        Geometric:
        ```
        CORNER_UL_LAT_PRODUCT = 34.12345
        CORNER_UL_LON_PRODUCT = -118.54321
        MAP_PROJECTION = "UTM"
        ```    


2. Sentinel (ESA/Copernicus) 
    - [Open Access Hub](https://www.copernicus.eu/en/access-data/conventional-data-access-hubs) 
    - [Data products format](https://sentiwiki.copernicus.eu/web/s2-products#S2Products-DataFormatsS2-Products-Data-Formatstrue)
    - Example Dataset: S2B_MSIL2A_20231005T032214_N0509_R018_T48UYU_20231005T062456.SAFE (Sentinel-2B L2A, acquired on October 5, 2023, Tile 48UYU).
        ```
        S2B_MSIL2A_20231005T032214_N0509_R018_T48UYU_20231005T062456.SAFE/
        ├── MTD_MSIL2A.xml                # Main metadata file
        ├── AUX_DATA/                     # Auxiliary data
        ├── GRANULE/
        │   └── L2A_T48UYU_A030050_20231005T032214/
        │       ├── MTD_TL.xml            # Tile-specific metadata
        │       ├── IMG_DATA/
        │       │   ├── R10m/            # 10m resolution bands (B02, B03, B04, B08)
        │       │   └── R20m/             # 20m resolution bands (B05, B11, etc.)
        │       └── QI_DATA/              # Quality masks (CLD, SNW, etc.)
        └── HTML/                         # Preview images
        ```
    Metadata Breakdown (MTD_MSIL2A.xml):   
    - Temporal:
        ```
        <SENSING_TIME>2023-10-05T03:22:14.756Z</SENSING_TIME>
        <ORBIT_NUMBER>321</ORBIT_NUMBER>
        ```
    - Geometric:
        ```
        <Geometric_Info>
        <Tile_Geocoding>
            <HORIZONTAL_CS_NAME>WGS84 / UTM zone 32N</HORIZONTAL_CS_NAME>
            <ULX>699960.0</ULX>  <!-- Upper-left X coordinate -->
            <ULY>5100360.0</ULY> <!-- Upper-left Y coordinate -->
        </Tile_Geocoding>
        </Geometric_Info>   
        ``` 




### The STAC catalogue
SpatioTemporal Asset Catalog (STAC) specification provides a common structure for describing and cataloging spatiotemporal assets. STAC Catalog manages multi-temporal data by organizing it hierarchically (by time, space, or subject). e.g. [Example page](https://stac101.com/)
```
catalog/
├── year=2023/
│   ├── month=10/
│   │   ├── day=05/
│   │   │   └── sentinel-2-item.json
│   │   └── catalog.json
│   └── catalog.json
└── catalog.json
```

- STAC Catalog 
    -  is a simple, flexible **JSON file** of links that provides a structure to organize and browse STAC Items. A series of best practices helps make recommendations for creating real world STAC Catalogs.
        ```
        {
        "stac_version": "1.0.0",
        "type": "Catalog",
        "id": "20201211_223832_CS2",
        "description": "A simple catalog example",
        "links": []
        }
        ```
- STAC Collection 
    - is an **extension of the STAC Catalog** with additional information such as the **spatial and temporal extents**, license, keywords, providers, etc that describe STAC Items that fall within the Collection.
        ```
        {
        "stac_version": "1.0.0",
        "type": "Collection",
        "license": "ISC",
        "id": "20201211_223832_CS2",
        "description": "A simple collection example",
        "links": [],
        "extent": {},
        "summaries": {}
        }
        ```
- STAC Item 
    - is the core atomic unit, representing a single spatiotemporal asset as a **GeoJSON feature** plus datetime and links.
        ```
        {
        "stac_version": "1.0.0",
        "type": "Feature",
        "id": "20201211_223832_CS2",
        "bbox": [],
        "geometry": {},
        "properties": {},
        "collection": "simple-collection",
        "links": [],
        "assets": {}
        }
        ```
    - Item Metadata:
        1. core item metadata
            - spatiotemporal information and the ID of the collection to which the item belongs.
            - access through attributes on the PySTAC Item instance.
        2. common metadata
            - include licensing and instrument information, descriptions of datetime ranges, and some other common fields.
        3. STAC extension
            - providing additional metadata not covered by the core STAC Spec.
            - [time series extension (deprecated)](https://github.com/stac-extensions/timeseries)









### Metadata in open-source geospatial software


### Metadata file formats: JSON and YAML



## Conceptual design of metadata requirements
[temporary, just to give an idea of the potential structure of the document]

## Conceptual design of the implementation frameworks
[temporary, just to give an idea of the potential structure of the document]
