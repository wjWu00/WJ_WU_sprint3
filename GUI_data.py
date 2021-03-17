import tkinter
from tkinter import *
from tkinter import messagebox
import main
import tkinter as tk
from tkinter import ttk



window = tk.Tk()  # create a new window
window.title('My GUI Data')  # window title
window.geometry('900x800')  # set up window size
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())


def call_db():
    #getting data from database
    connection, cursor = main.open_db("college_data.sqlite")
    cursor.execute(
        "INSERT INTO state_employment values('%s', '%s','%s','%s','%s')" % (state_name.get(), occupation_major.get(),
                                                                            total_emplpyment.get(),
                                                                            occupation_code.get(),
                                                                            salary_annual_25per()))
    main.close_db(connection)

state_name = StringVar()
occupation_major = StringVar()
total_emplpyment = IntVar()
occupation_code = StringVar()
salary_annual_25per = StringVar()

conn, cur = main.open_db("college_data.sqlite")
cur.execute("SELECT * FROM state_employment")
all_data = cur.fetchall()
main.close_db(conn)



# sort the data
def sort(data: list, key: int):
    sorted_data = sorted(data, key=lambda x: x[key])
    return sorted_data


def display_text(): #display data analysis
    Label(window, text='State Name').grid(row=18, column=0,padx=20)
    Label(window, text='Occupation Title').grid(row=19, column=0,padx=20)
    Label(window, text='Total Employees').grid(row=20, column=0,padx=20)
    Label(window, text='Occupation code').grid(row=21, column=0,padx=20)
    Label(window, text='Salary 25%').grid(row=22, column=0, padx=20)

    Entry(window, textvariable=state_name).grid(row=18, column=1)
    Entry(window, textvariable=occupation_major).grid(row=19, column=1)
    Entry(window, textvariable=total_emplpyment).grid(row=20, column=1)
    Entry(window, textvariable=occupation_code).grid(row=21, column=1)
    Entry(window, textvariable=salary_annual_25per).grid(row=22, column=1)
    Label(window, text='').grid(row=5, columnspan=0)

def display_list(key: int):  #display a data analysis list
    data_display = ttk.Treeview(window, columns=(1, 2, 3, 4, 5), show='headings', height='20')
    data_display.grid(row=5, columnspan=20)
    data_display.heading(1, text='State Name')
    data_display.column(1, width=130,padx=20)
    data_display.heading(2, text='Occupation Title')
    data_display.column(2, width=350)
    data_display.heading(3, text='Total Employees')
    data_display.column(3, width=95)
    data_display.heading(4, text='Occupation code')
    data_display.column(4, width=100)
    data_display.heading(5, text='Salary 25%')
    data_display.column(5, width=80)

    for row in sort(all_data, key):
        data_display.insert('', END, values=row)


def show_by_state():
    display_list(0)
def show_by_occ():
    display_list(1)
def show_by_employee():
    display_list(2)
def show_by_occCode():
    display_list(3)
def show_by_salary():
    display_list(4)

def display2():
    Label(window, text='').grid(row=7, columnspan=0)
    Label(window, text='').grid(row=9, columnspan=0)



def display_table():
#data sorting
    Button(window, text="State", height=1, width=15).grid(row=25, column=1)
    Button(window, text="Occupation", height=1, width=15).grid(row=25, column=2)
    Button(window, text="TotalEmployee", height=1, width=15).grid(row=25, column=3)
    Button(window, text="OccupationCode", height=1, width=15).grid(row=25, column=4)
    Button(window, text="Salary 25%", height=1, width=15).grid(row=25, column=5)



def messagebox():
    tkinter.messagebox.showinfo(title='Messagebox', message='You are updating your data!')



# create two buttons
tk.Button(window, text='Data sorting', font=('Arial', 20), command=display_text).place(x=500, y=30, anchor='nw')
tk.Button(window, text='Data List', font=('Arial', 20), command=display_table).place(x=500, y=80, anchor='nw')
#Button(window, text="Update", command=show).grid(row=2, column=2)
tk.Button(window, text='Exit', font=('Arial', 20), command=window.destroy).place(x=700, y=50, anchor='nw')
tk.Button(window, text='Messagebox', font=('Arial', 20), command=messagebox).place(x=700, y=100, anchor='nw')
#tk.Button(window, text="Exit", command=quit).grid(row=4, column=5)

window.mainloop()
