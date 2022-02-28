from DoE import sobol
import numpy as np
import time
from rzwqm.rzwqm_file import RZWQM
import os
import subprocess
from rzwqm.csv_parsing import read_the_file_split
from datetime import datetime
from stat import nse
met_path_snow = ''
simulate_path = ''


def write_to_file_with_changed_val(path_to_write, data, line_num, changed_line):
    sno_line_d = ''
    for count, val in enumerate(changed_line):
        if count != (len(changed_line) - 1):
            sno_line_d = sno_line_d + str(val) + '  '
        else:
            sno_line_d = sno_line_d + str(val)
        data[line_num] = sno_line_d
    print(sno_line_d)
    with open(path_to_write, 'w') as file:
        for line in data:
            file.write(line + '\n')


def return_nse_snow(path):
    ob = read_the_file_split(path)
    del ob[0]
    rz = RZWQM(met_path_snow, '', simulate_path)
    sim = rz.rzwqm_res_parse('snow')
    ob_all = []
    sim_all = []
    date_all = []
    try:
        for count, val in enumerate(ob):
            date = datetime.strptime(val[0], ('%d/%m/%Y'))
            date_all.append(date)
            ob_all.append(float(val[1]))
            sim_all.append(float(sim[count]))

        nse_val = nse(ob_all, sim_all)
        return nse_val
    except Exception as e :
        print(e)
        return 0

def return_nse_soil(path):
    ob = read_the_file_split(path)
    del ob[0]
    rz = RZWQM(met_path_snow, '', simulate_path)
    sim = rz.rzwqm_res_parse('soil_T')
    ob_all = []
    sim_all = []
    date_all = []
    try:
        for count, val in enumerate(ob):
            date = datetime.strptime(val[0], ('%d/%m/%Y'))
            date_all.append(date)
            ob_all.append(float(val[1]))
            sim_all.append(float(sim[count]))

        nse_val = nse(ob_all, sim_all)
        return nse_val
    except Exception as e :
        print(e)
        return 0

#access the sample points
def return__sample_points(range, sets_of_var, numberofsets):
    n = np.array(sobol(sets_of_var, numberofsets))
    for num, set in enumerate(sets_of_var):
        n[:, num] *= diff(range[num])
    return n





