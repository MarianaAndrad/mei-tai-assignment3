import os

from tqdm import tqdm

import streamlitdemo as main

DATASET = "../database"

if __name__ == '__main__':
    for version in tqdm(os.listdir(DATASET)):
        if os.path.isdir(os.path.join(DATASET, version)):
            main.DATASET_NAME = version
            main.run_all(f"{DATASET}/{version}/TEST", report_prefix=version)
