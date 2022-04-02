import pandas as pd
from classrad.utils import utils

import config

dset = "prostate-diagnosis"


def combine_zonal_masks(mask_dir):
    mask_paths = mask_dir.rglob("*.nii.gz")
    for mask_path in mask_paths:
        print("test")
        utils.relabel_mask(str(mask_path), {1: 1, 2: 1}, str(mask_path))


def get_corresponding_image_path(mask_path):
    image_dir = mask_path.parents[2] / "images" / "nifti" / mask_path.stem[:-4]
    image_paths = list(image_dir.rglob("*.nii.gz"))
    assert len(image_paths) == 1
    return image_paths[0]


def parse_all_patients(mask_dir, clinical_df):
    mask_paths = mask_dir.rglob("*.nii.gz")
    result = {
        "image_path": [],
        "mask_path": [],
        "patient_ID": [],
        "gleason": [],
    }
    for mask_path in mask_paths:
        image_path = get_corresponding_image_path(mask_path)
        patient_ID = mask_path.stem[:-4]
        gleason = clinical_df.loc[
            clinical_df.index == patient_ID, "Gleason"
        ].values[0]
        result["image_path"].append(str(image_path))
        result["mask_path"].append(str(mask_path))
        result["patient_ID"].append(patient_ID)
        result["gleason"].append(gleason)
    return result


if __name__ == "__main__":
    mask_dir = config.PROSTATE_DIR / "data" / dset / "masks" / "nifti-prostate"
    # combine_zonal_masks(mask_dir)
    image_dir = config.PROSTATE_DIR / "data" / dset / "images" / "nifti"
    clinical_df = (
        pd.read_excel(
            config.TABLE_DIR / dset / "prostate_diagnosis_clinical.xlsx"
        )
        .set_index("TCIA ID")
        .T
    )
    result_dict = parse_all_patients(mask_dir, clinical_df)
    result_df = pd.DataFrame(result_dict)
    result_df.to_csv(config.TABLE_DIR / dset / "paths.csv", index=False)
