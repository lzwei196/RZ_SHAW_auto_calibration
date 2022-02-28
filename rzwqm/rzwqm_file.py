from datetime import datetime, timedelta
import os



class RZWQM:

    def __init__(self, met_path, brk_path, simulate_path, rzwqm_project_path=None):
        self.met_path = met_path
        self.brk_path = brk_path
        self.rzwqm_project_path = rzwqm_project_path
        self.simulate_path = simulate_path

    def rzwqm_res_parse(self, var_name):
        # this function is to parse the rzwqm result, and return only the required column as list
        # should have a list for corresponding var's column number
        # for snow, it should be 91
        if var_name == 'snow':
            column_num = 91
        lines = read_text_file(self.simulate_path)
        # result starts at index #23
        lines = lines[23:]
        desired_data = []
        for line in lines:
            desired_data.append(float((line[column_num])))
        return desired_data

    def rzwqm_met_parse(self):
        # this function parses the met file
        with open(self.met_path) as f:
            lines = [line.rstrip('\n') for line in f]
        head = lines[0:36]
        content = lines[36:]
        parsed_content = []
        for line in content:
            split_line = line.split()
            parsed_content.append(split_line)
        return {'head': head, 'parsed_content': parsed_content}


    def rzwqm_general_text_parse(self, out_file_name, head_end):
        path = os.path.join(self.rzwqm_project_path, out_file_name)
        with open(path) as f:
            lines = [line.rstrip('\n') for line in f]
        head = lines[0:head_end]
        content = lines[head_end:]
        parsed_content = []
        for line in content:
            split_line = line.split()
            parsed_content.append(split_line)
        return {'head': head, 'parsed_content': parsed_content}

    @staticmethod
    def change_param_val_in_one_line(columns_with_val, line):
        changed = line.split()
        for val in columns_with_val.keys():
            changed[val] = columns_with_val[val]
        return changed

    @staticmethod
    def rzwqm_parse_layer(desired_depth, layer_content):
        return_obj = {}
        for data in layer_content:
            if int(data[1]) in desired_depth:
                if return_obj[int(data[1])]:
                    return_obj[int(data[1])].append(data)
            else:
                return_obj[int(data[1])] = []
                return_obj[int(data[1])].append(data)
        return return_obj
