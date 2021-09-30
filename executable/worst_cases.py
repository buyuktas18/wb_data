def worst_case(path, max_cool_series, max_cool_values, max_st_series, max_st_values, max_w_series, max_w_values):
    file1 = open(path+"/worst_cases.txt", "w")
    for i in range(25):
        file1.write(str(max_cool_series[i]) + "\t" + str(max_cool_values[i]) + "\n")
    file1.close()

    file2 = open(path+"/worst_cases_st.txt", "w")
    for i in range(25):
        file2.write(str(max_st_series[i]) + "\t" + str(max_st_values[i]) + "\n")
    file2.close()

    file3 = open(path+"/worst_cases_w.txt", "w")
    for i in range(25):
        file3.write(str(max_w_series[i]) + "\t" + str(max_w_values[i]) + "\n")
