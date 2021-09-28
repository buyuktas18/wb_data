import matplotlib.pyplot as plt
import numpy as np

def save_plots_cool(no_of_sample, path, initial_u_values, terminal_u_values, initial_v_values, terminal_v_values, initial_Lv, terminal_Lv):
    x_axis = np.arange(no_of_sample)


#cool mode changes

    #u value's change

    plt.plot(x_axis, initial_u_values, 'r', x_axis, terminal_u_values, 'b')
    plt.savefig(path+"/cool_u_change.png")
    plt.clf()

    #v value's change

    plt.plot(x_axis, initial_v_values, 'r', x_axis, terminal_v_values, 'b')
    plt.savefig(path+"/cool_v_change.png")
    plt.clf()

    #Lv value's change

    plt.plot(x_axis, initial_Lv, 'r', x_axis, terminal_Lv, 'b')
    plt.savefig(path+"/cool_Lv_change.png")
    plt.clf()


def save_plots_st(no_of_sample, path, initial_u_values, terminal_u_values, initial_v_values, terminal_v_values, initial_Lv, terminal_Lv):
    x_axis = np.arange(no_of_sample)


#standard mode changes

    #u value's change

    plt.plot(x_axis, initial_u_values, 'r', x_axis, terminal_u_values, 'b')
    plt.savefig(path+"/st_u_change.png")
    plt.clf()

    #v value's change

    plt.plot(x_axis, initial_v_values, 'r', x_axis, terminal_v_values, 'b')
    plt.savefig(path+"/st_v_change.png")
    plt.clf()

    #Lv value's change

    plt.plot(x_axis, initial_Lv, 'r', x_axis, terminal_Lv, 'b')
    plt.savefig(path+"/st_Lv_change.png")
    plt.clf()


def save_plots_warm(no_of_sample, path, initial_u_values, terminal_u_values, initial_v_values, terminal_v_values, initial_Lv, terminal_Lv):
    x_axis = np.arange(no_of_sample)


#warm mode changes

    #u value's change

    plt.plot(x_axis, initial_u_values, 'r', x_axis, terminal_u_values, 'b')
    plt.savefig(path+"/w_u_change.png")
    plt.clf()

    #v value's change

    plt.plot(x_axis, initial_v_values, 'r', x_axis, terminal_v_values, 'b')
    plt.savefig(path+"/w_v_change.png")
    plt.clf()

    #Lv value's change

    plt.plot(x_axis, initial_Lv, 'r', x_axis, terminal_Lv, 'b')
    plt.savefig(path+"/w_Lv_change.png")
    plt.clf()