from pathlib import Path

BASE_DIR = Path("/media/pw-research/hdd/radiomics-benchmark")
PROSTATE_DIR = BASE_DIR / "prostate"
DATASETS = ["prostate-diagnosis", "prostate-ucla", "prostatex"]
MODALITY_MAP = {}
DATA_DIR = PROSTATE_DIR / "data"
RESULT_DIR = PROSTATE_DIR / "results"
TABLE_DIR = PROSTATE_DIR / "tables"
EXCLUDED = {
    "ucla": ["Prostate-MRI-US-Biopsy-0473", "Prostate-MRI-US-Biopsy-0702"],
    "prostatex": [],
}
