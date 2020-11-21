from pathlib import Path

import argparse
import numpy as np
import plotly.graph_objects as go

colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

parser = argparse.ArgumentParser(description='Draw grafiquitas.')
parser.add_argument('--folder', nargs='+', required=True, type=str, help='Nombre de la carpeta [OpenMP, Original, MPI, Combinado]')
parser.add_argument('--type', required=True, type=str, help='Tipo de gráfica [color, gris, todo, speed]')

args = parser.parse_args()

folder_names = [Path("{}/times".format(folder)) for folder in args.folder]

if args.type in ["speed"]:
    # Coge los tiempos del original para poder comparar
    # Gris + Color
    original_processing_grey = open("Original/times/1/grey_processing.txt")
    original_processing_hsl = open("Original/times/1/hsl_processing.txt")
    original_processing_yuv = open("Original/times/1/yuv_processing.txt")
    fake_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in original_processing_grey.readlines()
    ]).mean() + np.asarray([
        float(l.split(" ")[-2])
        for l in original_processing_hsl.readlines()
    ]).mean() + np.asarray([
        float(l.split(" ")[-2])
        for l in original_processing_yuv.readlines()
    ]).mean()

    original_time_grey = open("Original/times/1/grey_time.txt")
    original_time_color = open("Original/times/1/color_time.txt")
    original_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in original_time_grey.readlines()
    ]).mean() + np.asarray([
        float(l.split(" ")[-2])
        for l in original_time_color.readlines()
    ]).mean()

    for f in folder_names:
        if f.parent.stem == "Original":
            continue

        amd_fig = go.Figure()

        max_iter = 9
        amd_teorico = [1/((1 - 0.32638) + 0.32638/n) for n in range(1, max_iter)]

        # Teórico
        amd_fig.add_trace(
            go.Scatter(
                x=[x for x in range(1, max_iter)],
                y=amd_teorico,
                text=[round(1/((1 - 0.32638) + 0.32638/n), 2) for n in range(1, max_iter)],
                textposition="top center",
                mode='lines+markers+text',
                name='Perfect Speed up'
            )
        )

        if f.parent.stem == "Combinado":
            # Tiene que calcular N gráficas (por carpeta) con Y (subcarpetas) en el eje X
            for n in f.iterdir():
                comb_means = []
                for it in sorted([it for it in n.iterdir()]):
                    comb_time_grey = open("{}/grey_time.txt".format(it))
                    comb_time_color = open("{}/color_time.txt".format(it))

                    comb_means.append(
                        np.asarray([
                            float(l.split(" ")[-2])
                            for l in comb_time_grey.readlines()
                        ]).mean() + np.asarray([
                            float(l.split(" ")[-2])
                            for l in comb_time_color.readlines()
                        ]).mean()
                    )

                amd_fig.add_trace(go.Scatter(
                    x=[i for i in range(1, max_iter)],
                    y=(np.asarray(original_mean)/np.asarray(comb_means)).tolist(),
                    text=[round(i,2) for i in (np.asarray(original_mean)/np.asarray(comb_means)).tolist()],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={} I/O'.format(n.stem))
                )

                fake_comb_means = []
                for it in sorted([it for it in n.iterdir()]):
                    comb_proc_grey = open("{}/grey_processing.txt".format(it))
                    comb_proc_hsv = open("{}/hsl_processing.txt".format(it))
                    comb_proc_yuv = open("{}/yuv_processing.txt".format(it))

                    fake_comb_means.append(
                        np.asarray([
                            float(l.split(" ")[-2])
                            for l in comb_proc_grey.readlines()
                        ]).mean() + np.asarray([
                            float(l.split(" ")[-2])
                            for l in comb_proc_hsv.readlines()
                        ]).mean() + np.asarray([
                            float(l.split(" ")[-2])
                            for l in comb_proc_yuv.readlines()
                        ]).mean()
                    )

                amd_fig.add_trace(go.Scatter(
                    x=[i for i in range(1, max_iter)],
                    y=(np.asarray(fake_mean)/np.asarray(fake_comb_means)).tolist(),
                    text=[round(i,2) for i in (np.asarray(fake_mean)/np.asarray(fake_comb_means)).tolist()],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={} NO I/O'.format(n.stem))

                )

        amd_fig.update_layout(
            title={
                'text': "Amdahl's Law",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Num processors",
            yaxis_title="Speed up",
        )
        amd_fig.update_xaxes(type='category')
        amd_fig.show()

        amd_fig.write_image("amdalh_comb_todo.svg")


if args.type in ["color", "todo"]:
    original_hsl = open("Original/times/1/hsl_processing.txt")
    original_hsl_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in original_hsl.readlines()
    ]).mean()
    original_yuv = open("Original/times/1/yuv_processing.txt")
    original_yuv_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in original_yuv.readlines()
    ]).mean()
    fake_mean = original_hsl_mean + original_yuv_mean
    original_time_color = open("Original/times/1/color_time.txt")
    original_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in original_time_color.readlines()
    ]).mean()

    # HSL
    hsl_fig = go.Figure()
    for folder in folder_names:
        if folder.parent.stem == "Combinado":
            # Tiene que calcular N gráficas (por carpeta) con Y (subcarpetas) en el eje X
            for n in folder.iterdir():
                hsl_means = []
                for it in sorted([it for it in n.iterdir()]):
                    hsl_processing = open("{}/hsl_processing.txt".format(it))
                    hsl_means.append(
                        np.asarray([
                            float(l.split(" ")[-2])
                            for l in hsl_processing.readlines()
                        ]).mean()
                    )

                hsl_fig.add_trace(go.Scatter(
                    x=[i for i in range(1, len(hsl_means)+1)],
                    y=hsl_means,
                    text=[round(i,2) for i in hsl_means],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={}'.format(n.stem))
                )

    hsl_fig.add_trace(go.Scatter(
        x=[i for i in range(1, len(hsl_means)+1)],
        y=[round(original_hsl_mean, 2)]*len(hsl_means),
        text=[round(original_hsl_mean, 2)]*len(hsl_means),
        textposition="top center",
        mode='lines+markers+text',
        name='Original')
    )

    hsl_fig.update_layout(
        title={
            'text': "HSL Processing",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Num. Threads",
        yaxis_title="Time (s)",
    )
    hsl_fig.update_xaxes(type='category')
    hsl_fig.show()
    hsl_fig.write_image("comb_hsl_proc.svg")
    # YUV
    yuv_fig = go.Figure()

    for folder in folder_names:
        if folder.parent.stem == "Combinado":
            # Tiene que calcular N gráficas (por carpeta) con Y (subcarpetas) en el eje X
            for n in folder.iterdir():
                yuv_means = []
                for it in sorted([it for it in n.iterdir()]):
                    yuv_processing = open("{}/yuv_processing.txt".format(it))
                    yuv_means.append(
                        np.asarray([
                            float(l.split(" ")[-2])
                            for l in yuv_processing.readlines()
                        ]).mean()
                    )

                yuv_fig.add_trace(go.Scatter(
                    x=[i for i in range(1, len(yuv_means)+1)],
                    y=yuv_means,
                    text=[round(i,2) for i in yuv_means],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={}'.format(n.stem))
                )

    yuv_fig.add_trace(go.Scatter(
        x=[i for i in range(1, len(yuv_means)+1)],
        y=[round(original_yuv_mean, 2)]*len(yuv_means),
        text=[round(original_yuv_mean, 2)]*len(yuv_means),
        textposition="top center",
        mode='lines+markers+text',
        name='Original')
    )

    yuv_fig.update_layout(
        title={
            'text': "YUV Processing",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Num. Threads",
        yaxis_title="Time (s)",
    )
    yuv_fig.update_xaxes(type='category')
    yuv_fig.show()
    yuv_fig.write_image("comb_yuv_proc.svg")

    color_fig = go.Figure()
    for i, f in enumerate(folder_names):
        if f.parent.stem == "Combinado":
            # Tiene que calcular N gráficas (por carpeta) con Y (subcarpetas) en el eje X
            for n in f.iterdir():
                color_means = []
                for it in sorted([it for it in n.iterdir()]):
                    color_time = open("{}/color_time.txt".format(it))
                    color_means.append(
                        np.asarray([
                            float(l.split(" ")[-2])
                            for l in color_time.readlines()
                        ]).mean()
                    )

                color_fig.add_trace(go.Scatter(
                    x=[i for i in range(1, len(color_means)+1)],
                    y=color_means,
                    text=[round(i,2) for i in color_means],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={}'.format(n.stem))
                )

    color_fig.add_trace(go.Scatter(
        x=[i for i in range(1, len(color_means)+1)],
        y=[round(original_mean, 2)]*len(color_means),
        text=[round(original_mean, 2)]*len(color_means),
        textposition="top center",
        mode='lines+markers+text',
        name='Original')
    )

    color_fig.update_layout(
        title={
            'text': "Color Time I/O",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Num. Threads",
        yaxis_title="Time (s)",
    )
    color_fig.update_xaxes(type='category')
    color_fig.show()
    color_fig.write_image("comb_color_total.svg")


if args.type in ["gris", "todo"]:
    original_gris = open("Original/times/1/grey_processing.txt")
    original_gris_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in original_gris.readlines()
    ]).mean()
    original_time_gris = open("Original/times/1/grey_time.txt")
    original_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in original_time_gris.readlines()
    ]).mean()

    grey_fig = go.Figure()
    for f in folder_names:
        if f.parent.stem == "Combinado":
            # Tiene que calcular N gráficas (por carpeta) con Y (subcarpetas) en el eje X
            for n in f.iterdir():
                grey_means = []
                for it in sorted([it for it in n.iterdir()]):
                    grey_processing = open("{}/grey_processing.txt".format(it))
                    grey_means.append(
                        np.asarray([
                            float(l.split(" ")[-2])
                            for l in grey_processing.readlines()
                        ]).mean()
                    )
                grey_fig.add_trace(go.Scatter(
                    x=[i for i in range(1, len(grey_means)+1)],
                    y=grey_means,
                    text=[round(i,2) for i in grey_means],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={}'.format(n.stem))
                )

    grey_fig.add_trace(go.Scatter(
        x=[i for i in range(1, len(grey_means)+1)],
        y=[round(original_gris_mean, 2)]*len(grey_means),
        text=[round(original_gris_mean, 2)]*len(grey_means),
        textposition="top center",
        mode='lines+markers+text',
        name='Original')
    )

    grey_fig.update_layout(
        title={
            'text': "Greyscale Processing",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Num. Threads",
        yaxis_title="Time (s)",
    )
    grey_fig.update_xaxes(type='category')
    grey_fig.show()
    grey_fig.write_image("comb_proc_grey.svg")

    total_grey_fig = go.Figure()
    for f in folder_names:
        if f.parent.stem == "Combinado":
            # Tiene que calcular N gráficas (por carpeta) con Y (subcarpetas) en el eje X
            for n in f.iterdir():
                total_grey_means = []
                for it in sorted([it for it in n.iterdir()]):
                    grey_time = open("{}/grey_time.txt".format(it))
                    total_grey_means.append(
                        np.asarray([
                            float(l.split(" ")[-2])
                            for l in grey_time.readlines()
                        ]).mean()
                    )
                total_grey_fig.add_trace(go.Scatter(
                    x=[i for i in range(1, len(total_grey_means)+1)],
                    y=total_grey_means,
                    text=[round(i,2) for i in total_grey_means],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={}'.format(n.stem))
                )

    total_grey_fig.add_trace(go.Scatter(
        x=[i for i in range(1, len(total_grey_means)+1)],
        y=[round(original_mean, 2)]*len(total_grey_means),
        text=[round(original_mean, 2)]*len(total_grey_means),
        textposition="top center",
        mode='lines+markers+text',
        name='Original')
    )

    total_grey_fig.update_layout(
        title={
            'text': "Greyscale Time I/O",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Num. Threads",
        yaxis_title="Time (s)",
    )
    total_grey_fig.update_xaxes(type='category')
    total_grey_fig.show()
    total_grey_fig.write_image("comb_grey_total.svg")
