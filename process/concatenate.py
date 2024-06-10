import os

import pandas as pd

DIR_IN = "data/processed"
DIR_OUT = "data/concatenated"
FILENAME = "concatenated.csv"


def concatenate():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)
    data_frames: list = []
    for filename in os.listdir(DIR_IN):
        filepath = os.path.join(DIR_IN, filename)
        df = pd.read_csv(filepath)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        data_frames.append(df)

    df = pd.concat(data_frames)
    filepath = os.path.join(DIR_OUT, FILENAME)
    df.to_csv(filepath, index=False)
    print(f"Concatenated data frames, shape is now: {df.shape}")


if __name__ == "__main__":
    concatenate()
