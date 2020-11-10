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
parser.add_argument('--type', required=True, type=str, help='Tipo de gráfica [color, gris, todo]')

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

        max_iter = 17 if f.parent.stem == "OpenMP" else 9
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

        if f.parent.stem == "MPI":
            pass

        if f.parent.stem == "OpenMP":
            omp_means = []
            for it in f.iterdir():
                omp_time_grey = open("{}/grey_time.txt".format(it))
                omp_time_color = open("{}/color_time.txt".format(it))

                omp_means.append(
                    np.asarray([
                        float(l.split(" ")[-2])
                        for l in omp_time_grey.readlines()
                    ]).mean() + np.asarray([
                        float(l.split(" ")[-2])
                        for l in omp_time_color.readlines()
                    ]).mean()
                )

            amd_fig.add_trace(go.Scatter(
                x=[i for i in range(1, max_iter)],
                y=(np.asarray(original_mean)/np.asarray(omp_means)).tolist(),
                text=[round(i,2) for i in (np.asarray(original_mean)/np.asarray(omp_means)).tolist()],
                textposition="top center",
                mode='lines+markers+text',
                name='{} OMP I/O'.format(f.parent.stem))
            )

            fake_omp_means = []
            for it in f.iterdir():
                omp_proc_grey = open("{}/grey_processing.txt".format(it))
                omp_proc_hsv = open("{}/hsl_processing.txt".format(it))
                omp_proc_yuv = open("{}/yuv_processing.txt".format(it))

                fake_omp_means.append(
                    np.asarray([
                        float(l.split(" ")[-2])
                        for l in omp_proc_grey.readlines()
                    ]).mean() + np.asarray([
                        float(l.split(" ")[-2])
                        for l in omp_proc_hsv.readlines()
                    ]).mean() + np.asarray([
                        float(l.split(" ")[-2])
                        for l in omp_proc_yuv.readlines()
                    ]).mean()
                )

            amd_fig.add_trace(go.Scatter(
                x=[i for i in range(1, max_iter)],
                y=(np.asarray(fake_mean)/np.asarray(fake_omp_means)).tolist(),
                text=[round(i,2) for i in (np.asarray(fake_mean)/np.asarray(fake_omp_means)).tolist()],
                textposition="top center",
                mode='lines+markers+text',
                name='{} OMP NO I/O'.format(f.parent.stem))
            )

        if f.stem == "Combinado":
            pass

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

        amd_fig.write_image("amdalh_omp_todo.svg")
        # amd_fig.write_image("amdalh_omp_IO.svg")
        # amd_fig.write_image("amdalh_omp_no_IO.svg")


if args.type in ["color", "todo"]:
    color_processing = {f.parent.stem: {} for f in folder_names}
    # HSL
    hsl_fig = go.Figure()
    for folder in folder_names:
        hsl_means = []
        for it in folder.iterdir():
            hsl_processing = open("{}/hsl_processing.txt".format(it))
            hsl_means.append(
                np.asarray([
                    float(l.split(" ")[-2])
                    for l in hsl_processing.readlines()
                ]).mean()
            )

        color_processing[folder.parent.stem]['hsl'] = hsl_means[:]
        hsl_fig.add_trace(go.Scatter(
            x=[i for i in range(1, len(hsl_means)+1)],
            y=hsl_means,
            text=[round(i,2) for i in hsl_means],
            textposition="top center",
            mode='lines+markers+text',
            name='{} Processing'.format(folder.parent.stem))
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
    hsl_fig.write_image("omp_hsl_proc.svg")
    # YUV
    yuv_fig = go.Figure()
    for folder in folder_names:
        yuv_means = []
        for it in folder.iterdir():
            yuv_processing = open("{}/yuv_processing.txt".format(it))
            yuv_means.append(
                np.asarray([
                    float(l.split(" ")[-2])
                    for l in yuv_processing.readlines()
                ]).mean()
            )

        color_processing[folder.parent.stem]['yuv'] = yuv_means[:]
        yuv_fig.add_trace(go.Scatter(
            x=[i for i in range(1, len(yuv_means)+1)],
            y=yuv_means,
            text=[round(i,2) for i in yuv_means],
            textposition="top center",
            mode='lines+markers+text',
            name='{} Processing'.format(folder.parent.stem))
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
    yuv_fig.write_image("omp_yuv_proc.svg")

    color_fig = go.Figure()
    for i, f in enumerate(folder_names):
        total = np.array(
            color_processing[f.parent.stem]['hsl']
        ) +  np.array(
            color_processing[f.parent.stem]['yuv']
        )
        color_fig.add_trace(go.Scatter(
            x=[i for i in range(1, len(total)+1)],
            y=total.tolist(),
            text=[round(i,2) for i in total],
            textposition="top center",
            mode='lines+markers+text',
            name='{} Time'.format(f.parent.stem),
            line=dict(color=colors[i])
        ))

    color_fig.update_layout(
        title={
            'text': "Color Time",
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
    color_fig.write_image("omp_color_total.svg")


if args.type in ["gris", "todo"]:

    grey_fig = go.Figure()
    for folder in folder_names:
        grey_means = []
        for it in folder.iterdir():
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
            name='{} Processing'.format(folder.parent.stem))
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
    grey_fig.write_image("omp_grey.svg")
