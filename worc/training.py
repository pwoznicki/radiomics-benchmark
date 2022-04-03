import pandas as pd
from classrad.data.dataset import FeatureDataset
from classrad.models.classifier import MLClassifier
from classrad.preprocessing.preprocessor import Preprocessor
from classrad.training.trainer import Inferrer, Trainer
from classrad.utils import io

import config


def main():
    task_name = config.DATASETS[0]
    result_dir = config.RESULT_DIR / task_name
    feature_df = pd.read_csv(result_dir / "features.csv")
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
    trainer.set_optimizer("optuna", n_trials=15)
    # trainer.run(auto_preprocess=True)

    best_params = io.load_json(result_dir / "best_params.json")
    inferrer = Inferrer(params=best_params, result_dir=result_dir)
    inferrer.fit_eval(feature_dataset.data)


if __name__ == "__main__":
    main()
