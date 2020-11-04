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
    amd_fig = go.Figure()
    amd_fig.add_trace(
        go.Scatter(
            x=[x for x in range(1, 17)],
            y=[1/((1 - 0.32638) + 0.32638/n) for n in range(1, 17)],
            text=[round(1/((1 - 0.32638) + 0.32638/n), 2) for n in range(1, 17)],
            textposition="top center",
            mode='lines+markers+text',
            name='Speed up'
        )
    )

    amd_fig.update_layout(
        title={
            'text': "Ley de Amdahl",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Nº procesadores",
        yaxis_title="Speed up",
    )
    amd_fig.update_xaxes(type='category')
    amd_fig.show()


if args.type in ["color", "todo"]:
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
        hsl_fig.add_trace(go.Scatter(
            x=[i for i in range(1, len(hsl_means)+1)],
            y=hsl_means,
            mode='lines+markers',
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

        yuv_fig.add_trace(go.Scatter(
            x=[i for i in range(1, len(yuv_means)+1)],
            y=yuv_means,
            mode='lines+markers',
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

    #color_fig = go.Figure()
    #for i, f in enumerate(folder_names):
    #    color_processing = open("{}/color_time.txt".format(f))
    #    color_processing = np.asarray([
    #        float(l.split(" ")[-2])
    #        for l in color_processing.readlines()
    #    ])
    #    color_fig.add_trace(go.Scatter(
    #        x=[i for i in range(len(color_processing))],
    #        y=color_processing,
    #        mode='lines+markers',
    #        name='{} Time'.format(f.parent.stem),
    #        line=dict(color=colors[i])
    #    ))
    #    color_fig.add_trace(go.Scatter(
    #        x=[i for i in range(len(color_processing))],
    #        y=[color_processing.mean()]*len(color_processing),
    #        mode='lines',
    #        name='{} Mean'.format(f.parent.stem),
    #        line=dict(color=colors[i])
    #    ))

    #color_fig.update_layout(
    #    title={
    #        'text': "Color Time",
    #        'y':0.9,
    #        'x':0.5,
    #        'xanchor': 'center',
    #        'yanchor': 'top'
    #    },
    #    xaxis_title="Iterations",
    #    yaxis_title="Time (s)",
    #)
    #color_fig.update_xaxes(type='category')
    #color_fig.show()


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
            mode='lines+markers',
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
