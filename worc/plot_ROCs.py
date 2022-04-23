import pandas as pd
from classrad.visualization.plotly_utils import plot_ROC

import config

tasks = config.DATASETS

for task in tasks:
    result_dir = config.RESULT_DIR / task
    df = pd.read_csv(result_dir / "test_results.csv")
    y_true = df["y_true"]
    y_pred_proba = df["y_pred"]
    fig = plot_ROC(y_true, y_pred_proba)
    fig.write_image(result_dir / "ROC.png")
