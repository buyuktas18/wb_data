def create_result(path, file_identifier, mainboard_names, total_iteration, 
                average_iteration, c_rate_of_success, cool_means, cool_sd,st_means,st_sd,warm_means,
                warm_sd, cool_max, st_max, warm_max, cool_u_offset, cool_v_offset, st_u_offset, st_v_offset,
                w_u_offset, w_v_offset, cool_u_offset_a, cool_v_offset_a, st_u_offset_a, st_v_offset_a, w_u_offset_a, w_v_offset_a):
    df = pd.DataFrame()

    df['Panel'] = file_identifier
    df['Mainboard'] = mainboard_names
    df['Total WB'] = pd.Series(total)
    df['Total Iteration'] = pd.Series(total_iteration)
    df['average iteration'] = pd.Series(average_iteration)
    df['rate of success'] = pd.Series(c_rate_of_success)
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


    df.to_excel(path+'/'+"result.xlsx")   