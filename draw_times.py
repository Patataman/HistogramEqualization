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

if args.type in ["color", "todo"]:
    # HSL
    hsl_fig = go.Figure()
    for f in folder_names:
        hsl_processing = open("{}/hsl_processing.txt".format(f))
        hsl_processing = np.asarray([
            float(l.split(" ")[-2])
            for l in hsl_processing.readlines()
        ])
        hsl_fig.add_trace(go.Scatter(
            x=[i for i in range(len(hsl_processing))],
            y=hsl_processing,
            mode='lines+markers',
            name='{} Processing'.format(f.parent.stem))
        )

    hsl_fig.update_layout(
        title={
            'text': "HSL Processing",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Iterations",
        yaxis_title="Time (s)",
    )
    hsl_fig.update_xaxes(type='category')
    hsl_fig.show()

    # YUV
    yuv_fig = go.Figure()
    for f in folder_names:
        yuv_processing = open("{}/yuv_processing.txt".format(f))
        yuv_processing = np.asarray([
            float(l.split(" ")[-2])
            for l in yuv_processing.readlines()
        ])
        yuv_fig.add_trace(go.Scatter(
            x=[i for i in range(len(yuv_processing))],
            y=yuv_processing,
            mode='lines+markers',
            name='{} Processing'.format(f.parent.stem))
        )

    yuv_fig.update_layout(
        title={
            'text': "YUV Processing",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Iterations",
        yaxis_title="Time (s)",
    )
    yuv_fig.update_xaxes(type='category')
    yuv_fig.show()

    color_fig = go.Figure()
    for i, f in enumerate(folder_names):
        color_processing = open("{}/color_time.txt".format(f))
        color_processing = np.asarray([
            float(l.split(" ")[-2])
            for l in color_processing.readlines()
        ])
        color_fig.add_trace(go.Scatter(
            x=[i for i in range(len(color_processing))],
            y=color_processing,
            mode='lines+markers',
            name='{} Time'.format(f.parent.stem),
            line=dict(color=colors[i])
        ))
        color_fig.add_trace(go.Scatter(
            x=[i for i in range(len(color_processing))],
            y=[color_processing.mean()]*len(color_processing),
            mode='lines',
            name='{} Mean'.format(f.parent.stem),
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
        xaxis_title="Iterations",
        yaxis_title="Time (s)",
    )
    color_fig.update_xaxes(type='category')
    color_fig.show()


if args.type in ["gris", "todo"]:

    grey_proc_fig = go.Figure()
    for f in folder_names:
        grey_processing = open("{}/grey_processing.txt".format(f))
        grey_processing = np.asarray([
            float(l.split(" ")[-2])
            for l in grey_processing.readlines()
        ])
        grey_proc_fig.add_trace(go.Scatter(
            x=[i for i in range(len(grey_processing))],
            y=grey_processing,
            mode='lines+markers',
            name='{} Processing'.format(f.parent.stem))
        )

    grey_proc_fig.update_layout(
        title={
            'text': "Greyscale Processing",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Iterations",
        yaxis_title="Time (s)",
    )
    grey_proc_fig.update_xaxes(type='category')
    grey_proc_fig.show()

    grey_fig = go.Figure()
    for i, f in enumerate(folder_names):
        grey_processing = open("{}/grey_time.txt".format(f))
        grey_processing = np.asarray([
            float(l.split(" ")[-2])
            for l in grey_processing.readlines()
        ])
        grey_fig.add_trace(go.Scatter(
            x=[i for i in range(len(grey_processing))],
            y=grey_processing,
            mode='lines+markers',
            name='{} Time'.format(f.parent.stem),
            line=dict(color=colors[i])
        ))
        grey_fig.add_trace(go.Scatter(
            x=[i for i in range(len(grey_processing))],
            y=[grey_processing.mean()]*len(grey_processing),
            mode='lines',
            name='{} Mean'.format(f.parent.stem),
            line=dict(color=colors[i])
        ))

    grey_fig.update_layout(
        title={
            'text': "Greyscale Time",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Iterations",
        yaxis_title="Time (s)",
    )
    grey_fig.update_xaxes(type='category')
    grey_fig.show()
