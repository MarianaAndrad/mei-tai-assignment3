import os
from pprint import pp

import matplotlib.pyplot as plt
import seaborn as sns
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
        version = int(file.split("_")[0][1:])
        print(version)
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


def concat_results():
    return concat_classification_results("genre", True), concat_classification_results("music", True), \
    concat_classification_results("genre", False), concat_classification_results("music", False)


def plot_noise_level_algorithm(classification, partition, save=False):
    # plot x = noise level, y = accuracy for each algorithm
    algorithms = classification["ds"]["methodCompression"].unique()
    metrics = ["accuracy"]

    # Plot each parameter
    fig = plt.figure(figsize=(15, 10))
    axs = fig.add_subplot(111)

    for alg in algorithms:
        data = classification["ds"]
        data = data[data["partition"] == partition]
        data = data[data["methodCompression"] == alg]
        data = data.sort_values(by="noiseLevel")
        axs.plot(data["noiseLevel"], data["accuracy"], label=alg, marker="o")

    axs.set_title(f"Accuracy per noise level")
    axs.set_xlabel("Noise Level")
    axs.set_ylabel("Accuracy")
    axs.legend()

    plt.tight_layout()

    if save:
        plt.savefig(f"plots/noise_level_algorithm_{partition}.png")
        plt.close()
    else:
        plt.show()


def plot_music_algorithm_per_parameter(classification_music, partition, save=False, test=True):
    algorithms = classification_music["ds"]["methodCompression"].unique()
    parameters = ["ws", "ds", "nf", "sh"]

    # Plot each parameter
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Grid of 2x2 for each metric
    axs = axs.flatten()  # Flatten to make indexing easier

    for i, param in enumerate(parameters):
        # Filter the data for the parameter
        data = classification_music[param]
        data = data[data["partition"] == partition]

        # Plot each algorithm
        for alg in algorithms:
            data_alg = data[data["methodCompression"] == alg]
            data_alg = data_alg.sort_values(by=param)

            # sns.lineplot(x=param, y="accuracy", data=data_alg, label=alg, ax=axs[i], marker="o")
            axs[i].plot(data_alg[param], data_alg["accuracy"], label=alg, marker="o")

        axs[i].set_title(f"Accuracy per {param}")
        axs[i].set_xlabel(param)
        axs[i].set_xscale('log', base=2)
        axs[i].set_ylabel("Accuracy")
        axs[i].legend()

    plt.tight_layout()

    if save:
        plt.savefig(f"plots/music_algorithm_per_parameter_{partition}_{'test' if test else 'unseen'}.png")
        plt.close()
    else:
        plt.show()


def plot_genre(classification_genre, partition, genre, param, save=False, test=True):
    algorithms = classification_genre[param]["methodCompression"].unique()
    metrics = ["accuracy", "f1-score", "precision", "recall"]

    # Plot each parameter
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Grid of 2x2 for each metric
    axs = axs.flatten()  # Flatten to make indexing easier

    for i, metric in enumerate(metrics):
        data = classification_genre[param]
        data = data[data["partition"] == partition]
        data = data[data["genre"] == genre]

        for alg in algorithms:
            data_alg = data[data["methodCompression"] == alg]
            data_alg = data_alg.sort_values(by=param)

            axs[i].plot(data_alg[param], data_alg[metric], label=alg, marker="o")

        axs[i].set_title(f"{metric} per {param}")
        axs[i].set_xlabel(param)
        axs[i].set_xscale('log', base=2)
        axs[i].set_ylabel(metric)
        axs[i].legend()

    plt.tight_layout()

    if save:
        plt.savefig(f"plots/genre_{genre}_per_parameter_{partition}_{param}_{'test' if test else 'unseen'}.png")
        plt.close()
    else:
        plt.show()


def main():
    partition_list = [0.2, 0.5, 1]
    classification_genre_test, classification_music_test, classification_genre_unseen, classification_music_unseen = concat_results()
    genres = classification_genre_test["ds"]["genre"].unique()
    param = ["ws", "ds", "nf", "sh"]
    for part in partition_list:
        plot_music_algorithm_per_parameter(classification_music_test, part, save=True)
        plot_music_algorithm_per_parameter(classification_music_unseen, part, save=True, test=False)
        for genre in genres:
            for p in param:
                plot_genre(classification_genre_test, part, genre, p, save=True)
                plot_genre(classification_genre_unseen, part, genre, p, save=True, test=False)


if __name__ == "__main__":
    main()
