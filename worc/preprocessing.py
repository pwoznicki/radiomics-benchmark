from pathlib import Path

import pandas as pd

import config

df = pd.read_csv(config.WORC_DIR / "tables" / "clinical.csv")
df = df[~df["Subject"].isin(config.EXCLUDED_SUBJECTS)]

datasets = config.DATASETS


def get_mask_suffix(subject):
    if subject.startswith("CRLM"):
        return "_lesion0_RAD"
    elif (
        subject.startswith("Melanoma")
        or subject in subjects_with_two_segmentations
    ):
        return "_lesion0"
    return ""


subjects_with_two_segmentations = ["GIST-018"]


def create_path_df_for_all_datasets():
    for dataset in datasets:
        create_path_df_for_single_dataset(dataset)


def create_path_df_for_single_dataset(dataset):
    df_dataset = df[df["Dataset"] == dataset].copy()
    result_dict = {
        "subject_id": [],
        "label": [],
        "image_path": [],
        "mask_path": [],
    }
    for _, row in df_dataset.iterrows():
        subject = row["Subject"]
        label = row["Diagnosis_binary"]
        modality = get_modality(row)

        dir_path = (
            config.WORC_DIR
            / "data"
            / (f"{subject}_{modality}")
            / "1"
            / "NIFTI"
        )
        image_path, mask_path = get_image_and_mask_paths(dir_path, subject)

        result_dict["subject_id"].append(subject)
        result_dict["label"].append(label)
        result_dict["image_path"].append(image_path.as_posix())
        result_dict["mask_path"].append(mask_path.as_posix())
    df_result = pd.DataFrame(result_dict)
    table_dir = config.WORC_DIR / "tables" / "derived"
    table_dir.mkdir(exist_ok=True, parents=True)
    df_result.to_csv(
        table_dir / f"{dataset}_paths.csv",
        index=False,
    )


def get_image_and_mask_paths(dir_path, subject):
    image_path = dir_path / "image.nii.gz"
    mask_suffix = get_mask_suffix(subject)
    mask_path = dir_path / f"segmentation{mask_suffix}.nii.gz"
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not mask_path.exists():
        raise FileNotFoundError(f"Mask file not found: {mask_path}")

    return image_path, mask_path


def get_modality(row):
    if row["CT Sessions"] == 1:
        return "CT"
    elif row["MR Sessions"] == 1:
        return "MR"
    else:
        raise ValueError(f"No modality found for Subject: {row.Subject}")


def main():
    create_path_df_for_all_datasets()


if __name__ == "__main__":
    main()
