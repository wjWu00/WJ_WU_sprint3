import requests
import secrets
import sqlite3
import xlrd
import sys
from importlib import reload
reload(sys)
from typing import Tuple


def get_data():
    all_data = []
    response = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant='
                            f'2,3&fields=id,school.state,school.name,2018.student.size,2016.repayment.3_yr_repayment.overall,'
                            f'2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line&api_key={secrets.api_key}')
    first_page = response.json()
    if response.status_code != 200:
        print(F"Error Getting Data from API: {response.raw}")
        return []
    total_results = first_page['metadata']['total']
    page = 0
    per_page = first_page['metadata']['per_page']
    all_data.extend(first_page['results'])
    while (page+1)*per_page < total_results:
        page += 1
        response = requests.get(
            f'https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,school.'
            f'state,school.name,2018.student.size,2016.repayment.3_yr_repayment.overall,2017.earnings.3_yrs_after_completion.'
            f'overall_count_over_poverty_line&api_key={secrets.api_key}&page={page}')
        if response.status_code != 200:  # if we didn't get good data keep going
            continue
        current_page = response.json()
        all_data.extend(current_page['results'])

    return all_data

def open_excel(file='state_M2019_dl.xlsx'):
    try:
        excel_data = xlrd.open_workbook(file)  # open excel file
        print(sys.getsizeof(excel_data))
        return excel_data
    except:
        print("open excel file failed!")


def excel_table(file='', colindex=[0], table_name='State_M2019_dl'):
    data = open_excel(file)
    table = data.sheet_by_name(table_name)  # get the sheet form excel file
    nrows = table.nrows  # get the numbers of rows
    t_name = table.row_values(0)[0].encode('utf8') #the name of the table
    colnames = table.row_values(1)  # get the value of the first col as key value
    list = []

    list.append(t_name)
    list.append(colnames)
    for rownum in range(2, nrows): #get the from second row
        row = table.row_values(rownum)
        if row:
            app = []
            for i in colindex:
                app.append(str(row[i]).encode("utf-8"))
            list.append(app)
    return list



def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


def setup_schools_table(cursor: sqlite3.Cursor):
    cursor.execute('''DROP TABLE IF EXISTS  schools''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS schools(
    school_id INTEGER PRIMARY KEY,
    school_name TEXT NOT NULL,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER,
    student_size_2017 INTEGER,
    earnings_2017 INTEGER,
    repayment_2016 INTEGER
    );''')


def setup_state_table(cursor: sqlite3.Cursor):
    cursor.execute('''DROP TABLE IF EXISTS  state_employment''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS state_employment( 
    state_name TEXT NOT NULL PRIMARY KEY,
    occupation_major TEXT NOT NULL,
    total_emplpyment INTEGER,
    25th_percentile_salary_hourly INTEGER,
    25th_percentile_salary_annual INTEGER,
    occupation_code TEXT NOT NULL
    );''')


def insert_schools_data(all_data, cursor):
    for univ_data in all_data:
        cursor.execute("""INSERT INTO SCHOOLS(school_id, school_name,school_state,student_size_2018,student_size_2017,
        earnings_2017,repayment_2016)
         VALUES (?,?,?,?,?,?,?);
        """, (univ_data['id'], univ_data['school.name'], univ_data['school.state'], univ_data['2018.student.size'], univ_data['2017.student.size'],
              univ_data['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
              univ_data['2016.repayment.3_yr_repayment.overall']))


def main(file_name,colindex):
    all_data = get_data()
    conn, cursor = open_db("college_data.sqlite")
    setup_schools_table(cursor)
    setup_state_table(cursor)
    close_db(conn)
    tables = excel_table(file_name,colindex, table_name='State_M2019_dl')
    t_name = tables.pop(0)
    key_list = ','.join(tables.pop(0)).encode('utf8')   #list transfer to str
    sql_line = "INSERT INTO "+t_name+"（"+key_list+"）VALUE"
    line = ''
    for info in tables:
        content = ','.join(info)
        if line != '':
            line =line + ',(' + content + ')'
        else:
            line = '('+content+')'
    sql_line = sql_line + line + ';'
    with open('college_data.sqlite', 'w') as f:  # open sql file and write the file in lines
        f.write(sql_line)


if __name__ == '__main__':
    file_name = 'state_M2019_dl.xlsx' #put in excel file
    colindex = [1, 9, 10, 19, 25, 7]      #add the colinindex which you want.
    main(file_name,colindex)