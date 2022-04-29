def add_label_col(df):
    if "max_gleason" in df.columns:
        # df = df[df["max_gleason"] >= 6]
        df["label"] = df["max_gleason"] >= 6
    elif "gleason_group" in df.columns:
        # df = df[df["gleason_group"] > 0]
        df["label"] = df["gleason_group"] >= 1
    else:
        raise ValueError("No Gleason score column found")
    return df
