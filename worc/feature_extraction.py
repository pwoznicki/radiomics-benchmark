import pandas as pd
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor

import config

modality_dict = config.MODALITY_MAP


def get_pyradiomics_param_file(dataset):
    modality = modality_dict[dataset]
    if modality == "CT":
        return "Baessler_CT.yaml"
    elif modality == "MR":
        return "default_MR.yaml"
    else:
        raise ValueError(f"Modality {modality} not recognized.")


def main():
    for dataset in config.DATASETS:
        print(f"Processing dataset: {dataset}")
        df = pd.read_csv(
            config.WORC_DIR / "tables" / "derived" / f"{dataset}_paths.csv"
        )
        result_dir = config.RESULT_DIR / dataset
        result_dir.mkdir(exist_ok=True, parents=True)

        image_dataset = ImageDataset(
            df=df,
            image_colname="image_path",
            mask_colname="mask_path",
            ID_colname="subject_id",
        )
        # Feature extraction
        extraction_params = get_pyradiomics_param_file(dataset)
        extractor = FeatureExtractor(
            image_dataset,
            out_path=(result_dir / "features.csv"),
            extraction_params=extraction_params,
        )
        extractor.extract_features(num_threads=8)


if __name__ == "__main__":
    main()
