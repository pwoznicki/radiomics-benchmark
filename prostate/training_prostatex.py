import pandas as pd
from classrad.data.dataset import FeatureDataset
from classrad.models.classifier import MLClassifier
from classrad.preprocessing.preprocessor import Preprocessor
from classrad.training.trainer import Trainer

import config


def main():
    result_dir = config.RESULT_DIR / "prostatex"
    df = pd.read_csv(result_dir / "prostate_features.csv")
    # Load features from table
    dataset = FeatureDataset(
        dataframe=df,
        target="label",
        ID_colname="case_ID",
    )
    # Split and load splits
    splits_path = result_dir / "splits.json"
    dataset.full_split(save_path=splits_path)
    dataset.load_splits_from_json(splits_path)
    # Preprocessing
    preprocessor = Preprocessor(
        normalize=True,
        feature_selection_method="anova",
        n_features=10,
        oversampling_method="SMOTE",
    )
    dataset._data = preprocessor.fit_transform(dataset.data)

    model = MLClassifier.from_sklearn(name="Random Forest")
    model.set_optimizer("optuna", n_trials=5)

    trainer = Trainer(
        dataset=dataset,
        models=[model],
        result_dir=result_dir,
        experiment_name="ProstateX-test",
    )
    trainer.run()


if __name__ == "__main__":
    main()
