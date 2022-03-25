from pathlib import Path

BASE_DIR = Path("/media/pw-research/hdd/radiomics-benchmark")
PROSTATE_DIR = BASE_DIR / "prostate"
DATASETS = ["prostate-diagnosis", "prostate-ucla", "prostatex"]
MODALITY_MAP = {}
RESULT_DIR = PROSTATE_DIR / "results"
EXCLUDED_SUBJECTS = []
