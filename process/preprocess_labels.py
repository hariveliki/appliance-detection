import os

import pandas as pd

import utils.utils_preprocess as utils_preprocess
from process.mapping import label2idx
from process.mapping import idx2label

DIR_IN = "data/concatenated"
FILENAME = "concatenated.csv"
DIR_OUT = "labels"


def preprocess_labels():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)
    print("Start preprocessing labels")
    filepath = os.path.join(DIR_IN, FILENAME)
    df = pd.read_csv(filepath)
    df = df[df["OHE_Labels"].notna()]
    df["OHE_Labels"] = df["OHE_Labels"].apply(lambda x: eval(x))
    for idx, label in idx2label.items():
        df[label] = df["OHE_Labels"].apply(lambda x: x[int(idx)])
    for idx, device in idx2label.items():
        device_df = df.groupby("Messpunkt_ID")[device].max().reset_index()
        device_df.columns = ["id", "label"]
        if "/" in device:
            filename = f'{device.replace("/", "_").lower()}.csv'
        elif "-" in device:
            filename = f'{device.replace("-", "_").lower()}.csv'
        else:
            filename = f'{device.replace(" ", "_").lower()}.csv'
        try:
            filepath = os.path.join(DIR_OUT, filename)
            if not os.path.exists(DIR_OUT):
                os.makedirs(DIR_OUT)
            device_df.to_csv(filepath, index=False)
        except:
            print(f"Error with filename: {filename}")
    print(f"Written labels to directory: {DIR_OUT}")


if __name__ == "__main__":
    preprocess_labels()
