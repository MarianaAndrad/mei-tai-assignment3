#!/bin/bash

SPOTIFY_DS="../datasets/dataset_spotify"

SPOTIFY_n_test_audios_genres=2
SPOTIFY_n_test_unseen_genres=2

N_TOTAL=12

CURRENT_VERSION=0

NOISE_LEVEL=0.0
WINDOW_SIZES=(1024 2048 4096 8192 16384 32768 65536)
SHIFTS=(256 512 1024 2048 4096 8192 16384 32768)
DOWN_SAMPLINGS=(1 2 4 8 16 32 64 128 256)
NUMBER_OF_SIGNIFICANT_FREQS=(1 2 4 8 16 32 64 128 256)

cd database
#rm -rf v*

for ws  in "${WINDOW_SIZES[@]}"
do
    echo "Generating data for window size: $ws"
    python generate_data.py --dataset_dir $SPOTIFY_DS --n_test_audios_genres $SPOTIFY_n_test_audios_genres --n_test_unseen_genres $SPOTIFY_n_test_unseen_genres --n_total $N_TOTAL --noise_level $NOISE_LEVEL --version "v$CURRENT_VERSION" --ws $ws &
    CURRENT_VERSION=$((CURRENT_VERSION+1))
done
wait


for shift  in "${SHIFTS[@]}"
do
    echo "Generating data for shift: $shift"
    python generate_data.py --dataset_dir $SPOTIFY_DS --n_test_audios_genres $SPOTIFY_n_test_audios_genres --n_test_unseen_genres $SPOTIFY_n_test_unseen_genres --n_total $N_TOTAL --noise_level $NOISE_LEVEL --version "v$CURRENT_VERSION" --sh $shift &
    CURRENT_VERSION=$((CURRENT_VERSION+1))
done
wait

for ds in "${DOWN_SAMPLINGS[@]}"
do
  echo "Generating data for down sampling: $ds"
  python generate_data.py --dataset_dir $SPOTIFY_DS --n_test_audios_genres $SPOTIFY_n_test_audios_genres --n_test_unseen_genres $SPOTIFY_n_test_unseen_genres --n_total $N_TOTAL --noise_level $NOISE_LEVEL --version "v$CURRENT_VERSION" --ds $ds &
  CURRENT_VERSION=$((CURRENT_VERSION+1))
done
wait

for nf in "${NUMBER_OF_SIGNIFICANT_FREQS[@]}"
do
  echo "Generating data for number of significant frequencies: $nf"
  python generate_data.py --dataset_dir $SPOTIFY_DS --n_test_audios_genres $SPOTIFY_n_test_audios_genres --n_test_unseen_genres $SPOTIFY_n_test_unseen_genres --n_total $N_TOTAL --noise_level $NOISE_LEVEL --version "v$CURRENT_VERSION" --nf $nf &
  CURRENT_VERSION=$((CURRENT_VERSION+1))
done
wait
