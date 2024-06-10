import torch
import json
import pandas as pd
import numpy as np
from tqdm import tqdm


def write_json_to_file(data, file_name):
    with open(file_name, "w") as outfile:
        json.dump(data, outfile, indent=4)


def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")


def get_timestamped(df: pd.DataFrame) -> pd.DataFrame:
    print("At utils.get_timestamped: Creating Timestamp column as pd.to_datetime().")
    print("Wait, it may take a while.")
    if "Timestamp" not in df.columns:
        df.insert(len(df.columns), "Timestamp", np.nan)
    timestamp = df.columns.get_loc("Timestamp")
    date = df.columns.get_loc("Datum")
    timeslot = df.columns.get_loc("Timeslot")
    for row in tqdm(range(len(df))):
        df.iloc[row, timestamp] = pd.to_datetime(
            str(df.iloc[row, date]) + " " + df.iloc[row, timeslot].split("-")[0],
            format="%Y%m%d %H:%M",
        )
    return df


def get_kanal(df: pd.DataFrame, kanal: float) -> pd.DataFrame:
    if not "Kanal" in df.columns:
        raise Exception("Kanal not in df.")
    df = df[df["Kanal"] == kanal]
    return df


def one_hot_encode(row, label2idx, length=15):
    labels = row["Strom_Bezeichnung"].split(",")
    if "" in labels:
        labels.remove("")
    labels = [label.strip() for label in labels]
    indices = [label2idx[label] for label in labels]
    ohe_array = np.zeros(length, dtype=int)
    ohe_array[indices] = 1
    return ohe_array.tolist()
