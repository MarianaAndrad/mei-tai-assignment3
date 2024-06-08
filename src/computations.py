import bz2
import functools as ft
import gzip
import lzma
import os
import random
from collections import defaultdict

import joblib
import taglib

mem_location = "../cache"
memory = joblib.Memory(mem_location)


def cache_results(func):
    fn = memory.cache(func)

    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        if "no_cache" in kwargs:
            return func(*args)
        return fn(*args)

    return wrapper


@cache_results
def compress_gzip(bindata):
    return len(gzip.compress(bindata))


@cache_results
def compress_lzma(bindata):
    return len(lzma.compress(bindata))


@cache_results
def compress_bz2(bindata):
    return len(bz2.compress(bindata))


# TODO ZSTD, LZ4, ZLIB

def ncd(bin_file_a, bin_file_b, method, data, fn):
    compress_a = fn(bin_file_a)
    compress_b = fn(bin_file_b)
    compress_ab = fn(bin_file_a + bin_file_b, no_cache=True)

    return method, data, (compress_ab - min(compress_a, compress_b)) / max(compress_a, compress_b)


class Model(object):
    def __init__(self, dataset):
        self.dataset = []
        for file in os.listdir(dataset):
            if file.endswith(".sig"):
                sig = os.path.join(dataset, file)
                wav = sig.replace("sig", "wav")
                with taglib.File(wav) as f:
                    genre, fname = f.tags["COMM"][0].split(";", 1)

                self.dataset.append({
                    "data": open(sig, "rb").read(),
                    "genre": genre,
                    "name": fname
                })

        random.shuffle(self.dataset)  # provide a better ui experience, but not necessary (because genres)

    def predict(self, file_to_classify):
        methods = ["bz2", "gzip", "lzma"] # TODO ZSTD, LZ4, ZLIB
        binary_file = open(file_to_classify, "rb").read()

        gen = joblib.Parallel(n_jobs=-1, return_as="generator_unordered")(
            joblib.delayed(ncd)(binary_file, file_b["data"], method, file_b, globals()[f"compress_{method}"])
            for file_b in self.dataset
            for method in methods
        )

        """
        [method][genre][score]
        [method][genre][count]
        """
        sum_scores_per_genre = defaultdict(lambda: defaultdict(lambda: 0))
        count_scores_per_genre = defaultdict(lambda: defaultdict(lambda: 0))

        """
        [method][score]
        [method][count]
        """
        best_scores = defaultdict(lambda: float("inf"))
        best_cases = defaultdict(lambda: None)

        top_cases = defaultdict(lambda: list())

        for method, data, score in gen:
            sum_scores_per_genre[method][data["genre"]] += score
            count_scores_per_genre[method][data["genre"]] += 1

            if score < best_scores[method]:
                best_scores[method] = score
                best_cases[method] = data

            top_cases[method].append((score, data))
            top_cases[method] = sorted(top_cases[method], key=lambda x: x[0])[:10]

            avg_scores = defaultdict(lambda: defaultdict(lambda: 0.))
            for method in methods:
                for genre, score in sum_scores_per_genre[method].items():
                    avg_scores[method][genre] = score / count_scores_per_genre[method][genre]

            yield avg_scores, best_cases, top_cases
