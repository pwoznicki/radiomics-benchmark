import pandas as pd

import config


def get_image_path(patient_ID, series_UID):
    result = (
        config.DATA_DIR
        / "prostate-ucla"
        / "images"
        / "nifti"
        / patient_ID
        / (series_UID + ".nii.gz")
    )
    if not result.exists():
        print("Warning: image path does not exist:", result)
        return None
    return str(result)


def get_mask_path(patient_ID, series_UID, roi):
    mask_dir = config.DATA_DIR / "prostate-ucla" / "masks" / "nifti"
    if roi == "prostate":
        result = mask_dir / patient_ID / f"ProstateSurface_{series_UID}.nii.gz"
    elif roi == "lesion":
        result = mask_dir / patient_ID / f"Target1_{series_UID}.nii.gz"
    else:
        raise ValueError("Unknown ROI:", roi)
    if not result.exists():
        print("Warning: mask path does not exist:", result)
        return None
    return str(result)


def main():
    df = pd.read_excel(str(config.TABLE_DIR / "prostate-ucla" / "biopsy.xlsx"))
    df["gleason"] = df["Primary Gleason"] + df["Secondary Gleason"]
    df.dropna(subset=["Series Instance UID (MRI)"], inplace=True)
    df["gleason"].fillna(value=0, inplace=True)
    patient_df = df.groupby(by="Series Instance UID (MRI)").max().reset_index()

    patient_df["image_path"] = patient_df.apply(
        lambda x: get_image_path(
            x["Patient Number"], x["Series Instance UID (MRI)"]
        ),
        axis=1,
    )
    patient_df["prostate_mask_path"] = patient_df.apply(
        lambda x: get_mask_path(
            x["Patient Number"], x["Series Instance UID (MRI)"], roi="prostate"
        ),
        axis=1,
    )
    patient_df["lesion_mask_path"] = patient_df.apply(
        lambda x: get_mask_path(
            x["Patient Number"], x["Series Instance UID (MRI)"], roi="lesion"
        ),
        axis=1,
    )
    path_df = patient_df[
        [
            "Patient Number",
            "gleason",
            "image_path",
            "prostate_mask_path",
            "lesion_mask_path",
            "Series Instance UID (MRI)",
        ]
    ]
    path_df.rename(
        {
            "Patient Number": "patient_ID",
            "gleason": "max_gleason",
            "Series Instance UID (MRI)": "series_UID",
        },
        axis="columns",
        inplace=True,
    )
    path_df.sort_values(by="patient_ID", inplace=True)
    path_df.dropna(inplace=True)
    path_df.to_csv(
        str(config.TABLE_DIR / "prostate-ucla" / "derived" / "paths.csv"),
        index=False,
    )


if __name__ == "__main__":
    main()
