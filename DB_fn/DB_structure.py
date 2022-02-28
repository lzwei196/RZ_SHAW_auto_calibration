import mysql.connector
from mysql.connector import errorcode
from snow_depth_project.project_db_connect import cursor

DB_name = 'snow_depth_project'

Table = {}

Table['downloaded_eccc_data'] = (
    "CREATE TABLE `downloaded_eccc_data`("
    "`id` int(11) NOT NULL AUTO_INCREMENT,"
    "`file_name` LONGTEXT NOT NULL,"
    "`file_location` LONGTEXT NOT NULL ,"
    "`station_id` TEXT NOT NULL ,"
    "`year` int(4) NOT NULL ,"
    "PRIMARY KEY (`id`))"
    "ENGINE =InnoDB"
)

Table['snow_sobol_test'] = (
    "CREATE TABLE `snow_sobol_test`("
    "`id` int(11) NOT NULL AUTO_INCREMENT,"
    "`avg_snow` float NOT NULL ,"
    "`init_snow` float NOT NULL ,"
    "`NSE` float NOT NULL ,"
    "PRIMARY KEY (`id`))"
    "ENGINE =InnoDB"
)

Table['soil_temp_test'] = (
    "CREATE TABLE `snow_sobol_test`("
    "`id` int(11) NOT NULL AUTO_INCREMENT,"
    "`bubble` float NOT NULL ,"
    "`ksat` float NOT NULL ,"
    "`wet` float NOT NULL ,"
    "`dry` float NOT NULL ,"
    "`NSE` float NOT NULL ,"
    "PRIMARY KEY (`id`))"
    "ENGINE =InnoDB"
)

def create_tables():
    cursor.execute("USE {}".format(DB_name))
    for table_name in Table:
        table_description = Table[table_name]
        try:
            # print(table_description)
            print("creating table ({})".format(table_name), end="")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table alreayd exists")
            else:
                print(err.msg)


create_tables()