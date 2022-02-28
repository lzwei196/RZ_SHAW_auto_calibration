from mysql_connect import cursor, db
import json
import os
from csv_parsing import read_the_file_split


#############DB general sql

def db_dly_date_data(name):
    sql = (
        "CREATE TABLE `{}`("
        "`date_data_id` int(11) NOT NULL AUTO_INCREMENT,"
        "`year_id` int(11) NOT NULL,"
        "`station_id` TEXT NOT NULL,"
        "`elementnum` CHAR(3) NOT NULL,"
        "`month` int(2) NOT NULL ,"
        "PRIMARY KEY (`date_data_id`),"
        "FOREIGN KEY(`year_id`) REFERENCES `years_for_each_element`(year_id)"
        ") ENGINE = InnoDB".format(name)
    )
    return sql


def db_dly_value(name):
    sql = (
        "CREATE TABLE `{}`("
        "`data_id` int(11) NOT NULL AUTO_INCREMENT,"
        "`date_data_id` int(11) NOT NULL,"
        "`dayinthemonth` int(2) NOT NULL,"
        "`value` LONGTEXT NOT NULL ,"
        "PRIMARY KEY (`data_id`),"
        "FOREIGN KEY(`date_data_id`) REFERENCES `{}`(`date_data_id`)"
        ")ENGINE = InnoDB".format(name, name + "_date_id")
    )
    return sql


###############################add delete actions

def add_env_element(element_code, variable_name):
    sql = "INSERT INTO `env variables`(element_code, variable_name) VALUES (%s, %s)"
    cursor.execute(sql, (element_code, variable_name))
    db.commit()
    id = cursor.lastrowid
    # print("Added elements{}".format(id))


def add_env_element_all():
    data = read_jsonfile("env_elements.json")
    for key, val in data.items():
        add_env_element(key, val)


def add_element_years(element_id, year):
    sql = "INSERT INTO `years_for_each_element`(element_id, year) VALUES (%s, %s)"
    cursor.execute(sql, (element_id, year))
    db.commit()
    id = cursor.lastrowid
    # print("Added elements{}".format(id))


def add_env_dly_date_data(year_id, station_id, month, elementnum):
    sql = "INSERT INTO `env_dly_date_data`(year_id,station_id,month, elementnum) VALUES (%s, %s, %s, %s)"
    # sql = f"INSERT INTO {} (year_id, station_id,month,elementnum) VALUES ({},{},{},{})".format(name,)
    cursor.execute(sql, year_id, station_id, month, elementnum)
    # cursor.execute(sql)
    db.commit()
    id = cursor.lastrowid
    # print("Added elements{}".format(id))
    return id


def add_dly_value(date_data_id, dayinthemonth, value):
    sql = "INSERT INTO `dly_value`(date_data_id,dayinthemonth,value) VALUES (%s, %s, %s)"
    cursor.execute(sql, (date_data_id, dayinthemonth, value))
    db.commit()
    id = cursor.lastrowid
    # print("Added elements{}".format(id))


def sql_execute(thefunc):
    def wrapper(**kwargs):
        sql = thefunc(**kwargs)
        cursor.execute(sql, (kwargs['year_id'], kwargs['station_id'], kwargs['month'], kwargs['elementnum']))
        db.commit()
        id = cursor.lastrowid
        # print("Added elements{}".format(id))
        return id

    return wrapper


def sql_execute_with_val(thefunc):
    def wrapper(**kwargs):
        sql = thefunc(**kwargs)
        cursor.execute(sql, (kwargs['date_data_id'], kwargs['dayinthemonth'], kwargs['value']))
        db.commit()
        id = cursor.lastrowid
        # print("Added elements{}".format(id))
        return id

    return wrapper


@sql_execute
def add_dly_date_data_builder(**kwargs):
    sql = f"INSERT INTO {kwargs['name']} (year_id, station_id, month, elementnum) " \
          f"VALUES (%s, %s, %s, %s)"
    # print(sql)
    return sql


@sql_execute_with_val
def add_dly_value_builder(**kwargs):
    sql = f"INSERT INTO {kwargs['name']} (date_data_id,dayinthemonth,value) VALUES (%s, %s, %s)"
    # print(sql)
    return sql


def add_station_id_val(**kwargs):
    sql = f"INSERT INTO `station_id` (name, province, climate_id, station_id, latitude, longitude, elevation)  VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # print(sql)
    cursor.execute(sql, (
    kwargs['name'], kwargs['province'], kwargs['climate_id'], kwargs['station_id'], kwargs['latitude'],
    kwargs['longitude'], kwargs['elevation']))
    db.commit()
    id = cursor.lastrowid
    print("Added elements{}".format(id))
    return id


def add_station_years(**kwargs):
    sql = "INSERT INTO `station_data_years` (station_id, first_year, last_year, hly_first_year, hly_last_year, " \
          "dly_first_year, dly_last_year, mly_first_year, mly_last_year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
    cursor.execute(sql, (
    kwargs['station_id'], kwargs['first_year'], kwargs['last_year'], kwargs['hly_first_year'], kwargs['hly_last_year'],
    kwargs['dly_first_year'], kwargs['dly_last_year'], kwargs['mly_first_year'], kwargs['mly_last_year']))
    db.commit()
    id = cursor.lastrowid
    print("Added elements{}".format(id))
    return id


############################################### select actions
def sql_execute_select(thefunc):
    def wrapper(*args):
        sql = thefunc(args)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    return wrapper()


def select_the_elementid(element):
    try:
        sql = ("SELECT element_id FROM `env variables` WHERE element_code = ('{}')".format(element))
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(e)


def select_the_station_year_dly(station_id):
    try:
        sql = ("SELECT dly_first_year, dly_last_year FROM station_data_years WHERE  station_id = ('{}')".format(
            station_id))
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(e)


def select_the_yearid(year, element):
    sql = ("SELECT year_id FROM years_for_each_element WHERE year = ('{}')  AND element_id = ('{}') ".format(year,
                                                                                                             element))
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


# @sql_execute_select
def select_general_station_id(*args):
    field = args[0]
    val = args[1]
    sql = f"SELECT * FROM station_id WHERE {field} = '{val}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# document actions

def read_jsonfile(path):
    with open("{}".format(path)) as f:
        elements = json.load(f)
    return elements


# returns the list of the values for each line
def split_functions(s):
    final_obj = {}
    splitted = s.split()
    prefix = splitted[0]
    final_obj['station_id'] = prefix[0:7]
    final_obj['year'] = prefix[7:11]
    final_obj['month'] = prefix[11:13]
    final_obj['elementnum'] = prefix[13:16]
    value_obj = [{'day': '1', 'value': prefix[16:23]}]
    del splitted[0]
    value_obj.extend(split_for_value(splitted))
    final_obj['values'] = value_obj
    return final_obj


###return the values with days in an array
def split_for_value(line):
    value_obj = []
    for i, val in enumerate(line):
        value_obj.append({'day': i + 2, "value": val})
    return value_obj


def read_years_in_dir(path, elementid):
    path_to_data_folder = path
    years = []
    for file in os.listdir(path_to_data_folder):
        if file.endswith(".txt"):
            year = file[11:15]
            add_element_years(elementid, year)
            years.append(year)
    return years


def read_file_path__in_dir(path):
    path_to_data_folder = path
    all_path = []

    for file in os.listdir(path_to_data_folder):
        if file.endswith(".txt"):
            the_path = os.path.join(path, file)
            all_path.append(the_path)

    return all_path


def read_file_path_in_dir_custom(path, extension):
    path_to_data_folder = path
    all_path = []
    for file in os.listdir(path_to_data_folder):
        if file.endswith(extension):
            # the_path = os.path.join(path, file)
            all_path.append(file)

    return all_path

def value_string_to_num(s):
    if s == '000000' or s == '-99999M':
        return 999
    else:
        res = int(s.strip('0'))/10
        return res
