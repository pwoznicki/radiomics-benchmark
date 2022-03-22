from pathlib import Path

BASE_DIR = Path("/media/pw-research/hdd/radiomics-benchmark")
WORC_DIR = BASE_DIR / "worc"
DATASETS = ["CRLM", "Desmoid", "GIST", "Lipo", "Liver", "Melanoma"]
MODALITY_MAP = {
    "CRLM": "CT",
    "Desmoid": "MR",
    "GIST": "CT",
    "Lipo": "MR",
    "Liver": "MR",
    "Melanoma": "CT",
}
RESULT_DIR = WORC_DIR / "results"
EXCLUDED_SUBJECTS = [
    "Melanoma-037",
    "Melanoma-039",
    "Melanoma-064",
    "Melanoma-071",
    "Melanoma-089",
    "Melanoma-094",
    "Melanoma-096",
    "Melanoma-100",
    "GIST-244",
]
