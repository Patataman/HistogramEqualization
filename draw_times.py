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
parser.add_argument('--type', required=True, type=str, help='Tipo de gráfica [color, gris, todo, speed, msg]')

args = parser.parse_args()

folder_names = [Path("{}/times".format(folder)) for folder in args.folder]

if args.type in ['msg']:
    histo_grey = go.Figure()
    histo_color = go.Figure()

    # Histograma Original
    org_cpu_grey = open("Original/times/1/grey_processing.txt")
    org_cpu_hsl = open("Original/times/1/hsl_processing.txt")
    org_cpu_yuv = open("Original/times/1/yuv_processing.txt")
    sec_grey_cpu = np.asarray([
        float(l.split(" ")[-2])
        for l in org_cpu_grey.readlines()
    ]).mean()

    sec_color_cpu = np.asarray([
        float(l.split(" ")[-2])
        for l in org_cpu_hsl.readlines()
    ]).mean() + np.asarray([
        float(l.split(" ")[-2])
        for l in org_cpu_yuv.readlines()
    ]).mean()

    org_time_grey = open("Original/times/1/grey_time.txt")
    org_time_color = open("Original/times/1/color_time.txt")

    sec_grey_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in org_time_grey.readlines()
    ]).mean()
    sec_color_mean = np.asarray([
        float(l.split(" ")[-2])
        for l in org_time_color.readlines()
    ]).mean()

    sec_io_grey = sec_grey_mean - sec_grey_cpu
    sec_io_color = sec_color_mean - sec_color_cpu

    # Histograma paralelo
    for f in folder_names:
        if f.parent.stem == "Combinado":
            par_time_grey =  open("Combinado/times/2-4/grey_time.txt")
            par_time_color = open("Combinado/times/2-4/color_time.txt")
            par_cpu_grey =   open("Combinado/times/2-4/grey_processing.txt")
            par_cpu_hsl =    open("Combinado/times/2-4/hsl_processing.txt")
            par_cpu_yuv =    open("Combinado/times/2-4/yuv_processing.txt")
            par_time_msg_gris =   open("Combinado/times/2-4/msg_time_gris.txt")
            par_time_msg_color =   open("Combinado/times/2-4/msg_time_color.txt")

            par_grey_cpu = np.asarray([
                float(l.split(" ")[-2])
                for l in par_cpu_grey.readlines()
            ]).mean()

            par_color_cpu = np.asarray([
                float(l.split(" ")[-2])
                for l in par_cpu_hsl.readlines()
            ]).mean() + np.asarray([
                float(l.split(" ")[-2])
                for l in par_cpu_yuv.readlines()
            ]).mean()

            par_grey_mean = np.asarray([
                float(l.split(" ")[-2])
                for l in par_time_grey.readlines()
            ]).mean()
            par_color_mean = np.asarray([
                float(l.split(" ")[-2])
                for l in par_time_color.readlines()
            ]).mean()

            par_io_grey = par_grey_mean - par_grey_cpu
            par_io_color = par_color_mean - par_color_cpu

            par_msg_gris = []
            aux = []
            for l in par_time_msg_gris.readlines():
                aux.append(float(l.split(" ")[-2]))
                if len(aux) % 4 == 0:
                    # Hay 4 mensajes del gris
                    par_msg_gris.append(np.asarray(aux).sum())
                    del aux[:]
            par_msg_gris_mean = np.asarray(par_msg_gris).mean()

            par_msg_color = []
            aux = []
            for l in par_time_msg_color.readlines():
                aux.append(float(l.split(" ")[-2]))
                if len(aux) % 7 == 0:
                    # Hay 7 mensajes del color
                    par_msg_color.append(np.asarray(aux).sum())
                    del aux[:]
            par_msg_color_mean = np.asarray(par_msg_color).mean()

    #################

    x_types = ["sequential", "parallel"]
    histo_grey = go.Figure(data=[
        go.Bar(name='cpu', x=x_types, y=[sec_grey_cpu, par_grey_cpu],
            text=[round(sec_grey_cpu,2), round(par_grey_cpu,2)], textposition='auto'),
        go.Bar(name='msg', x=x_types, y=[0, par_msg_gris_mean],
            text=[0,round(par_msg_gris_mean,2)], textposition='auto'),
        go.Bar(name='io',  x=x_types, y=[sec_io_grey, par_io_grey],
            text=[round(sec_io_grey,2), round(par_io_grey, 2)], textposition='auto'),
    ])

    histo_grey.update_xaxes(type='category')
    histo_grey.update_layout(
        barmode='stack',
        title_text='Greyscale Total times', # title of plot
        xaxis_title_text='Sequential vs Parallel', # xaxis label
        yaxis_title_text='Time (s)', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )
    histo_grey.show()
    histo_grey.write_image("hist_times_grey.svg")

    histo_color = go.Figure(data=[
        go.Bar(name='cpu', x=x_types, y=[sec_color_cpu, par_color_cpu],
            text=[round(sec_color_cpu,2), round(par_color_cpu, 2)], textposition='auto'),
        go.Bar(name='msg', x=x_types, y=[0, par_msg_color_mean],
            text=[0, round(par_msg_color_mean, 2)], textposition='auto'),
        go.Bar(name='io',  x=x_types, y=[sec_io_color, par_io_color],
            text=[round(sec_io_color, 2), round(par_io_color, 2)], textposition='auto'),
    ])

    histo_color.update_xaxes(type='category')
    histo_color.update_layout(
        barmode='stack',
        title_text='Color Total times', # title of plot
        xaxis_title_text='Sequential vs Parallel', # xaxis label
        yaxis_title_text='Time (s)', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )
    histo_color.show()
    histo_color.write_image("hist_times_color.svg")

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

    amd_fig = go.Figure()
    gstv_fig = go.Figure()

    max_iter = 17
    amd_teorico = [1/((1 - 0.32638) + 0.32638/n) for n in range(1, max_iter)]
    gstv_teorico = [n - (1 - 0.32638)*(n-1) for n in range(1, max_iter)]

    scatter_amd = go.Scatter(
        x=[x for x in range(1, max_iter)],
        y=amd_teorico,
        text=[round(1/((1 - 0.32638) + 0.32638/n), 2) for n in range(1, max_iter)],
        textposition="top center",
        mode='lines+markers+text',
        name='Perfect Speed up'
    )
    scatter_gstv = go.Scatter(
        x=[x for x in range(1, max_iter)],
        y=gstv_teorico,
        text=[round(i,2) for i in gstv_teorico],
        textposition="top center",
        mode='lines+markers+text',
        name='Perfect Speed up'
    )

    # Teórico
    amd_fig.add_trace(scatter_amd)
    gstv_fig.add_trace(scatter_gstv)

    for f in folder_names:
        if f.parent.stem == "Original":
            continue

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

                scatter = go.Scatter(
                    x=[i for i in range(1, max_iter)],
                    y=(np.asarray(original_mean)/np.asarray(comb_means)).tolist(),
                    text=[round(i,2) for i in (np.asarray(original_mean)/np.asarray(comb_means)).tolist()],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={} I/O'.format(n.stem)
                )
                amd_fig.add_trace(scatter)
                gstv_fig.add_trace(scatter)

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

                scatter = go.Scatter(
                    x=[i for i in range(1, max_iter)],
                    y=(np.asarray(fake_mean)/np.asarray(fake_comb_means)).tolist(),
                    text=[round(i,2) for i in (np.asarray(fake_mean)/np.asarray(fake_comb_means)).tolist()],
                    textposition="top center",
                    mode='lines+markers+text',
                    name='MPI N={} NO I/O'.format(n.stem)
                )
                amd_fig.add_trace(scatter)
                gstv_fig.add_trace(scatter)

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

        gstv_fig.update_layout(
            title={
                'text': "Gustafson's Law",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Num processors",
            yaxis_title="Speed up",
        )
        gstv_fig.update_xaxes(type='category')
        gstv_fig.show()

        gstv_fig.write_image("gustafson_comb_todo.svg")


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
