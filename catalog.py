import os
import pandas as pd

def load_first_csv():
    for file_name in os.listdir():
        if file_name.endswith(".csv"):
            return pd.read_csv(file_name), file_name
    return None, None

def get_dataset_metadata(df, file_name):
    metadata = {
        "dataset_name": file_name.replace(".csv", ""),
        "columns": df.columns.tolist(),
        "sample_values": {}
    }

    for col in df.columns:
        try:
            unique_vals = df[col].dropna().astype(str).unique()[:10]
            metadata["sample_values"][col] = unique_vals.tolist()
        except:
            metadata["sample_values"][col] = []

    return metadata
