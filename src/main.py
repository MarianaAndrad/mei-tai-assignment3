import gzip
import lzma
import bz2
import functools as ft
import os
from pprint import pp


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


def main():
    file_to_classify = "../0.sig"
    methods = ["gzip", "lzma", "bz2"]

    scores = []

    for file in os.listdir("../train_data"):
        if file.endswith(".sig"):
            file_b = f"../train_data/{file}"

            scores.append({
                "file": file,
                **{method: ncd(file_to_classify, file_b, globals()[f"compress_{method}"]) for method in methods}
            })

    classifications = {}
    for method in methods:
        classifications[method] = sorted(scores, key=lambda x: x[method])[0]["file"]
    pp(classifications)


if __name__ == '__main__':
    main()
