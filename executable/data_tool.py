#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
import os
import matplotlib.pyplot as plt
import re
import pandas as pd
import pathlib
from scipy.stats import norm
import sklearn.covariance
import shutil
from save_plots import save_plots_cool, save_plots_st, save_plots_warm
from find_gains import find_gains, export_to_excel

#we shall store all the file names in this list


def run_program(filelist, path, options):

    total = []

    st1 = []
    st2 = []
    st3 = []
    st4 = []
    st5 = []
    st6 = []

    means = []
    st_devs = []

    cool_means = []
    cool_sd = []

    st_means = []
    st_sd = []

    warm_means = []
    warm_sd = []

    avg_us = []
    avg_vs = []
    avg_Lvs = []

    cool_max = []
    st_max = []
    warm_max = []

    cool_u_offset = []
    cool_v_offset = []

    st_u_offset = []
    st_v_offset = []

    w_u_offset = []
    w_v_offset = []

    cool_u_offset_a = []
    cool_v_offset_a = []

    st_u_offset_a = []
    st_v_offset_a = []

    w_u_offset_a = []
    w_v_offset_a = []


    mainboard_names=[] 

    
    df = pd.DataFrame()
    total_iteration = []
    average_iteration = []
    c_rate_of_success = []
    """for root, dirs, files in os.walk(path):
        for file in files:
            
            filelist.append(os.path.join(root,file))"""


    #filelist = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]


    file_identifier=[]
    for fi in filelist:
        result = re.search('05(.*)_', fi)
        file_identifier.append('05'+result.group(1))
   

    for fp in range(len(filelist)):


        
        

        with open(filelist[fp]) as f:
            lines = f.readlines()

        res = lines[0].split('\t')[6]
        #mainboard_names.append('NG')
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

        find_gains(lines, checkpoint_0, checkpoint_1, checkpoint_2, end_of_measurements)
        

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



        x_axis = np.arange(len(checkpoint_1))


        

        my_path_str = path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]
        my_path = pathlib.Path(my_path_str) 


        if my_path.is_dir():
            shutil.rmtree(my_path)
            


        os.mkdir(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp])
        export_to_excel(my_path_str, number_of_ok, serie_numbers)
        #cool deviations
        save_plots_cool(len(checkpoint_1), my_path_str, initial_u_values, terminal_u_values, initial_v_values, terminal_v_values, initial_Lv, terminal_Lv)

        average_u = np.average(initial_u_values)
        average_v = np.average(initial_v_values)

        average_u_a = np.average(terminal_u_values)
        average_v_a = np.average(terminal_v_values)

        cool_u_offset.append(average_u)
        cool_v_offset.append(average_v)

        cool_u_offset_a.append(average_u_a)
        cool_v_offset_a.append(average_v_a)




        res = np.sqrt((average_u - initial_u_values)**2+(average_v - initial_v_values)**2)
        mu, std = norm.fit(res)
        plt.hist(res, bins=6, density=True, alpha=1, color='g')


        cool_mean = mu
        cool_means.append(cool_mean)

        cool_sdev = std
        cool_sd.append(cool_sdev)

        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/normal_cool.png")
        plt.clf()

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


        # In[175]:


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


        # In[176]:


        #standard values


        # In[177]:

        save_plots_st(len(checkpoint_1), my_path_str, st_initial_u_values, st_terminal_u_values, st_initial_v_values, st_terminal_v_values, st_initial_Lv, st_terminal_Lv)

        st_average_u = np.average(st_initial_u_values)
        st_average_v = np.average(st_initial_v_values)

        st_average_u_a = np.average(st_terminal_u_values)
        st_average_v_a = np.average(st_terminal_v_values)

        st_u_offset.append(st_average_u)
        st_v_offset.append(st_average_v)

        st_u_offset_a.append(st_average_u_a)
        st_v_offset_a.append(st_average_v_a)

        res = np.sqrt((st_average_u - st_initial_u_values)**2+(st_average_v - st_initial_v_values)**2)
        mu, std = norm.fit(res)

        st_mean = mu
        st_means.append(st_mean)

        st_sdev = std
        st_sd.append(st_sdev)

        plt.hist(res, bins=6, density=True, alpha=1, color='g')


        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/normal_st.png")
        plt.clf()


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

        save_plots_warm(len(checkpoint_1), my_path_str, w_initial_u_values, w_terminal_u_values, w_initial_v_values, w_terminal_v_values, w_initial_Lv, w_terminal_Lv)
        


        w_average_u = np.average(w_initial_u_values)
        w_average_v = np.average(w_initial_v_values)

        w_average_u_a = np.average(w_terminal_u_values)
        w_average_v_a = np.average(w_terminal_v_values)

        w_u_offset.append(w_average_u)
        w_v_offset.append(w_average_v)

        w_u_offset_a.append(w_average_u_a)
        w_v_offset_a.append(w_average_v_a)

        res = np.sqrt((w_average_u - w_initial_u_values)**2+(w_average_v - w_initial_v_values)**2)
        mu, std = norm.fit(res)

        w_mean = mu
        warm_means.append(w_mean)

        warm_sd.append(std)

        plt.hist(res, bins=6, density=True, alpha=1, color='g')


        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/normal_warm.png")
        plt.clf()



        file1 = open(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/worst_cases.txt", "w")
        for i in range(25):
            file1.write(str(max_cool_series[i]) + "\t" + str(max_cool_values[i]) + "\n")
        file1.close()

        file2 = open(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/worst_cases_st.txt", "w")
        for i in range(25):
            file2.write(str(max_st_series[i]) + "\t" + str(max_st_values[i]) + "\n")
        file2.close()

        

#1
        mu, std = norm.fit(initial_u_values)
        st1.append(std)
        plt.hist(initial_u_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/initial_u_cool.png")
        plt.clf()

#2

        mu, std = norm.fit(initial_v_values)
        st2.append(std)

        plt.hist(initial_v_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/initial_v_cool.png")
        plt.clf()
#3

        mu, std = norm.fit(st_initial_u_values)
        st3.append(std)

        plt.hist(st_initial_v_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/initial_u_st.png")
        plt.clf()

#4
        mu, std = norm.fit(st_initial_v_values)
        st4.append(std)

        plt.hist(st_initial_v_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/initial_v_st.png")
        plt.clf()

#5

        mu, std = norm.fit(w_initial_u_values)
        st5.append(std)

        plt.hist(w_initial_u_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/initial_u_warm.png")
        plt.clf()

#6
        mu, std = norm.fit(w_initial_v_values)
        st6.append(std)

        plt.hist(w_initial_v_values, bins=6, density=True, alpha=1, color='r', edgecolor='k')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mean = %.2f,  std = %.2f, N = %i" % (mu, std, number_of_ok)
        plt.title(title)

        plt.savefig(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/initial_v_warm.png")
        plt.clf()


        el = sklearn.covariance.EllipticEnvelope(store_precision=True, assume_centered=False, support_fraction=None, contamination=0.0075, random_state=0)
        d = pd.DataFrame()
        
        d['u'] = initial_u_values
        d['v'] = initial_v_values
        el.fit(d)
        d['anomaly'] = el.predict(d)
        predictions = d.loc[d['anomaly'] < 1]
        anomalies = []
        anomaly_index = list(predictions.index.values)


        for i in range(len(anomaly_index)):
            anomalies.append(serie_numbers[anomaly_index[i]])

        file2 = open(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/prediction_seri.txt", "w")
        for i in anomalies:
            file2.write(i+"\n")
        file2.close()

        

        predictions.to_excel(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/predictions.xlsx")   


        number_of_iteration = 0
        for i in range(len(ending_point)):
            number_of_iteration += int((ending_point[i]-checkpoint_0[i]-6)/2)


        # In[344]:


        avg_iteration = number_of_iteration/number_of_ok
        

        # In[345]:


        rate_of_success = number_of_ok/(number_of_ok+number_of_nok)



        # In[349]:


        avg_u = (np.average(deviation_u)+np.average(st_deviation_u)+np.average(w_deviation_u))/3

        avg_us.append(avg_u)



        # In[351]:


        avg_v = (np.average(deviation_v)+np.average(st_deviation_v)+np.average(w_deviation_v))/3

        avg_vs.append(avg_v)

        # In[353]:


        avg_Lv = (np.average(deviation_Lv)+np.average(st_deviation_Lv)+np.average(w_deviation_Lv))/3
        avg_Lvs.append(avg_Lv)
        

        total_iteration.append(number_of_iteration)
        average_iteration.append(avg_iteration)
        c_rate_of_success.append(rate_of_success)
        total.append(number_of_ok)
        
        warm_max.append(np.max(res))
        sorted_indexes = res.argsort()

        max_w_values = res[sorted_indexes[-25:][::-1]]
        max_w_series = []
        for k in range(25):
            max_w_series.append(serie_numbers[sorted_indexes[-k-1]])

        file3 = open(path+'/'+file_identifier[fp]+"-"+mainboard_names[fp]+"/worst_cases_w.txt", "w")
        for i in range(25):
            file3.write(str(max_w_series[i]) + "\t" + str(max_w_values[i]) + "\n")

    df['Panel'] = file_identifier
    df['Mainboard'] = mainboard_names
    df['Total WB'] = pd.Series(total)
    df['Total Iteration'] = pd.Series(total_iteration)
    df['average iteration'] = pd.Series(average_iteration)
    df['rate of success'] = pd.Series(c_rate_of_success)
    df['avg_u'] = pd.Series(avg_us)
    df['avg_v'] = pd.Series(avg_vs)
    df['avg_Lv'] = pd.Series(avg_Lvs)
    df['Cool mean'] = pd.Series(cool_means)
    df['Cool sdev'] = pd.Series(cool_sd)
    df['Standard mean'] = pd.Series(st_means)
    df['Standard sdev'] = pd.Series(st_sd)
    df['Warm mean'] = pd.Series(warm_means)
    df['Warm sdev'] = pd.Series(warm_sd)
    df['Cool max'] = pd.Series(cool_max)
    df['Standard max'] = pd.Series(st_max)
    df['Warm max'] = pd.Series(warm_max)
    df['Cool u offset'] = pd.Series(cool_u_offset)
    df['Cool v offset'] = pd.Series(cool_v_offset)
    df['Standard u offset'] = pd.Series(st_u_offset)
    df['Standard v offset'] = pd.Series(st_v_offset)
    df['Warm u offset'] = pd.Series(w_u_offset)
    df['Warm v offset'] = pd.Series(w_v_offset)
    df['Cool u offset after wb'] = pd.Series(cool_u_offset_a)
    df['Cool v offset after wb'] = pd.Series(cool_v_offset_a)
    df['Standard u offset after wb'] = pd.Series(st_u_offset_a)
    df['Standard v offset after wb'] = pd.Series(st_v_offset_a)
    df['Warm u offset after wb'] = pd.Series(w_u_offset_a)
    df['Warm v offset after wb'] = pd.Series(w_v_offset_a)

    df['stdev1'] = pd.Series(st1)
    df['stdev2'] = pd.Series(st2)
    df['stdev3'] = pd.Series(st3)
    df['stdev4'] = pd.Series(st4)
    df['stdev5'] = pd.Series(st5)
    df['stdev6'] = pd.Series(st6)

    df.to_excel(path+'/'+"result.xlsx")   
    print(df)



























