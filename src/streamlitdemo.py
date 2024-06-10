import os
import tempfile
import functools as ft
import uuid

import plotly.graph_objs as go
import streamlit as st
import taglib
from sklearn.metrics import classification_report, accuracy_score, precision_score, f1_score, recall_score

from computations import Model

PLOT_HEIGHT = 400
SPLIT = "TEST"  # "TEST" or "UNSEEN"
DATASET_NAME = "v2"

# model = Model(f"../database/{DATASET_NAME}/TRAIN")
model = None


def on_audio_click(file):
    # Create a temporary directory to store the uploaded file
    temp_dir = tempfile.mkdtemp()
    sig_path = file.split("/")[-1].replace("wav", "sig")
    os.system(f"cd ../database/{DATASET_NAME}; ./params.sh -w {os.path.join(temp_dir, sig_path)} {file}")

    # Predict the genre
    st.session_state["prediction"] = model.predict(os.path.join(temp_dir, sig_path))


def get_parameters(file):
    with open(file, "r") as f:
        lines = f.readlines()
        parameters = dict()
        for line in lines:
            key, value = line.strip().split(",")
            parameters[key] = value
    return parameters


def run_all(root, report_prefix=""):
    cache = generate_detailed_report(root, report_prefix)
    Xg, Xf, yg, yf = generate_metrics_report(root, cache)
    methods = Xg.keys()
    parameters = get_parameters(f"../database/{DATASET_NAME}/params.csv")

    with open(f"results/{report_prefix}__metrics_report.md", "w") as f:
        for method in methods:
            print(f"## {method} - Genre", file=f)
            print("```", file=f)
            print(classification_report(yg[method], Xg[method]), file=f)
            print("```", file=f)

            print(f"## {method} - Name", file=f)
            print("Accuracy: ", round(sum(Xf[method]) / len(Xf[method]), ndigits=2), file=f)

    with open(f"results/{report_prefix}__classification_genre.csv", "w") as f:
        f.write("ws,ds,nf,sh,genre,precision,recall,f1-score,accuracy,methodCompression,partition\n")
        for method in methods:
            accuracy_per_genre = dict()
            precision_per_genre = dict()
            recall_per_genre = dict()
            f1_per_genre = dict()
            genres = set(yg[method])
            for genre in genres:
                accuracy_per_genre[genre] = accuracy_score(list(map(lambda x: 1 if x == genre else 0, yg[method])),
                                                           list(map(lambda x: 1 if x == genre else 0, Xg[method])))
                precision_per_genre[genre] = precision_score(yg[method], Xg[method], labels=[genre], zero_division=0,
                                                             average="macro")
                recall_per_genre[genre] = recall_score(yg[method], Xg[method], labels=[genre], zero_division=0,
                                                       average="macro")
                f1_per_genre[genre] = f1_score(yg[method], Xg[method], labels=[genre], zero_division=0, average="macro")

            for genre in genres:
                f.write(
                    f"{parameters['ws']},"
                    f"{parameters['ds']},"
                    f"{parameters['nf']},"
                    f"{parameters['sh']},"
                    f"{genre},"
                    f"{round(precision_per_genre[genre], ndigits=2)},"
                    f"{round(recall_per_genre[genre], ndigits=2)},"
                    f"{round(f1_per_genre[genre], ndigits=2)},"
                    f"{round(accuracy_per_genre[genre], ndigits=2)},"
                    f"{method[0]},"
                    f"{method[1]}\n")

    with open(f"results/{report_prefix}__classification_music.csv", "w") as f:
        f.write("ws,ds,nf,sh,accuracy,methodCompression,partition\n")
        for method in methods:
            f.write(
                f"{parameters['ws']},"
                f"{parameters['ds']},"
                f"{parameters['nf']},"
                f"{parameters['sh']},"
                f"{round(sum(Xf[method]) / len(Xf[method]), ndigits=2)},"
                f"{method[0]},"
                f"{method[1]}\n")


def generate_metrics_report(root, cache, depth=0, path=""):
    Xg = dict()
    yg = dict()
    Xf = dict()
    yf = dict()

    for node in sorted(os.listdir(root)):
        if not node.endswith(".wav") and not os.path.isdir(os.path.join(root, node)):
            continue

        if os.path.isdir(os.path.join(root, node)):
            Xg1, Xf1, yg1, yf1 = generate_metrics_report(os.path.join(root, node), cache, depth=depth + 1,
                                                         path=os.path.join(path, node))
            for key, value in Xg1.items():
                Xg.setdefault(key, list())
                Xg[key] += value

            for key, value in Xf1.items():
                Xf.setdefault(key, list())
                Xf[key] += value

            for key, value in yg1.items():
                yg.setdefault(key, list())
                yg[key] += value

            for key, value in yf1.items():
                yf.setdefault(key, list())
                yf[key] += value
        else:
            with taglib.File(os.path.join(root, node)) as f:
                genre, fname = f.tags["COMM"][0].split(";", 1)

            avg_scores, best_cases, top_cases = cache[node]
            part = path.split("/")[-1]

            for method, res in best_cases.items():
                if res is None:
                    continue
                if (method, part) not in Xg:
                    Xg[(method, part)] = list()
                    Xf[(method, part)] = list()
                    yg[(method, part)] = list()
                    yf[(method, part)] = list()

                Xg[(method, part)].append(res["genre"])
                yg[(method, part)].append(genre)
                if res["name"] != fname:
                    Xf[(method, part)].append(0)
                else:
                    Xf[(method, part)].append(1)
                yf[(method, part)].append(1)

    return Xg, Xf, yg, yf


def generate_detailed_report(root, report_prefix, depth=0, path="", cache=None):
    if cache is None:
        cache = dict()

    report = ""

    for node in sorted(os.listdir(root)):
        if not node.endswith(".wav") and not os.path.isdir(os.path.join(root, node)):
            continue

        if os.path.isdir(os.path.join(root, node)):
            report += f"# Using {float(node) * 100}% of each file\n"
            report += generate_detailed_report(os.path.join(root, node), report_prefix, depth=depth + 1,
                                               path=os.path.join(path, node),
                                               cache=cache)
        else:
            with taglib.File(os.path.join(root, node)) as f:
                genre, fname = f.tags["COMM"][0].split(";")

            temp_dir = tempfile.mkdtemp()
            sig_path = node.replace("wav", "sig")
            os.system(
                f"cd ../database/{DATASET_NAME}; ./params.sh -w {os.path.join(temp_dir, sig_path)} {SPLIT}/{os.path.join(path, node)}")

            last_results = None
            for prediction in model.predict(os.path.join(temp_dir, sig_path)):
                last_results = prediction
            avg_scores, best_cases, top_cases = last_results
            cache[node] = (avg_scores, best_cases, top_cases)

            report += f"## {node} - {genre} - {fname}\n"
            report += f"### NCD Scores\n"
            for method, genres in avg_scores.items():
                report += f"#### {method}\n"
                for genre, score in genres.items():
                    report += f"- {genre}: {score}\n"

            report += f"### Predictions\n"
            for method, result in best_cases.items():
                if result is None:
                    continue
                report += f"#### Best Case for {method}\n"
                report += f"- Genre: {result['genre']}\n"
                report += f"- Name: {result['name']}\n"

            report += f"#### Best Cases\n"
            for method, cases in top_cases.items():
                report += f"#### Top 10 Cases for {method}\n"
                for case in cases:
                    report += f"- {case[1]['genre']} - {case[1]['name']}: {case[0]}\n"

    if depth == 0:
        with open(f"{report_prefix}__report.md", "w") as f:
            f.write(report)
        return cache
    else:
        return report


def recursive_tree(root, depth=0, path=""):
    for node in sorted(os.listdir(root)):
        if node.endswith(".sig"):
            continue

        if os.path.isdir(os.path.join(root, node)):
            with st.expander(f"{node}"):
                recursive_tree(os.path.join(root, node), depth=depth + 1, path=os.path.join(path, node))
        else:
            with taglib.File(os.path.join(root, node)) as f:
                genre, fname = f.tags["COMM"][0].split(";")
            st.button(f"{node} - {genre} - {fname}", key=uuid.uuid4(),
                      on_click=ft.partial(on_audio_click, f"{SPLIT}/{os.path.join(path, node)}"))


if __name__ == "__main__":
    if model is None:
        model = Model(f"../database/{DATASET_NAME}/TRAIN")

    # Streamlit App
    st.set_page_config(page_title="TAI Assignment 3", layout="wide")
    st.title("TAI Assignment 3")

    with st.sidebar:
        st.button("Run all and create report", on_click=ft.partial(run_all, f"../database/{DATASET_NAME}/{SPLIT}"))
        recursive_tree(f"../database/{DATASET_NAME}/{SPLIT}")

    prediction_placeholders = {
        "bz2": st.empty(),
        "gzip": st.empty(),
        "lzma": st.empty(),
        "zstd": st.empty(),
        "zlib": st.empty(),
    }

    graph_grid_1 = st.columns(3)
    graph_grid_2 = st.columns(3)
    graph_placeholders = {
        "bz2": graph_grid_1[0].container(height=PLOT_HEIGHT, border=False).empty(),
        "gzip": graph_grid_1[1].container(height=PLOT_HEIGHT, border=False).empty(),
        "lzma": graph_grid_1[2].container(height=PLOT_HEIGHT, border=False).empty(),
        "zstd": graph_grid_2[0].container(height=PLOT_HEIGHT, border=False).empty(),
        "zlib": graph_grid_2[1].container(height=PLOT_HEIGHT, border=False).empty(),
    }

    top_graph_grid_1 = st.columns(3)
    top_graph_grid_2 = st.columns(3)
    top_graph_placeholders = {
        "bz2": top_graph_grid_1[0].container(height=PLOT_HEIGHT, border=False).empty(),
        "gzip": top_graph_grid_1[1].container(height=PLOT_HEIGHT, border=False).empty(),
        "lzma": top_graph_grid_1[2].container(height=PLOT_HEIGHT, border=False).empty(),
        "zstd": top_graph_grid_2[0].container(height=PLOT_HEIGHT, border=False).empty(),
        "zlib": top_graph_grid_2[1].container(height=PLOT_HEIGHT, border=False).empty(),
    }

    if "prediction" in st.session_state:
        for avg_scores, best_cases, top_cases in st.session_state["prediction"]:
            for method, result in best_cases.items():
                if result is None:
                    continue
                prediction_placeholders[method].write(
                    f"Best case for {method}: {result['genre']} - \"{result['name']}\" - {result['score']}")

            for method, genres in avg_scores.items():
                fig = go.Figure(
                    data=[go.Bar(x=list(genres.keys()), y=list(genres.values()))],
                    layout=go.Layout(title=f"Average NCD Scores for {method}", height=PLOT_HEIGHT)
                )
                graph_placeholders[method].plotly_chart(fig)

            for method, cases in top_cases.items():
                fig = go.Figure(
                    data=[go.Bar(x=[f"{case['genre']} - \"{case['name']}\"" for _, case in cases],
                                 y=[score for score, _ in cases])],
                    layout=go.Layout(title=f"Top 10 NCD Scores for {method}", height=PLOT_HEIGHT)
                )
                top_graph_placeholders[method].plotly_chart(fig)
