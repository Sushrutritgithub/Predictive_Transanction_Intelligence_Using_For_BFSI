import pandas as pd
import numpy as np

def preprocess_input(data: dict, feature_order: list):
    df = pd.DataFrame([data])

    drop_cols = ["sender_id", "receiver_id"]
    for col in drop_cols:
        if col in df.columns:
            df = df.drop(col, axis=1)

    df = pd.get_dummies(df, columns=["transaction_type"], drop_first=True)

    for col in feature_order:
        if col not in df.columns:
            df[col] = 0 

    df = df[feature_order]

    return df
