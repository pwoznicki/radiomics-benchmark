from pathlib import Path

import config
import pandas as pd


def get_image_path(case_ID, modality, image_names):
    fname = image_names.loc[image_names.case_ID == case_ID, modality].values[0]
    result = (
        config.DATA_DIR
        / "prostatex"
        / "lesion"
        / "Images"
        / modality
        / (fname + ".nii.gz")
    )
    if not result.exists():
        result = result.parent / (fname + ".nii")
        if not result.exists():
            print("Warning: image path does not exist:", result)
            return None
    return str(result)


def get_mask_path(case_ID, finding_ID, roi, modality="T2"):
    mask_dir = config.DATA_DIR / "prostatex" / roi
    if modality != "T2":
        raise ValueError(f"Unknown modality: {modality}")
    if roi == "prostate":
        result = mask_dir / "mask_prostate" / f"{case_ID}.nii.gz"
    elif roi == "lesion":
        result = (
            mask_dir
            / "Masks"
            / modality
            / f"{finding_ID}-t2_tse_tra_ROI.nii.gz"
        )
    else:
        raise ValueError("Unknown ROI:", roi)
    if not result.exists():
        alternative_path = result.parent / f"ProstateX-{result.name[11:]}"
        if not alternative_path.exists():
            alternative_path = result.parent / (
                result.name[:-11] + "0" + result.name[-11:]
            )
            if alternative_path.exists():
                result = alternative_path
            else:
                if case_ID == "ProstateX-0199":
                    result = (
                        result.parent
                        / "ProstateX-0199-Finding1-t2_tse_tra0_ROI.nii_ROI.nii.gz"
                    )
                elif case_ID == "ProstateX-0191":
                    result = (
                        result.parent
                        / "ProstateX-0191-Finding1-t2_tse_tra_Grappa30_ROI.nii.gz"
                    )
                elif case_ID == "ProstateX-0176":
                    result = (
                        result.parent
                        / "ProstateX-0176-Finding1-t2_tse_tra0_ROI.nii_ROI.nii.gz"
                    )
    return str(result)


def main():
    df = pd.read_csv(
        str(config.TABLE_DIR / "prostatex" / "PROSTATEx_Classes.csv")
    )
    df.rename(
        columns={
            "ID": "finding_ID",
            "Gleason Grade Group": "gleason_group",
            "Clinically Significant": "label",
        },
        inplace=True,
    )
    df["case_ID"] = df["finding_ID"].apply(lambda x: x[:-9])
    df["finding_ID"] = df["finding_ID"].apply(lambda x: x[:-9] + "-" + x[-8:])
    df.loc[
        df["gleason_group"] == "No biopsy information",
        "gleason_group",
    ] = 0
    df["gleason_group"] = df["gleason_group"].astype(int)
    df = (
        df.sort_values("gleason_group", ascending=False)
        .drop_duplicates(["case_ID"])
        .sort_values("case_ID")
    )
    image_names = pd.read_csv(
        config.TABLE_DIR / "prostatex" / "Image_list.csv"
    )
    image_names["case_ID"] = image_names["T2"].apply(lambda x: x.split("_")[0])
    # use only T2 images
    modality = "T2"
    df[f"image_path"] = df.apply(
        lambda x: get_image_path(x["case_ID"], modality, image_names),
        axis=1,
    )
    for roi in ["prostate", "lesion"]:
        df[f"{roi}_mask_path"] = df.apply(
            lambda x: get_mask_path(x["case_ID"], x["finding_ID"], roi, "T2"),
            axis=1,
        )
    df.dropna(axis="index", inplace=True)
    save_dir = config.TABLE_DIR / "prostatex" / "derived"
    save_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(
        save_dir / "paths.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
