# Corpus Callosum Involvement — Registration Pipeline (pHGG vs Adult GBM)

Registers pediatric high-grade glioma (BraTS-PEDs) and adult glioblastoma
(BraTS-GLI) cases to MNI152 space and measures tumor overlap with the corpus
callosum. `data/histologies.tsv` and `data/BraTS-PEDs_metadata.tsv` (cohort
selection) and `atlas/` (CC masks) are already included.

## Steps

1. Set up the environment (Python 3.11):
   ```bash
   cd PEDs-HGG
   python3.11 -m venv venv_ants
   source venv_ants/bin/activate
   pip install --upgrade pip && pip install -r requirements.txt
   ```

2. Verify install: `python -c "import ants, nibabel, numpy, pandas; print('all OK')"`

3. Download pediatric imaging from TCIA
   (https://www.cancerimagingarchive.net/collection/brats-peds/), extract to
   `data/BraTS-PEDs-v1/Training/` so each case folder holds `*-t1c.nii.gz` and
   `*-seg.nii.gz`.

4. Download adult imaging from Synapse into `data/BraTS-GLI/`:
   ```bash
   export SYNAPSE_AUTH_TOKEN=your_token_here   # synapse.org -> Account -> Access Tokens
   python download_gbm_synapse.py
   ```

5. Register the pediatric cohort:
   ```bash
   python cc_registration_peds.py             # -> cc_results_peds/cc_results_phgg.csv
   ```

6. Filter the adult cohort to GBM-like cases (ET > 100):
   ```bash
   python scan_gli_et.py                       # -> cc_results_gbm/gbm_cases.txt
   ```

7. Register the adult cohort:
   ```bash
   python cc_registration_gbm.py               # -> cc_results_gbm/cc_results_gbm.csv
   ```

8. Results are in `cc_results_peds/` and `cc_results_gbm/` (per-case JSON + a
   combined CSV each).

Notes: activate the venv before each run; scripts skip cases that already have a
`_cc.json`, so interrupted runs resume; run step 6 before step 7.


## Registration output

CC involvement counts from the registration stage, before any statistical
analysis. WT = whole tumor, TC = tumor core, ET = enhancing tumor.

| Metric | pHGG (n=104) | Adult GBM (n=1213) |
|--------|--------------|--------------------|
| CC whole — WT | 62 (59.6%) | 623 (51.4%) |
| CC whole — TC | 34 (32.7%) | 341 (28.1%) |
| CC whole — ET | 16 (15.4%) | 327 (27.0%) |
| CC genu — TC | 27 (26.0%) | 179 (14.8%) |
| CC genu — WT | 57 (54.8%) | 467 (38.5%) |
| CC body — TC | 17 (16.3%) | 216 (17.8%) |
| CC splenium — WT | 10 (9.6%) | 275 (22.7%) |
| CC splenium — TC | 5 (4.8%) | 173 (14.3%) |
| Butterfly WT | 45 (43.3%) | 422 (34.8%) |
| Butterfly ET | 6 (5.8%) | 208 (17.1%) |

Counts are cases with any overlap in that region. ET metrics reflect that a large
share of pHGG is non-enhancing (et_vol = 0), unlike the enhancement-filtered GBM
cohort. Significance testing is done in the separate analysis stage.

## Registration to MNI152 Space

Sample cases warped to the MNI152 template. Red = warped tumor (whole tumor) in
MNI space; cyan = corpus callosum contour. Each panel shows sagittal, coronal,
and axial views at the midline. These span CC-involved and non-involved cases so
the computed overlap flags can be checked against anatomy.

| Case | CC whole (WT) | CC genu (TC) | Butterfly (WT) |
|------|---------------|--------------|----------------|
| BraTS-PED-00033-000 | yes | yes | yes |
| BraTS-PED-00001-000 | yes | yes | yes |
| BraTS-PED-00043-000 | yes | no  | yes |
| BraTS-PED-00128-000 | no  | no  | no |
| BraTS-PED-00151-000 | no  | no  | no |

![QC BraTS-PED-00033-000](mni-mapping-sample/QC_BraTS-PED-00033-000.png)
![QC BraTS-PED-00001-000](mni-mapping-sample/QC_BraTS-PED-00001-000.png)
![QC BraTS-PED-00043-000](mni-mapping-sample/QC_BraTS-PED-00043-000.png)
![QC BraTS-PED-00128-000](mni-mapping-sample/QC_BraTS-PED-00128-000.png)
![QC BraTS-PED-00151-000](mni-mapping-sample/QC_BraTS-PED-00151-000.png)
