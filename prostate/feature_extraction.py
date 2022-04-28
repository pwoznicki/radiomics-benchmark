import pandas as pd
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor

import config

datasets = ["prostatex", "prostate-ucla"]
for dataset in datasets:
    df = pd.read_csv(config.TABLE_DIR / dataset / "derived" / f"paths.csv")
    df = df.loc[~df.case_ID.isin(config.EXCLUDED["prostatex"])]
    result_dir = config.RESULT_DIR / dataset
    result_dir.mkdir(exist_ok=True, parents=True)

    for roi in ["prostate", "lesion"]:
        # Load dataframe
        image_dataset = ImageDataset(
            df=df,
            image_colname="image_path",
            mask_colname=f"{roi}_mask_path",
            ID_colname="finding_ID",
        )
        # Feature extraction
        extraction_params = "default_MR.yaml"
        extractor = FeatureExtractor(
            image_dataset,
            out_path=(result_dir / f"{roi}_features.csv"),
            extraction_params=extraction_params,
        )
        extractor.extract_features(num_threads=8)
