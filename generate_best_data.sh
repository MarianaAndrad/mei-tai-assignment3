#!/bin/bash

SPOTIFY_DS="./datasets/dataset_spotify"

SPOTIFY_n_test_audios_genres=10
SPOTIFY_n_test_unseen_genres=10

N_TOTAL=25

CURRENT_VERSION=0

NOISE_LEVELS=(0.0 0.1 0.15 0.2 0.25 0.3 0.5)
BETS_WINDOW_SIZE=4096
BETS_SHIFT=1024
BETS_DOWN_SAMPLING=1
BETS_NUMBER_OF_SIGNIFICANT_FREQS=64

cd database
rm -rf v_*

for NOISE_LEVEL  in "${NOISE_LEVELS[@]}"
do
    echo "Generating data for noise level: $NOISE_LEVEL"
    python database/generate_data.py --dataset_dir $SPOTIFY_DS --n_test_audios_genres $SPOTIFY_n_test_audios_genres --n_test_unseen_genres $SPOTIFY_n_test_unseen_genres --n_total $N_TOTAL --noise_level $NOISE_LEVEL --version "v_$CURRENT_VERSION" --ws $BETS_WINDOW_SIZE --sh $BETS_SHIFT --ds $BETS_DOWN_SAMPLING --nof $BETS_NUMBER_OF_SIGNIFICANT_FREQS
    CURRENT_VERSION=$((CURRENT_VERSION+1))
done

