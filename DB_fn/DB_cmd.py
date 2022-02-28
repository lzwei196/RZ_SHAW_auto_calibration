from snow_depth_project.project_db_connect import cursor, db
import json
import os

######add delete action
def add_downloaded_data(file_name, file_location, station_id, year):
    sql = "INSERT INTO `downloaded_eccc_data`(file_name, file_location, station_id, year) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (file_name, file_location, station_id, year))
    db.commit()
    id = cursor.lastrowid
    print("Added element{}".format(id))

def add_snow_test_res(avg_snow, init_snow, nse):
    sql = "INSERT INTO `snow_sobol_test`(avg_snow, init_snow, nse) VALUES (%s, %s, %s)"
    cursor.execute(sql, (avg_snow, init_snow, nse))
    db.commit()
    id = cursor.lastrowid
    print("Added element{}".format(id))

#####select action
def select_dl_eccc_data(year, station_id):
    try:
        sql = "SELECT `file_location` FROM `downloaded_eccc_data` WHERE station_id = ('{}') AND year = ('{}')".format(station_id, year)
        #print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(e)
