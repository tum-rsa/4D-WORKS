# 4D-Works project roadmap

## Related work: existing metadata practices in published literature and software
[here we insert our notes, illustrations, etc as mentioned in the kickoff. Illustrations to be kept in the final version should be in the assets folder too.]

### Metadata practices in published 4D datasets


### Metadata practices in satellite image time series (SITS)


### The STAC catalogue


### Metadata in open-source geospatial software

#### The LAS format (ASPRS):
![image](.\assets\las_format_def.png)
* VLRs contain the projection, metadata, waveform packet info, etc
* EVLRs can be appened at the end of the file -> info can be added without rewriting the whole file. They have a higher payload than the VLRs

The header of a LAS file has the following info:
![image](.\assets\LAS_header1.png)
![image](.\assets\LAS_header2.png)
* LAS uses WKT (and for legacy point records formats GeoTiff) to save the CRS

The minimum information for a point in the LAS format is the following (point data record format 0):
![image](.\assets\LAS_PDRF_0.png)

Other info can be recorded with the different PDRFs. Here is a recap:
![image](.\assets\las_cheatsheet.png)
A good recap of what's added in each PDRF is available here: https://laspy.readthedocs.io/en/latest/intro.html#header

Note: attribute formats need to be defined (e.g. float32? int8? uint16? etc). -> Interesting info from pylas:
![image](.\assets\extra_dimensions.png)

#### COPC
* COPC stores data in chunks depending on the octree
    * only point info, no VLRs
    * COPC files MUST contain data with ONLY ASPRS LAS Point Data Record Format 6, 7, or 8
![image](.\assets\COPC_EPT.png)

#### EPT
![image](.\assets\EPT.png)
![image](.\assets\EPT2.png)

#### lapsy and pylas
Completely based on LAS (+ copc support), so same metadata info.

#### py4dgeo
* date info 
* transformation

#### pdal 

#### QGIS


#### CloudCompare
Formats supported:
![image](.\assets\CC_supported_formats.png)

Metadata:
![image](.\assets\CC_metadata.png)

### Metadata file formats: JSON and YAML



## Conceptual design of metadata requirements
[temporary, just to give an idea of the potential structure of the document]

## Conceptual design of the implementation frameworks
[temporary, just to give an idea of the potential structure of the document]
