import pandas as pd
from classrad.visualization.plotly_utils import plot_ROC

import config

tasks = ["prostatex", "prostate-ucla"]
rois = ["prostate", "lesion"]
cohorts = ["internal_test", "external_test"]
for task in tasks:
    for roi in rois:
        result_dir = config.RESULT_DIR / (task + "_PCa") / roi
        for cohort in cohorts:
            df = pd.read_csv(result_dir / f"{cohort}.csv")
            y_true = df["y_true"]
            y_pred_proba = df["y_pred"]
            fig = plot_ROC(y_true, y_pred_proba)
            fig.write_image(result_dir / f"ROC_{cohort}.png")
