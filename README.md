### Code for the analysis used in the paper "AutoRadiomics: A Framework for Reproducible Radiomics Research" [Woznicki et al. 2022](https://www.frontiersin.org/articles/10.3389/fradi.2022.919133/full)


### Requirements
```
git clone https://github.com/pwoznicki/AutoRadiomics
cd AutoRadiomics
git checkout 8d35988cd475af84573f11993542724912485825 # commit from 25.04.2022
pip install -e .
```

### Run experiments
Select your base directory for all experiments and update `BASE_DIR` in `worc/config.py`.

# WORC datasets
1. Download data for all six experiments from https://xnat.bmia.nl/data/projects/worc and put all of them in `<your_base_dir>/worc/data/`.

2. Download table with labels and clinical data from the XNAT repository (Scroll down to Subjects -> Options -> Spreadsheet). Save it as <your_base_dir>/worc/tables/clinical.csv

3. Run the scripts:
```
cd worc
python preprocess.py
python feature_extraction.py
python training.py
```

The results will be saved in `<your_base_dir>/worc/results/`.

# Prostate datasets (Prostate-UCLA and ProstateX)
#### Data Download
1. Prostate-UCLA:
- Download DICOM images from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=68550661 (takes a while...) \ Save them in a folder <your_base_dir>/prostate/data/prostate-ucla/dicom/.

- Using the same link, download STL Files (ZIP). Unzip and put all the .STL files in the folder <your_base_dir>/prostate/data/prostate-ucla/masks/STL/.

- From the same link, download Biopsy data (Excel file). Save it as <your_base_dir>/prostate/tables/prostate-ucla/biopsy.xlsx.

2. PROSTATEx:
```
git clone https://github.com/rcuocolo/PROSTATEx_masks
cd PROSTATEx_masks
git checkout 43b55e454410d78831fd184d8010f23af91e5144
cp -r Files/lesions/* <your_base_dir>/prostate/data/prostatex/lesion
cp -r Files/prostate <your_base_dir>/prostate/data/prostatex/
cp -r Files/lesions/*.csv <your_base_dir>/prostate/tables/prostatex/

#### Preprocessing:
1. Prostate-UCLA requires conversion to Nifti:
- Convert dicom images to nifti (will be saved in <your_base_dir>/prostate/data/prostate-ucla/nifti/)):
```
cd <your_base_dir>/prostate/data/prostate-ucla/dicom/
dcm2niix -z y -f %i/%j -z y -o nifti dicom
```
- Convert segmentations from STL into nifti. For that, run a docker container with 3D Slicer Notebook environment from this directory. In there, run the notebook `work/preprocessing/slicer_stl_to_nifti.ipynb` (set the paths accordingly) with Slicer kernel.
```
cd prostate
docker run -p 8888:8888 -p 49053:49053 -v <your_base_dir>/prostate/data/prostate-ucla/:/data -v "$PWD":/home/sliceruser/work --rm -ti lassoan/slicer-notebook:latest
```
```
python create_path_df_ucla.py
```
2. PROSTATEx:
```
python create_path_df_prostatex.py
```
#### Feature extraction:
```
python feature_extraction.py
```

