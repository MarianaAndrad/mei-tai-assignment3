import os
import random
from collections import defaultdict

import librosa
import soundfile as sf
import numpy as np
import taglib
from tqdm import tqdm

DATASET_DIR = "../dataset"
NOISE_LEVEL = 0.3
PARTS = [0.2, 0.5, 1]
VERSION = "v2"
N_TEST_AUDIOS_GENRE = 10
N_TEST_UNSEEN_GENRES = 10


def process_audio(audio_path, noise_level):
    """Add noise to audio."""
    audio, sr = librosa.load(audio_path, mono=False, sr=44100)
    noise = np.random.normal(0, 1, audio.shape)
    scaled_noise = noise_level * noise
    augmented_audio = audio + scaled_noise
    return augmented_audio, sr


def main():
    db_count = 0
    test_count = defaultdict(lambda: 0)
    unseen_count = defaultdict(lambda: 0)

    for root, dirs, files in tqdm(os.walk(DATASET_DIR)):
        if len(files) == 0:
            continue
        genre = root.split("/")[-1]
        test_files = []  # partial audio file + noise in DB
        unseen_files = []  # partial audio file + noise not in DB
        database_files = []  # complete audio file

        for i, audio in enumerate(files):
            if i < N_TEST_AUDIOS_GENRE:
                test_files.append(audio)

            if N_TEST_AUDIOS_GENRE < i < N_TEST_UNSEEN_GENRES + N_TEST_AUDIOS_GENRE:
                unseen_files.append(audio)
            else:
                database_files.append(audio)

        # TODO COLOCAR IN ONE FUNCTION
        for percentage in PARTS:
            os.makedirs(f"./{VERSION}/TEST/{percentage}", exist_ok=True)
            for audio in test_files:
                scaled, sr = process_audio(os.path.join(root, audio), NOISE_LEVEL)
                scaled = scaled.T
                accumulated = 0
                iteration = 0
                while accumulated < len(scaled):
                    sf.write(f"./{VERSION}/TEST/{percentage}/aud{test_count[percentage]}_{iteration}.wav",
                             scaled[accumulated:accumulated + int(len(scaled) * percentage)], sr, format='wav')

                    with taglib.File(f"./{VERSION}/TEST/{percentage}/aud{test_count[percentage]}_{iteration}.wav",
                                     save_on_exit=True) as f:
                        f.tags["COMM"] = [f"{genre};{audio.split('.')[0]}"]

                    accumulated += int(len(scaled) * percentage)
                    iteration += 1

                test_count[percentage] += 1

        # TODO COLOCAR IN ONE FUNCTION
        for percentage in PARTS:
            os.makedirs(f"./{VERSION}/UNSEEN/{percentage}", exist_ok=True)
            for audio in unseen_files:
                scaled, sr = process_audio(os.path.join(root, audio), NOISE_LEVEL)
                scaled = scaled.T
                accumulated = 0
                iteration = 0
                while accumulated < len(scaled):
                    sf.write(f"./{VERSION}/UNSEEN/{percentage}/aud{unseen_count[percentage]}_{iteration}.wav",
                             scaled[accumulated:accumulated + int(len(scaled) * percentage)], sr, format='wav')

                    with taglib.File(f"./{VERSION}/UNSEEN/{percentage}/aud{unseen_count[percentage]}_{iteration}.wav",
                                     save_on_exit=True) as f:
                        f.tags["COMM"] = [f"{genre};{audio.split('.')[0]}"]

                    accumulated += int(len(scaled) * percentage)
                    iteration += 1

                unseen_count[percentage] += 1

        os.makedirs(f"./{VERSION}/TRAIN", exist_ok=True)
        for audio in database_files:
            aud, sr = librosa.load(os.path.join(root, audio), mono=False, sr=44100)
            aud = aud.T
            sf.write(f"./{VERSION}/TRAIN/aud{db_count}.wav", aud, sr, format='wav')
            os.system(
                f"../GetMaxFreqs/bin/GetMaxFreqs -w ./{VERSION}/TRAIN/aud{db_count}.sig ./{VERSION}/TRAIN/aud{db_count}.wav")

            with taglib.File(f"./{VERSION}/TRAIN/aud{db_count}.wav", save_on_exit=True) as f:
                f.tags["COMM"] = [f"{genre};{audio.split('.')[0]}"]
            db_count += 1


if __name__ == "__main__":
    main()
