import matplotlib.pyplot as plt
import numpy as np


def create_plot(file_id):
    global series
    global fig
    global ax 

    x = []
    y = []
    series = []

    with open(file_id + "/graph_data.txt") as f:
        lines = f.readlines()

    for line in lines:
        arr = line.split("\t")
        x.append(int(arr[0]))
        y.append(int(arr[1]))
        series.append(arr[2])


    fig, ax = plt.subplots()
    global sc
    sc = plt.scatter(x, y)


    global annot 
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = series[ind["ind"][0]]
    annot.set_text(text)
    


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

