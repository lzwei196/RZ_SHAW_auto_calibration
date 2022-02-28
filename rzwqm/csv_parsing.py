import csv
def read_the_file_split(path):
    parsed_data_all =[]
    with open(path, 'r') as f:
        for row in csv.reader(f, delimiter=','):
            parsed_data_all.append(row)
    return parsed_data_all


def read_the_file_split_text(path):
    with open(path, 'r') as f:
        content = [str(line).strip().split() for line in f]

    return content

