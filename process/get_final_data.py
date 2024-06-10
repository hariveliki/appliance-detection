import os

import pandas as pd

FILEPATH = "data/concatenated/concatenated.csv"
DIR_OUT = "data/final"
FILENAME = "final.csv"


def get_final_data():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)
    df = pd.read_csv(FILEPATH)
    assert "Power" in df.columns
    assert "Messpunkt_ID" in df.columns
    df = df[["Power", "Messpunkt_ID"]]
    df["Count"] = df.groupby("Messpunkt_ID").cumcount()
    df = df.pivot(index="Messpunkt_ID", columns="Count", values="Power")
    filepath = os.path.join(DIR_OUT, FILENAME)
    df.to_csv(filepath, index=False)
    print(f"Written final dataframe to {DIR_OUT}")
    print(f"Final dataframe has shape: {df.shape}")


if __name__ == "__main__":
    get_final_data()
