import numpy as np
import os
import re
import pathlib
import shutil
from save_plots import save_plots_cool, save_plots_st, save_plots_warm
from find_gains import find_gains, export_to_excel
from dist_val import cool_dist_u, cool_dist_v, st_dist_u, st_dist_v, w_dist_u, w_dist_v
from predict import predict
from evaluation import create_result
from worst_cases import worst_case
from show_position import update_annot, hover, create_plot
from graph_data import create_data
from variables import *
import tkinter as tk
from show_position import create_plot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_program(filelist, path):
    print("enter")
    #read all files and append it to the list
    for fi in filelist:
        result = re.search('05(.*)_', fi)
        file_identifier.append('05'+result.group(1))
   

    for fp in range(len(filelist)):
        
        with open(filelist[fp]) as f:
            lines = f.readlines()

        res = lines[0].split('\t')[6]
        mainboard_names.append(res)


        serie_numbers = []
        checkpoint_0 = []
        checkpoint_1 = []
        checkpoint_2 = []
        starting_point = []
        ending_point = []
        end_of_measurements = []
        number_of_nok = 0
        number_of_ok = 0
        i = 0

        for line in lines:
            if "WHITE BALANCE ADJUSTMENT STEP" in line:
                started_at = i
                
            if ("WBA_RESULT= OK" in line):
                end_of_measurements.append(i)
                starting_point.append(started_at)
                serie_numbers.append(lines[started_at-1].split('\t')[0])
                number_of_ok = number_of_ok+1
            elif "WBA_RESULT= NOK" in line:
                number_of_nok=number_of_nok+1
            i = i+1
        i = 0
        j = 0
    
        flag = True


        for line in lines:
            if (starting_point[j] <= i and i <= end_of_measurements[j]):
                
                #print(end_of_measurements[j])
                if "SET_WBA_ColorTemp= 0" in line:
                    checkpoint_0.append(i)
                elif "SET_WBA_ColorTemp= 1" in line:
                    checkpoint_1.append(i)
                elif "SET_WBA_ColorTemp= 2" in line:
                    checkpoint_2.append(i)
                elif "WBA_INTERNAL_PATTERN_OFF" in line:
                    if(flag):
                        ending_point.append(i)
                    if "WBA_INTERNAL_PATTERN_OFF: NOK" in line:
                        flag = False
                    else:
                        flag = True
                    
            if i == end_of_measurements[j] and j != len(end_of_measurements)-1:
            
                j = j+1
            i = i+1

        

        #cool values
        initial_u_values = []
        terminal_u_values = []
        initial_v_values = []
        terminal_v_values = []
        initial_Lv = []
        terminal_Lv =[]

        for j in range(number_of_ok):
            result = re.search('u= (.*)\tv', lines[checkpoint_0[j]+2])
            initial_u_values.append(result.group(1))
            result = re.search('u= (.*)\tv', lines[checkpoint_1[j]-1])
            terminal_u_values.append(result.group(1))
            result = re.search('v= (.*)\tL', lines[checkpoint_0[j]+2])
            initial_v_values.append(result.group(1))
            result = re.search('v= (.*)\tL', lines[checkpoint_1[j]-1])
            terminal_v_values.append(result.group(1))
            result = re.search('Lv= (.*) ', lines[checkpoint_0[j]+2])
            initial_Lv.append(result.group(1))
            result = re.search('Lv= (.*)\ ', lines[checkpoint_1[j]-1])
            terminal_Lv.append(result.group(1))



        initial_u_values = np.array(initial_u_values)
        initial_u_values = initial_u_values.astype(int)
        terminal_u_values = np.array(terminal_u_values)
        terminal_u_values = terminal_u_values.astype(int)
        deviation_u = np.abs(terminal_u_values - initial_u_values)

        initial_v_values = np.array(initial_v_values)
        initial_v_values = initial_v_values.astype(int)
        terminal_v_values = np.array(terminal_v_values)
        terminal_v_values = terminal_v_values.astype(int)
        deviation_v = np.abs(terminal_v_values - initial_v_values)

        initial_Lv = np.array(initial_Lv)
        initial_Lv = initial_Lv.astype(int)
        terminal_Lv = np.array(terminal_Lv)
        terminal_Lv = terminal_Lv.astype(int)
        deviation_Lv = np.abs(terminal_Lv - initial_Lv)

        my_path_str = path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]
        my_path = pathlib.Path(my_path_str) 
        my_files.append(file_identifier[fp]+"-"+mainboard_names[fp])

        if my_path.is_dir():
            shutil.rmtree(my_path)
            


        os.mkdir(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp])
        
        average_u = np.average(initial_u_values)
        average_v = np.average(initial_v_values)

        average_u_a = np.average(terminal_u_values)
        average_v_a = np.average(terminal_v_values)

        cool_u_offset.append(average_u)
        cool_v_offset.append(average_v)

        cool_u_offset_a.append(average_u_a)
        cool_v_offset_a.append(average_v_a)


        #cool mode furthest points

        res = np.sqrt((average_u - initial_u_values)**2+(average_v - initial_v_values)**2)
        cool_max.append(np.max(res))

        sorted_indexes = res.argsort()

        max_cool_values = res[sorted_indexes[-25:][::-1]]
        max_cool_series = []
        for k in range(25):
            max_cool_series.append(serie_numbers[sorted_indexes[-k-1]])

    

        #standard values
        st_initial_u_values = []
        st_terminal_u_values = []
        st_initial_v_values = []
        st_terminal_v_values = []
        st_initial_Lv = []
        st_terminal_Lv =[]

        for j in range(len(checkpoint_1)):
            result = re.search('u= (.*)\tv', lines[checkpoint_1[j]+2])
            st_initial_u_values.append(result.group(1))
            result = re.search('u= (.*)\tv', lines[checkpoint_2[j]-1])
            st_terminal_u_values.append(result.group(1))
            result = re.search('v= (.*)\tL', lines[checkpoint_1[j]+2])
            st_initial_v_values.append(result.group(1))
            result = re.search('v= (.*)\tL', lines[checkpoint_2[j]-1])
            st_terminal_v_values.append(result.group(1))
            result = re.search('Lv= (.*) ', lines[checkpoint_1[j]+2])
            st_initial_Lv.append(result.group(1))
            result = re.search('Lv= (.*)\ ', lines[checkpoint_2[j]-1])
            st_terminal_Lv.append(result.group(1))


        st_initial_u_values = np.array(st_initial_u_values)
        st_initial_u_values = st_initial_u_values.astype(int)
        st_terminal_u_values = np.array(st_terminal_u_values)
        st_terminal_u_values = st_terminal_u_values.astype(int)
        st_deviation_u = np.abs(st_terminal_u_values - st_initial_u_values)

        st_initial_v_values = np.array(st_initial_v_values)
        st_initial_v_values = st_initial_v_values.astype(int)
        st_terminal_v_values = np.array(st_terminal_v_values)
        st_terminal_v_values = st_terminal_v_values.astype(int)
        st_deviation_v = np.abs(st_terminal_v_values - st_initial_v_values)

        st_initial_Lv = np.array(st_initial_Lv)
        st_initial_Lv = st_initial_Lv.astype(int)
        st_terminal_Lv = np.array(st_terminal_Lv)
        st_terminal_Lv = st_terminal_Lv.astype(int)
        st_deviation_Lv = np.abs(st_terminal_Lv - st_initial_Lv)


        st_average_u = np.average(st_initial_u_values)
        st_average_v = np.average(st_initial_v_values)

        st_average_u_a = np.average(st_terminal_u_values)
        st_average_v_a = np.average(st_terminal_v_values)

        st_u_offset.append(st_average_u)
        st_v_offset.append(st_average_v)

        st_u_offset_a.append(st_average_u_a)
        st_v_offset_a.append(st_average_v_a)


        #standard mode furthest points

        res = np.sqrt((st_average_u - st_initial_u_values)**2+(st_average_v - st_initial_v_values)**2)
        
        st_max.append(np.max(res))

        sorted_indexes = res.argsort()

        max_st_values = res[sorted_indexes[-25:][::-1]]
        max_st_series = []
        for k in range(25):
            max_st_series.append(serie_numbers[sorted_indexes[-k-1]])
        



        #warm values
        w_initial_u_values = []
        w_terminal_u_values = []
        w_initial_v_values = []
        w_terminal_v_values = []
        w_initial_Lv = []
        w_terminal_Lv =[]

        for j in range(len(checkpoint_1)):
            result = re.search('u= (.*)\tv', lines[checkpoint_2[j]+2])
            w_initial_u_values.append(result.group(1))
            result = re.search('u= (.*)\tv', lines[ending_point[j]-2])
            w_terminal_u_values.append(result.group(1))
            result = re.search('v= (.*)\tL', lines[checkpoint_2[j]+2])
            w_initial_v_values.append(result.group(1))
            result = re.search('v= (.*)\tL', lines[ending_point[j]-2])
            w_terminal_v_values.append(result.group(1))
            result = re.search('Lv= (.*) ', lines[checkpoint_2[j]+2])
            w_initial_Lv.append(result.group(1))
            result = re.search('Lv= (.*)\ ', lines[ending_point[j]-2])
            w_terminal_Lv.append(result.group(1))


        # In[318]:


        w_initial_u_values = np.array(w_initial_u_values)
        w_initial_u_values = w_initial_u_values.astype(int)
        w_terminal_u_values = np.array(w_terminal_u_values)
        w_terminal_u_values = w_terminal_u_values.astype(int)
        w_deviation_u = np.abs(w_terminal_u_values - w_initial_u_values)

        w_initial_v_values = np.array(w_initial_v_values)
        w_initial_v_values = w_initial_v_values.astype(int)
        w_terminal_v_values = np.array(w_terminal_v_values)
        w_terminal_v_values = w_terminal_v_values.astype(int)
        w_deviation_v = np.abs(w_terminal_v_values - w_initial_v_values)

        w_initial_Lv = np.array(w_initial_Lv)
        w_initial_Lv = w_initial_Lv.astype(int)
        w_terminal_Lv = np.array(w_terminal_Lv)
        w_terminal_Lv = w_terminal_Lv.astype(int)
        w_deviation_Lv = np.abs(w_terminal_Lv - w_initial_Lv)

        


        w_average_u = np.average(w_initial_u_values)
        w_average_v = np.average(w_initial_v_values)

        w_average_u_a = np.average(w_terminal_u_values)
        w_average_v_a = np.average(w_terminal_v_values)

        w_u_offset.append(w_average_u)
        w_v_offset.append(w_average_v)

        w_u_offset_a.append(w_average_u_a)
        w_v_offset_a.append(w_average_v_a)

        #warm mode furthest points

        res = np.sqrt((w_average_u - w_initial_u_values)**2+(w_average_v - w_initial_v_values)**2)
        
        warm_max.append(np.max(res))
        sorted_indexes = res.argsort()

        max_w_values = res[sorted_indexes[-25:][::-1]]
        max_w_series = []
        for k in range(25):
            max_w_series.append(serie_numbers[sorted_indexes[-k-1]])

        #last assignments for the resul excel
        number_of_iteration = 0
        for i in range(len(ending_point)):
            number_of_iteration += int((ending_point[i]-checkpoint_0[i]-6)/2)

        avg_iteration = number_of_iteration/number_of_ok
        rate_of_success = number_of_ok/(number_of_ok+number_of_nok)
        avg_u = (np.average(deviation_u)+np.average(st_deviation_u)+np.average(w_deviation_u))/3
        avg_us.append(avg_u)

        avg_v = (np.average(deviation_v)+np.average(st_deviation_v)+np.average(w_deviation_v))/3

        avg_vs.append(avg_v)

        avg_Lv = (np.average(deviation_Lv)+np.average(st_deviation_Lv)+np.average(w_deviation_Lv))/3
        avg_Lvs.append(avg_Lv)
        
        total_iteration.append(number_of_iteration)
        average_iteration.append(avg_iteration)
        c_rate_of_success.append(rate_of_success)
        total.append(number_of_ok)




        #decision with checkbox

        save_plots_cool(len(checkpoint_1), my_path_str, initial_u_values, terminal_u_values, initial_v_values, terminal_v_values, initial_Lv, terminal_Lv)
        save_plots_st(len(checkpoint_1), my_path_str, st_initial_u_values, st_terminal_u_values, st_initial_v_values, st_terminal_v_values, st_initial_Lv, st_terminal_Lv)
        save_plots_warm(len(checkpoint_1), my_path_str, w_initial_u_values, w_terminal_u_values, w_initial_v_values, w_terminal_v_values, w_initial_Lv, w_terminal_Lv)

        cool_dist_u(my_path_str, initial_u_values)
        cool_dist_v(my_path_str, initial_v_values)
        st_dist_u(my_path_str, st_initial_u_values)
        st_dist_v(my_path_str, st_initial_v_values)
        w_dist_u(my_path_str, w_initial_u_values)
        w_dist_u(my_path_str, w_initial_v_values)

        #create a text file contains inital and terminal coordinate values

        #convert lists to np arrays
        #for cool mode
        arr1 = initial_u_values
        arr2 = initial_v_values
        arr3 = terminal_u_values
        arr4 = terminal_v_values

        #for standard mode

        arr5 = st_initial_u_values
        arr6 = st_initial_v_values
        arr7 = st_terminal_u_values
        arr8 = st_terminal_v_values

        #for warm mode

        arr9 = w_initial_u_values
        arr10 = w_initial_v_values
        arr11 = w_terminal_u_values
        arr12 = w_terminal_v_values

        coordinates = [arr1, arr2, arr3, arr4,   
                        arr5, arr6, arr7, arr8,
                        arr9, arr10, arr11, arr12]


        find_gains(lines, checkpoint_0, checkpoint_1, checkpoint_2, end_of_measurements)
        print(number_of_ok)
        export_to_excel(my_path_str, number_of_ok, serie_numbers, coordinates)
        
        worst_case(my_path_str, max_cool_series, max_cool_values, max_st_series, max_st_values, max_w_series, max_w_values)

        predict(initial_u_values, initial_v_values, serie_numbers, my_path_str)


        #interactive scatter

        #create_plot(initial_u_values, initial_v_values, serie_numbers)

        create_data(my_path_str, initial_u_values, initial_v_values, serie_numbers)

        #create_plot(my_path_str)
    



    """create_result(path, file_identifier, mainboard_names, total_iteration, 
                average_iteration, c_rate_of_success, cool_means, cool_sd,st_means,st_sd,warm_means,
                warm_sd, cool_max, st_max, warm_max, cool_u_offset, cool_v_offset, st_u_offset, st_v_offset,
                w_u_offset, w_v_offset, cool_u_offset_a, cool_v_offset_a, st_u_offset_a, st_v_offset_a
                w_u_offset_a, w_v_offset_a):    """
    print(my_files)
    return my_files
    





















