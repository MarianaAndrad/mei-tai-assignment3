import bz2
import gzip
import lzma
import os
import functools as ft

VERSION = "v1"
TEST_FOLDER = "TEST"
TRAIN_FOLDER = "TRAIN"
DATA_FOLDER = "../train_data"
PERCENT = "0.2"

@ft.lru_cache(maxsize=None)
def compress_gzip(bindata):
    return len(gzip.compress(bindata))


@ft.lru_cache(maxsize=None)
def compress_lzma(bindata):
    return len(lzma.compress(bindata))


@ft.lru_cache(maxsize=None)
def compress_bz2(bindata):
    return len(bz2.compress(bindata))


def ncd(file_a, file_b, fn):
    bin_file_a = open(file_a, 'rb').read()
    bin_file_b = open(file_b, 'rb').read()

    compress_a = fn(bin_file_a)
    compress_b = fn(bin_file_b)
    compress_ab = fn(bin_file_a + bin_file_b)

    return (compress_ab - min(compress_a, compress_b)) / max(compress_a, compress_b)


def predict(file_to_classify):
    train_folder = os.path.join(DATA_FOLDER, VERSION, TRAIN_FOLDER)
    methods = ["bz2", "gzip", "lzma"]
    scores = []

    for root, dirs, files in os.walk(train_folder):
        if len(files) == 0:
            continue

        files = list(filter(lambda x: x.endswith(".sig"), files))

        for file in files:
            file_b = os.path.join(root, file)
            scores.append({
                "file": file,
                "genre": root.split("/")[-1],
                **{method: ncd(file_to_classify, file_b, globals()[f"compress_{method}"]) for method in methods}
            })

    classifications = {}
    for method in methods:
        predicted = sorted(scores, key=lambda x: x[method])[0]
        classifications[method] = (predicted["file"].split(".")[0], predicted["genre"])
    return classifications


if __name__ == "__main__":
    test_folder = os.path.join(DATA_FOLDER, VERSION, TEST_FOLDER, PERCENT)
    hits_per_algorithm_genre = {}
    hits_per_algorithm_fname = {}
    total = 0

    for root, dirs, files in os.walk(test_folder):
        if len(files) == 0:
            continue

        files = list(filter(lambda x: x.endswith(".sig"), files))

        genre = root.split("/")[-1]
        for file in files:
            file_to_classify = os.path.join(root, file)
            total += 1
            for method, (fname_classified, genre_classified) in predict(file_to_classify).items():
                print(f"Predicted genre: {genre_classified}, Predicted file: {fname_classified} | Real genre: {genre}, Real file: {file}")
                if genre_classified == genre:
                    hits_per_algorithm_genre[method] = hits_per_algorithm_genre.get(method, 0) + 1

                if fname_classified in file:
                    hits_per_algorithm_fname[method] = hits_per_algorithm_fname.get(method, 0) + 1

    print("Hits per genre:")
    for method, hits in hits_per_algorithm_genre.items():
        print(f"{method} hit rate: {hits / total}")

    print("Hits per file:")
    for method, hits in hits_per_algorithm_fname.items():
        print(f"{method} hit rate: {hits / total}")
