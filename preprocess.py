from process.preprocess_data import preprocess_data
from process.preprocess_labels import preprocess_labels
from process.concatenate import concatenate
from process.get_final_data import get_final_data


def preprocess():
    preprocess_data()
    concatenate()
    preprocess_labels()
    get_final_data()


if __name__ == "__main__":
    preprocess()
