import sys
import os

import pandas as pd

import utils.utils_preprocess as utils_preprocess
from process.mapping import label2idx

DIR_IN = "data/raw"
DIR_OUT = "data/processed"


def preprocess_data():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)
    for filename in os.listdir(DIR_IN):
        filepath = os.path.join(DIR_IN, filename)
        df = pd.read_csv(filepath, low_memory=False)
        df = utils_preprocess.get_timestamped(df)
        assert "Timestamp" in df.columns
        assert len(df.get("Timestamp").unique()) > 1
        df = utils_preprocess.get_kanal(df, 1.29)
        assert all(kanal == 1.29 for kanal in df.get("Kanal").unique())
        df["Strom_Bezeichnung"].fillna("Unknown", inplace=True)
        df["OHE_Labels"] = df.apply(
            utils_preprocess.one_hot_encode, axis=1, args=(label2idx,)
        )
        df = df[df["OHE_Labels"].notna()]
        filepath = os.path.join(DIR_OUT, filename)
        df.to_csv(filepath, index=False)
        print(f"Preprocessed df with shape: {df.shape} and columns: {df.columns}")


if __name__ == "__main__":
    preprocess_data()
