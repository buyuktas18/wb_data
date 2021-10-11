def create_data(path, initial_u_values, initial_v_values, serie_numbers):
    file1 = open(path+"/graph_data.txt", "w")
    for i in range(len(initial_u_values)):
        file1.write(str(initial_u_values[i]) + "\t" + str(initial_v_values[i]) + "\t" + str(serie_numbers[i]) + "\n")
    file1.close()