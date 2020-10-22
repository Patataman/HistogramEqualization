from pathlib import Path

import argparse
import numpy as np
import plotly.graph_objects as go


parser = argparse.ArgumentParser(description='Draw grafiquitas.')
parser.add_argument('--folder', required=True, type=str, help='Nombre de la carpeta [OpenMP, Original, MPI, Combinado]')
parser.add_argument('--type', required=True, type=str, help='Tipo de gráfica [color, gris, todo]')

args = parser.parse_args()


folder_name = Path("{}/times".format(args.folder))

if args.type in ["color", "todo"]:
    # HSL
    hsl_processing = open("{}/hsl_processing.txt".format(folder_name))
    hsl_processing = np.asarray([
        float(l.split(" ")[-2])
        for l in hsl_processing.readlines()
    ])
    # YUV
    yuv_processing = open("{}/yuv_processing.txt".format(folder_name))
    yuv_processing = np.asarray([
        float(l.split(" ")[-2])
        for l in yuv_processing.readlines()
    ])
    # Color
    color_time = open("{}/color_time.txt".format(folder_name))
    color_time = np.asarray([
        float(l.split(" ")[-2])
        for l in color_time.readlines()
    ])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[i for i in range(len(color_time))], y=hsl_processing,
                        mode='lines+markers',
                        name='HSL Processing'))
    fig.add_trace(go.Scatter(x=[i for i in range(len(color_time))], y=yuv_processing,
                        mode='lines+markers',
                        name='YUV Processing'))
    fig.add_trace(go.Scatter(x=[i for i in range(len(color_time))], y=color_time,
                        mode='lines+markers',
                        name='Color Time'))

    fig.update_layout(
        title={
            'text': "Time in color",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Iterations",
        yaxis_title="Time (s)",
    )

    fig.show()

if args.type in ["gris", "todo"]:
    grey_processing = open("{}/grey_processing.txt".format(folder_name))
    grey_processing = np.asarray([
        float(l.split(" ")[-2])
        for l in grey_processing.readlines()
    ])

    grey_time = open("{}/grey_time.txt".format(folder_name))
    grey_time = np.asarray([
        float(l.split(" ")[-2])
        for l in grey_time.readlines()
    ])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[i for i in range(len(grey_time))],
        y=grey_processing,
        mode='lines+markers',
        name='Grey Processing'))
    fig.add_trace(go.Scatter(
        x=[i for i in range(len(grey_time))],
        y=grey_time,
        mode='lines+markers',
        name='Grey Time'))

    fig.update_layout(
        title={
            'text': "Time in grayscale",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Iterations",
        yaxis_title="Time (s)",
    )

    fig.show()
