import pandas as pd
from classrad.data.dataset import ImageDataset
from classrad.feature_extraction.extractor import FeatureExtractor

import config

dataset = "prostate-ucla"
df = pd.read_csv(config.TABLE_DIR / dataset / "derived" / f"paths.csv")
result_dir = config.RESULT_DIR / dataset
result_dir.mkdir(exist_ok=True, parents=True)

for roi in ["prostate", "lesion"]:
    image_dataset = ImageDataset(
        df=df,
        image_colname="image_path",
        mask_colname=f"{roi}_mask_path",
        ID_colname="series_UID",
    )
    # Feature extraction
    extraction_params = "default_MR.yaml"
    extractor = FeatureExtractor(
        image_dataset,
        out_path=(result_dir / f"{roi}_features.csv"),
        extraction_params=extraction_params,
    )
    extractor.extract_features(num_threads=1)
