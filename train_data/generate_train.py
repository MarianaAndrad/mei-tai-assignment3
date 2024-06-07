import os
import random

import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm

DATASET_DIR = "../dataset/"
NOISE_LEVEL = 0.3
PARTS = [0.2, 0.5, 1]
VERSION = "v1"
N_TEST_AUDIOS_GENRE = 2


def process_audio(audio_path, noise_level):
    audio, sr = librosa.load(audio_path, mono=False, sr=44100)
    noise = np.random.normal(0, 1, audio.shape)
    scaled_noise = noise_level * noise
    augmented_audio = audio + scaled_noise
    return augmented_audio, sr


def main():
    for root, dirs, files in tqdm(os.walk(DATASET_DIR)):
        if len(files) == 0:
            continue
        genre = root.split("/")[-1]
        test_files = []
        train_files = []
        random.shuffle(files)
        for i, audio in enumerate(files):
            if i < N_TEST_AUDIOS_GENRE:
                test_files.append(audio)
            train_files.append(audio)

        for percentage in PARTS:
            os.makedirs(f"./{VERSION}/TEST/{percentage}/{genre}")
            for i, audio in enumerate(test_files):
                scaled, sr = process_audio(os.path.join(root, audio), NOISE_LEVEL)
                scaled = scaled.T
                accumulated = 0
                iteration = 0
                while accumulated < len(scaled):
                    sf.write(f"./{VERSION}/TEST/{percentage}/{genre}/aud{i}_{iteration}.wav",
                             scaled[accumulated:accumulated + int(len(scaled) * percentage)], sr, format='wav')
                    os.system(
                        f"../GetMaxFreqs/bin/GetMaxFreqs -w ./{VERSION}/TEST/{percentage}/{genre}/sig{i}_{iteration}.sig ./{VERSION}/TEST/{percentage}/{genre}/aud{i}_{iteration}.wav")

                    accumulated += int(len(scaled) * percentage)
                    iteration += 1

        os.makedirs(f"./{VERSION}/TRAIN/{genre}")
        for i, audio in enumerate(train_files):
            aud, sr = librosa.load(os.path.join(root, audio), mono=False, sr=44100)
            aud = aud.T
            sf.write(f"./{VERSION}/TRAIN/{genre}/aud{i}.wav", aud, sr, format='wav')
            os.system(f"../GetMaxFreqs/bin/GetMaxFreqs -w ./{VERSION}/TRAIN/{genre}/sig{i}.sig ./{VERSION}/TRAIN/{genre}/aud{i}.wav")


if __name__ == "__main__":
    main()
