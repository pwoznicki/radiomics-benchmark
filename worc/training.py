import pandas as pd
from autorad.data.dataset import FeatureDataset
from autorad.models.classifier import MLClassifier
from autorad.preprocessing.preprocessor import Preprocessor
from autorad.training.trainer import Inferrer, Trainer
from autorad.utils import io

import config


def main():
    datasets = config.DATASETS
    for task_name in datasets:
        result_dir = config.RESULT_DIR / task_name
        feature_df = pd.read_csv(result_dir / "features.csv")
        feature_df = feature_df[feature_df.label != -1]
        feature_dataset = FeatureDataset(
            dataframe=feature_df,
            target="label",
            ID_colname="subject_id",
        )
        splits_path = result_dir / "splits.json"
        feature_dataset.full_split(splits_path)
        feature_dataset.load_splits_from_json(splits_path)
        models = MLClassifier.initialize_default_sklearn_models()
        trainer = Trainer(
            dataset=feature_dataset,
            models=models,
            result_dir=result_dir,
            experiment_name=task_name,
        )
        trainer.run_auto_preprocessing(oversampling=False)
        trainer.set_optimizer("optuna", n_trials=100)
        trainer.run(auto_preprocess=True)

        best_params = io.load_json(result_dir / "best_params.json")
        inferrer = Inferrer(params=best_params, result_dir=result_dir)
        inferrer.fit_eval(feature_dataset)


if __name__ == "__main__":
    main()
