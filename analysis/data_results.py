import os

import pandas as pd

DIR_RESULTS = "../src/results"


def concat_classification_results(_type, test_bool):
    ws_i = [0, 1, 2, 3, 4, 5, 6]
    sh_i = [7, 8, 9, 10, 11, 12, 13, 14]
    ds_i = [15, 16, 17, 18, 19, 20, 21, 22, 23]
    nf_i = [24, 25, 26, 27, 28, 29, 30, 31, 32]

    classification = {
        "ws": pd.DataFrame(),
        "ds": pd.DataFrame(),
        "nf": pd.DataFrame(),
        "sh": pd.DataFrame()
    }

    for file in os.listdir(DIR_RESULTS):
        if not file.endswith(".csv"):
            continue

        file_path = os.path.join(DIR_RESULTS, file)
        if "best" in file:
            continue
        version = int(file.split("_")[0][1:])
        if test_bool and "TEST" in file:
            if _type in file:
                df = pd.read_csv(file_path)
                if any(version == v for v in ws_i):
                    classification["ws"] = pd.concat([classification["ws"], df])
                elif any(version == v for v in ds_i):
                    classification["ds"] = pd.concat([classification["ds"], df])
                elif any(version == v for v in nf_i):
                    classification["nf"] = pd.concat([classification["nf"], df])
                elif any(version == v for v in sh_i):
                    classification["sh"] = pd.concat([classification["sh"], df])
        elif "UNSEEN" in file:
            if _type in file:
                df = pd.read_csv(file_path)
                if any(version == v for v in ws_i):
                    classification["ws"] = pd.concat([classification["ws"], df])
                elif any(version == v for v in ds_i):
                    classification["ds"] = pd.concat([classification["ds"], df])
                elif any(version == v for v in nf_i):
                    classification["nf"] = pd.concat([classification["nf"], df])
                elif any(version == v for v in sh_i):
                    classification["sh"] = pd.concat([classification["sh"], df])

    return classification


def concat_classification_noise(_type, test_bool):
    classification = pd.DataFrame()

    for file in os.listdir(DIR_RESULTS):
        if not file.endswith(".csv"):
            continue

        file_path = os.path.join(DIR_RESULTS, file)
        if "best" in file:
            if test_bool and "TEST" in file:
                if _type in file:
                    df = pd.read_csv(file_path)
                    classification = pd.concat([classification, df])
            elif "UNSEEN" in file:
                if _type in file:
                    df = pd.read_csv(file_path)
                    classification = pd.concat([classification, df])

    return classification


def concat_results():
    return concat_classification_results("genre", True), concat_classification_results("music", True), \
        concat_classification_results("genre", False), concat_classification_results("music", False)


def main():
    partition_list = [0.2, 0.5, 1]
    classification_genre_test, classification_music_test, classification_genre_unseen, classification_music_unseen = concat_results()
    concat_classification_noise("music", True).to_csv("classification_music_noise_test.csv", index=False)
    concat_classification_noise("music", False).to_csv("classification_music_noise_unseen.csv", index=False)
    concat_classification_noise("genre", True).to_csv("classification_genre_noise_test.csv", index=False)
    concat_classification_noise("genre", False).to_csv("classification_genre_noise_unseen.csv", index=False)

    pd.concat(classification_genre_test.values()).to_csv("classification_genre_test.csv", index=False)
    pd.concat(classification_genre_unseen.values()).to_csv("classification_genre_unseen.csv", index=False)
    pd.concat(classification_music_test.values()).to_csv("classification_music_test.csv", index=False)
    pd.concat(classification_music_unseen.values()).to_csv("classification_music_unseen.csv", index=False)


if __name__ == "__main__":
    main()
