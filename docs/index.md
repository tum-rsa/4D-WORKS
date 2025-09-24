# 4D-WORKS: Towards metadata standards and automatic curation workflows for 3D time series data considering interoperability and reusability in open-source tools and standard software

Project website: [https://www.asg.ed.tum.de/en/rsa/research/4d-works/](https://www.asg.ed.tum.de/en/rsa/research/4d-works/)

## Abstract

Topographic 3D time series acquired through laser scanning or photogrammetry become increasingly available in many domains of Earth System Sciences. While standards and best practices have been established for 3D data, they are mostly lacking for multitemporal or time series data, where processing is currently mostly time-agnostic and (meta)data handled in a user-specific design. The objective of this pilot project is to develop a curation workflow for 3D time series data from different sources (platforms and sensors). Particular focus is on the development of standardized time-dependent metadata that can be automatically generated from different data acquisition strategies. The result will be a comprehensive guide and tutorials about developed best practices as a foundation for metadata standards, provided with an open-access repository of template material and scripts to integrate in workflows of the user community. Users are researchers and practitioners from any domain in Earth System Sciences that use multitemporal topographic data, i.a. from geomorphology, hydrology, ecology, and public and private organizations working in environmental monitoring contexts. The pilot project will strongly facilitate access and (re)usability of 3D time series for prospective users, where the developed metadata-rich workflows are fundamental for efficient and flexible use in domain-specific tasks. This advances RDM workflows to fully consider the special properties of 3D time series (4D data) and making them accessible to the wider user community. This contributes to NFDI4Earth efforts especially regarding long-term perspectives of data use and efficiency of analysis workflows.

## Roadmap Overview

This [metadata curation roadmap](roadmap/roadmap_concept.md) summarises how to ingest, construct, and search a STAC-based metadata using topo4d extension for topographic 3D time series data.

- [Roadmap](roadmap/roadmap_concept.md) outlines the metadata ingestion, construction, and usage workflow.
- [Related Work](roadmap/roadmap_related_work.md) surveys standards, repositories, and tools informing our approach.
- [Topo4D Extension API](api/topo4d-extension.md) provides the STAC extension fields and validation helpers.
- [Builder API](api/builder.md) provides helpers for making STAC Items using other community open-source tools, e.g., laspy, PDAL, etc..
- [Notebook: make_STAC_kijkduin](notebooks/make_STAC_kijkduin.ipynb) example notebook building a STAC catalog from near-continuous terrestrial laser scanning point clouds.
- [Notebook: make_STAC_Isar](notebooks/make_STAC_Isar.ipynb) example notebook building a STAC catalog involve multi-temporal multi-source point clouds and relevant products.
- [Notebook: demo_stac_kijkduin](notebooks/demo_stac_kijkduin.ipynb) example notebook showcasing the usage of STAC catalog with analysis tools, e.g., py4dgeo.

## Topographic 4D STAC Extension

[topo4d](https://github.com/tum-rsa/topo4d)

## Acknowledgement
This work is funded by the German Research Foundation (DFG) in the frame of the National Research Data Infrastructure program [NFDI4EARTH](https://www.nfdi4earth.de/) (project number: 460036893).
