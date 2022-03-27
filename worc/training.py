import pandas as pd
from classrad.data.dataset import FeatureDataset
from classrad.models.classifier import MLClassifier
from classrad.training.trainer import Trainer

import config

dataset_name = config.DATASETS[0]
feature_df = pd.read_csv(
    config.WORC_DIR / "results" / dataset_name / "features.csv"
)
features = [
    col
    for col in feature_df.columns
    if col.startswith(("original", "wavelet", "log-sigma"))
]
feature_dataset = FeatureDataset(
    dataframe=feature_df,
    features=features,
    target="label",
    ID_colname="subject_id",
    task_name=f"{dataset_name}",
    meta_columns=["subject_id", "label"],
)
split_path = config.RESULT_DIR / dataset_name / "splits.json"
feature_dataset.full_split(split_path)
feature_dataset.load_splits_from_json(split_path)
model = MLClassifier.from_sklearn(name="Random Forest")
model.set_optimizer("optuna", n_trials=5)

trainer = Trainer(
    dataset=feature_dataset,
    models=[model],
    result_dir=config.RESULT_DIR,
    feature_selection="anova",
    num_features=10,
    experiment_name="exp1",
)

trainer.run()
