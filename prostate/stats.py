import numpy as np
import pandas as pd
from classrad.evaluation.utils import get_youden_threshold
from classrad.utils import io
from classrad.utils.statistics import describe_auc, describe_f1, describe_stat

import config

tasks = ["prostate-ucla", "prostatex"]
rois = ["prostate", "lesion"]
params = config.PARAMS

for task in tasks:
    for roi in rois:
        result_dir = config.RESULT_DIR / (task + "_PCa") / roi
        results_internal = io.load_json(result_dir / "internal_test.json")
        results_external = io.load_json(result_dir / "external_test.json")
        df = pd.read_csv(result_dir / "internal_test.csv")
        df_external = pd.read_csv(result_dir / "external_test.csv")
        print(f"{task}_{roi}:")
        auc_mean_cv = np.mean(results_internal["AUC train"])
        auc_std_cv = np.std(results_internal["AUC train"])
        print(f"AUC train: {auc_mean_cv:.3f} +/- {auc_std_cv:.3f}")
        auc_mean, auc_lower, auc_upper = describe_auc(
            df["y_true"], df["y_pred"]
        )
        thr, _, _ = get_youden_threshold(df["y_true"], df["y_pred"])
        f1_tuple = describe_f1(df["y_true"], (df["y_pred"] > thr))
        sens_tuple, spec_tuple = describe_stat(
            df["y_true"], (df["y_pred"] > thr)
        )
        # print(f"AUC test: {auc_mean:.3f} [{auc_lower:.3f}, {auc_upper:.3f}]")
        print("External:")
        auc_mean_ext, auc_lower_ext, auc_upper_ext = describe_auc(
            df_external["y_true"], df_external["y_pred"]
        )
        auc_ext_test = results_external["AUC test"]
        thr, _, _ = get_youden_threshold(df_external["y_true"], df["y_pred"])
        # print(f"AUC test ext: {auc_ext_test:.3f} [{auc_lower_ext:.3f}, {auc_upper_ext:.3f}]")
        f1_tuple = describe_f1(
            df_external["y_true"], (df_external["y_pred"] > thr)
        )
        sens_tuple, spec_tuple = describe_stat(
            df_external["y_true"], (df_external["y_pred"] > thr)
        )
