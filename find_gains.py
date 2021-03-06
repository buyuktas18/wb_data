import numpy as np
import pandas as pd
import re
from openpyxl import load_workbook

list_1 = []
list_2 = []
list_3 = []
list_4 = []
list_5 = []
list_6 = []
list_7 = []
list_8 = []
list_9 = []



def find_gains(lines, checkpoint_0, checkpoint_1, checkpoint_2, end_of_measurements):
    #find gain offset for cold MODE
        for i in range(len(checkpoint_0)):
            for j in range(checkpoint_0[i], checkpoint_1[i]): 
                if "Factory_Comp= 0" in lines[j]:    #R gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_1) <= i:
                        list_1.append(gain_value)
                    else:
                        list_1[i] = gain_value
                elif "Factory_Comp= 1" in lines[j]:   #G gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_2) <= i:
                        list_2.append(gain_value)
                    else:
                        list_2[i] = gain_value
                elif "Factory_Comp= 2" in lines[j]:   #B gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_3) <= i:
                        list_3.append(gain_value)
                    else:
                        list_3[i] = gain_value
            if len(list_4) <= i:
                list_4.append(128)
            if len(list_5) <= i:
                list_5.append(128)
            if len(list_6) <= i:
                list_6.append(128)

    #find gain offset for standard MODE
        for i in range(len(checkpoint_1)):
            for j in range(checkpoint_1[i], checkpoint_2[i]): 
                if "Factory_Comp= 0" in lines[j]:    #R gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_4) <= i:
                        list_4.append(gain_value)
                    else:
                        list_4[i] = gain_value
                elif "Factory_Comp= 1" in lines[j]:   #G gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_5) <= i:
                        list_5.append(gain_value)
                    else:
                        list_5[i] = gain_value
                elif "Factory_Comp= 2" in lines[j]:   #B gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_6) <= i:
                        list_6.append(gain_value)
                    else:
                        list_6[i] = gain_value
            if len(list_7) <= i:
                list_7.append(128)
            if len(list_8) <= i:
                list_8.append(128)
            if len(list_9) <= i:
                list_9.append(128)
    #find gain offset for warm MODE
        for i in range(len(checkpoint_2)):
            for j in range(checkpoint_2[i], end_of_measurements[i]): 
                if "Factory_Comp= 0" in lines[j]:    #R gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_7) <= i:
                        list_7.append(gain_value)
                    else:
                        list_7[i] = gain_value
                elif "Factory_Comp= 1" in lines[j]:   #G gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_8) <= i:
                        list_8.append(gain_value)
                    else:
                        list_8[i] = gain_value
                elif "Factory_Comp= 2" in lines[j]:   #B gain
                    gain_value = re.search('VALUE= (.*) ', lines[j])
                    gain_value = gain_value.group(1)
                    if len(list_9) <= i:
                        list_9.append(gain_value)
                    else:
                        list_9[i] = gain_value
            if len(list_1) <= i:
                list_1.append(128)
            if len(list_2) <= i:
                list_2.append(128)
            if len(list_2) <= i:
                list_2.append(128)

def export_to_excel(path, number_of_ok,  serie_numbers, coordinates):
    gain_data = np.zeros((number_of_ok, 21))



    gain_data[:,0] = coordinates[0]
    gain_data[:,1] = coordinates[2]
    gain_data[:,2] = coordinates[1]
    gain_data[:,3] = coordinates[3]    
    gain_data[:,4] = list_1
    gain_data[:,5] = list_2
    gain_data[:,6] = list_3

    gain_data[:,7] = coordinates[4]
    gain_data[:,8] = coordinates[6]
    gain_data[:,9] = coordinates[5]
    gain_data[:,10] = coordinates[7] 
    gain_data[:,11] = list_4
    gain_data[:,12] = list_5
    gain_data[:,13] = list_6

    gain_data[:,14] = coordinates[8]
    gain_data[:,15] = coordinates[10]
    gain_data[:,16] = coordinates[9]
    gain_data[:,17] = coordinates[11]    
    gain_data[:,18] = list_7
    gain_data[:,19] = list_8
    gain_data[:,20] = list_9

    list_1.clear()
    list_2.clear()
    list_3.clear()
    list_4.clear()
    list_5.clear()
    list_6.clear()
    list_7.clear()
    list_8.clear()
    list_9.clear()

    

    mux = pd.MultiIndex.from_product([['Cool', 'Standard', 'Warm'], ['initial u', 'final u', 'initial v', 'final v', 'R Gain', 'G Gain', 'B Gain']])
    df_gain = pd.DataFrame(gain_data, index = serie_numbers, columns=mux)
    df_gain.to_excel(path+"/final_gains.xlsx", sheet_name='gains')


    #find averages based on month
    months = []
    month_types = []
    for s in serie_numbers:
        months.append(s[6:8])
        if (s[6:8] in month_types) == False:
            month_types.append(s[6:8])
    #copy the existing dataframe
    df_month = df_gain

    #add the modified dataframe to the new sheet on excel
    df_month['month'] = months

    book = load_workbook(path+"/final_gains.xlsx")
    writer = pd.ExcelWriter(path+"/final_gains.xlsx", engine = 'openpyxl')
    writer.book = book

    for m in month_types:
        print("a")
        
        new_df = df_month[df_month['month'] == m]
        
            
        new_df.to_excel(writer, sheet_name=m)
    

    writer.save()
    writer.close()


