# Important: this is a mirrored private repository of the public repository [4D-WORKS](https://github.com/tum-rsa/4D-WORKS), for ISPRS Congress tutorial preparation

### Check remotes

Use `git remote -v`, you should see below:

```
origin  https://github.com/tum-rsa/4D-WORKS-dev.git (fetch)
origin  https://github.com/tum-rsa/4D-WORKS-dev.git (push)
public  https://github.com/tum-rsa/4D-WORKS.git (fetch)
public  https://github.com/tum-rsa/4D-WORKS.git (push)
```

The ***origin*** is the private repo [4D-WORKS-dev](https://github.com/tum-rsa/4D-WORKS-dev.git), and the ***public*** is the public repo [4D-WORKS](https://github.com/tum-rsa/4D-WORKS).

### How to work with this private repo:

- To push daily update: use `git push origin main`. This goes to the private repo
- To get updates from the public repo: use `git fetch public` and `git merge public/main`. This fetch updates from public repo and merge them into the private repo.
- To publish the private features: use `git push public main`. ***This should only be done on the day of tutorial session (5 July, 2026).***


### Todo

- [ ] Installation guide and data download link. **@JW**
  - [ ] install markdown/pdf
  - [ ] env.yaml
  - [ ] data on zenodo/mediaTUM
- [x] Re-organize the tutorial repo structure. **@JW**
  - [x] tutorial notebooks are under [tutoral/](./docs/tutorial/)
- [x] Isar demo data: 5 epochs, 200 MB (uncompressed) per epoch, plus 2 sentinel-2 images. **@PG**
  - [x] downsampled point clouds in copc.laz format
- [ ] [NB1](./docs/tutorial/01_data2catalog.ipynb): From data to STAC. (Isar demo data) **@JW**
  - [x] helper fun()
  - [x] input: fetch data from public/local
  - [ ] update asset links with public repo address
  - [x] output: a STAC catalog
- [ ] [NB2](./docs/tutorial/02_query_catalog.ipynb): Query and filtering STAC to fetch selected data. **@PM**
  - [x] input: a STAC catalog
  - [x] interpretation, plotting, filtering
  - [x] display 2 sentinel-2 images (could be from a STAC catalog)
  - [ ] output: download filtered data assets
  - [ ] refinement with more interactivity (e.g., optional downloads, different colors in map visualization)
- [ ] [NB3](./docs/tutorial/03_catalog4analysis.ipynb): Perform a simple analysis (e.g., M3C2 by py4dgeo) and visualize (by CC/QGIS) with downloaded assets. **@XH**
  - [x] input: data assets
  - [x] two ways: programming-based and gui-based
  - [x] output: a map/plot of the analysis product (e.g., M3C2 distance map)
  - [ ] refinement of visuals (./tutorial/assets/*)
- [ ] [demo](./demo/): use Kijkduin catalog to present a minimal potree project. **@PM**
  - [ ] input: Kijkduin catalog, a demo potree repo, a one-touch deploy script.
  - [ ] output: a self-hosted STAC catalog and potree service
- [ ] Slides preparation **@ALL**
  - [ ] S1: concept and outline: problem -> solution -> today's task -> discussion
  - [ ] S2: roadmap of NBs
  - [ ] S3: demo description

### Milestones

- **M1 12.05**: NBs ready, data ready
- **M2 02.06**: slides ready, repo ready, talks ready
- **M3 15.06**: wrap-up and prepare the email to be sent to audience

---

# 4D-WORKS: Towards metadata standards and automatic curation workflows for 3D time series data considering interoperability and reusability in open-source tools and standard software

Repository of the NFDI4Earth 4D-WORKS pilot project.

Project website: [https://www.asg.ed.tum.de/en/rsa/research/4d-works/](https://www.asg.ed.tum.de/en/rsa/research/4d-works/)

## Build

**Conda:**
```
conda env create -f environment.yaml
conda activate 4dworks
```

**Setup [MkDocs](https://www.mkdocs.org/) locally**
```
cd mkdocs
mkdocs serve
```

## Funding
This work was funded by the German Research Foundation (DFG) through the pilot project [4D-WORKS](https://www.asg.ed.tum.de/en/rsa/research/4d-works/) (2025) within the [NFDI4Earth](https://www.nfdi4earth.de/) project (DFG project no. 460036893) within the German National Research Data Infrastructure ([NFDI](https://www.nfdi.de/)). 
