import pandas as pd
from autorad.data.dataset import FeatureDataset
from autorad.models.classifier import MLClassifier
from autorad.training.trainer import Inferrer, Trainer
from autorad.utils import io

import config
import utils


def main():
    tasks = ["prostatex", "prostate-ucla"]
    params = config.PARAMS
    for roi in ["prostate", "lesion"]:
        dataset = {}
        for task in tasks:
            print(f"Training {task} {roi}")
            result_dir = config.RESULT_DIR / task / roi
            df = pd.read_csv(result_dir / f"{roi}_features.csv")
            df = utils.add_label_col(df)
            # Load features from table
            dataset[task] = FeatureDataset(
                dataframe=df,
                target="label",
                ID_colname=params[task]["ID_colname"],
            )
            # Split and load splits
            splits_path = result_dir / "splits.json"
            split_on = params[task]["split_on"]
            dataset[task].full_split(save_path=splits_path, split_on=split_on)
            dataset[task].load_splits_from_json(splits_path, split_on=split_on)
        for task in tasks:
            result_dir = config.RESULT_DIR / task / roi
            models = MLClassifier.initialize_default_sklearn_models()
            trainer = Trainer(
                dataset=dataset[task],
                models=models,
                result_dir=result_dir,
                experiment_name=f"{task}_{roi}",
            )
            trainer.run_auto_preprocessing(
                oversampling=params[task]["oversampling"]
            )
            trainer.set_optimizer("optuna", n_trials=20)
            trainer.run(auto_preprocess=True)

            best_params = io.load_json(result_dir / f"best_params.json")
            inferrer = Inferrer(params=best_params, result_dir=result_dir)
            inferrer.fit_eval(dataset[task], result_name=f"internal_test")
            other_tasks = [t for t in tasks if t != task]
            for other_task in other_tasks:
                # inferrer.fit(dataset[task])
                inferrer.eval(
                    dataset[other_task],
                    result_name=f"external_test_{other_task}",
                )


if __name__ == "__main__":
    main()
