import os

from tqdm import tqdm

import app as main
from src.computations import Model

DATASET = "../database"

if __name__ == '__main__':
    for version in tqdm(os.listdir(DATASET)):
        if os.path.isdir(os.path.join(DATASET, version)):
            main.DATASET_NAME = version
            main.model = Model(f"../database/{version}/TRAIN")
            main.SPLIT = "TEST"
            main.run_all(f"{DATASET}/{version}/TEST", report_prefix=version+"_TEST")
            main.SPLIT = "UNSEEN"
            main.run_all(f"{DATASET}/{version}/UNSEEN", report_prefix=version+"_UNSEEN")
