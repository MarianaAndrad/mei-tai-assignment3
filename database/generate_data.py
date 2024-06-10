import os
import stat
from collections import defaultdict

import click
import librosa
import soundfile as sf
import numpy as np
import taglib
from tqdm import tqdm


def template(ws, sh, ds, nf):
    return f"""#!/bin/bash

../../GetMaxFreqs/bin/GetMaxFreqs  -ws {ws} -sh {sh} -ds {ds} -nf {nf} $@
"""


def process_audio(audio_path, noise_level):
    """Add noise to audio."""
    audio, sr = librosa.load(audio_path, mono=False, sr=44100)
    noise = np.random.normal(0, 1, audio.shape)
    scaled_noise = noise_level * noise
    augmented_audio = audio + scaled_noise
    return augmented_audio, sr


def split_test(test_files, percentages, root, noise_level, version, genre, count, type_str):
    for percentage in percentages:
        os.makedirs(f"./{version}/{type_str}/{percentage}", exist_ok=True)
        for audio in test_files:
            scaled, sr = process_audio(os.path.join(root, audio), noise_level)
            scaled = scaled.T
            accumulated = 0
            iteration = 0
            while accumulated < len(scaled):
                sf.write(f"./{version}/{type_str}/{percentage}/aud{count[percentage]}_{iteration}.wav",
                         scaled[accumulated:accumulated + int(len(scaled) * percentage)], sr, format='wav')

                with taglib.File(f"./{version}/{type_str}/{percentage}/aud{count[percentage]}_{iteration}.wav",
                                 save_on_exit=True) as f:
                    f.tags["COMM"] = [f"{genre};{audio.split('.')[0]}"]

                accumulated += int(len(scaled) * percentage)
                iteration += 1

            count[percentage] += 1


def split_train(version, database_files, root, db_count, genre):
    os.makedirs(f"./{version}/TRAIN", exist_ok=True)
    for audio in database_files:
        aud, sr = librosa.load(os.path.join(root, audio), mono=False, sr=44100)
        aud = aud.T
        sf.write(f"./{version}/TRAIN/aud{db_count}.wav", aud, sr, format='wav')
        os.system(
            f"cd ./{version}; ./params.sh -w ../../database/{version}/TRAIN/aud{db_count}.sig ../../database/{version}/TRAIN/aud{db_count}.wav")

        with taglib.File(f"./{version}/TRAIN/aud{db_count}.wav", save_on_exit=True) as f:
            f.tags["COMM"] = [f"{genre};{audio.split('.')[0]}"]
        db_count += 1


@click.command()
@click.option("--noise_level", default=0.3, help="Noise level to add to audio.")
@click.option("--n_test_audios_genres", default=10, help="Number of test audios per genre.")
@click.option("--n_test_unseen_genres", default=10, help="Number of test audios per unseen genre.")
@click.option("--n_total", default=-1, help="Total number of musics to consider per genre.")
@click.option("--version", default="v0", help="Version of the dataset.")
@click.option("--dataset_dir", default="../datasets/dataset_youmusic", help="Path to the dataset.")
@click.option("--ws", default=1024, help="Window size.")  # Size of the window for computing the FFT
@click.option("--sh", default=256, help="shift.")  # Window overlap
@click.option("--ds", default=4, help="Downsampling.")  # Down sampling factor
@click.option("--nf", default=4, help="nFreqs.")  # Number of  significant frequencies
def main(noise_level, n_test_audios_genres, n_test_unseen_genres, n_total, version, dataset_dir, ws, sh, ds, nf):
    parts = [0.2, 0.5, 1]
    db_count = 0
    test_count = defaultdict(lambda: 0)
    unseen_count = defaultdict(lambda: 0)

    os.mkdir(f"./{version}")
    with open(f"./{version}/params.csv", "w") as f:
        f.write("Parameter,Value\n")
        f.write(f"ws,{ws}\n")
        f.write(f"sh,{sh}\n")
        f.write(f"ds,{ds}\n")
        f.write(f"nf,{nf}\n")
        f.write(f"noise_level,{noise_level}\n")

    with open(f"./{version}/params.sh", "w") as f:
        f.write(template(ws, sh, ds, nf))

    st = os.stat(f"./{version}/params.sh")
    os.chmod(f"./{version}/params.sh", st.st_mode | stat.S_IEXEC)

    for root, dirs, files in tqdm(os.walk(dataset_dir)):
        if len(files) == 0:
            continue
        genre = root.split("/")[-1]
        test_files = []  # partial audio file + noise in DB
        unseen_files = []  # partial audio file + noise not in DB
        database_files = []  # complete audio file

        for i, audio in enumerate(files):
            if n_total != -1 and i == n_total:
                break

            if i < n_test_audios_genres:
                test_files.append(audio)

            if n_test_audios_genres < i < n_test_unseen_genres + n_test_audios_genres:
                unseen_files.append(audio)
            else:
                database_files.append(audio)

        split_train(version, database_files, root, db_count, genre)
        split_test(test_files, parts, root, noise_level, version, genre, test_count, type_str="TEST")
        split_test(unseen_files, parts, root, noise_level, version, genre, unseen_count, type_str="UNSEEN")
        db_count += len(database_files)


if __name__ == "__main__":
    main()
