#!/bin/bash

SPOTIFY_DS="../datasets/dataset_spotify"

SPOTIFY_n_test_audios_genres=2
SPOTIFY_n_test_unseen_genres=2

N_TOTAL=12

CURRENT_VERSION=6

NOISE_LEVELS=(0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
BETS_WINDOW_SIZE=4096
BETS_SHIFT=1024
BETS_DOWN_SAMPLING=16
BETS_NUMBER_OF_SIGNIFICANT_FREQS=2

cd database
#rm -rf v_best_params*

for NOISE_LEVEL  in "${NOISE_LEVELS[@]}"
do
    echo "Generating data for noise level: $NOISE_LEVEL"
    python generate_data.py --dataset_dir $SPOTIFY_DS --n_test_audios_genres $SPOTIFY_n_test_audios_genres --n_test_unseen_genres $SPOTIFY_n_test_unseen_genres --n_total $N_TOTAL --noise_level $NOISE_LEVEL --version "v_best_params_$CURRENT_VERSION" --ws $BETS_WINDOW_SIZE --sh $BETS_SHIFT --ds $BETS_DOWN_SAMPLING --nf $BETS_NUMBER_OF_SIGNIFICANT_FREQS
    CURRENT_VERSION=$((CURRENT_VERSION+1))
done

