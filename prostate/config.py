from pathlib import Path

BASE_DIR = Path("/media/pw-research/hdd/radiomics-benchmark")
PROSTATE_DIR = BASE_DIR / "prostate"
DATASETS = ["prostate-diagnosis", "prostate-ucla", "prostatex"]
MODALITY_MAP = {}
DATA_DIR = PROSTATE_DIR / "data"
RESULT_DIR = PROSTATE_DIR / "results"
TABLE_DIR = PROSTATE_DIR / "tables"
EXCLUDED = {
    "prostate-ucla": [
        "Prostate-MRI-US-Biopsy-0473",
        "Prostate-MRI-US-Biopsy-0702",
        "Prostate-MRI-US-Biopsy-0585",
    ],
    "prostatex": ["ProstateX-0189"],
}
PARAMS = {
    "prostatex": {
        "ID_colname": "case_ID",
        "split_on": "case_ID",
        "prostate": {},
        "oversampling": False,
    },
    "prostate-ucla": {
        "ID_colname": "series_UID",
        "split_on": "patient_ID",
        "oversampling": False,
    },
}
