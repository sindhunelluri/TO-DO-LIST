#importing the required modules
import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

#defining the function to add tasks
def add_task():
    task_string = task_field.get()
    if len(task_string)==0:
        messagebox.showinfo('Error!','Field is Empty')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string ,))
        list_update()
        task_field.delete(0,'end')
#definig the function to update tasks
def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)
#defining the functions to delete a task
def delete_task():
    try:
        the_value=task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title=?',(the_value,))
    except:
        messagebox.showerror('OOPS!','No Task Selected Cannot Delete')
#defining the functions to delete all tasks
def delete_all_tasks():
    message_box=messagebox.askyesno('Delete All','Are You Sure ?')
    if message_box==True:
        while (len(tasks)!=0):
            tasks.pop()
        the_cursor.execute('delete from tasks')
        list_update()
#defining the functions to clear list
def clear_list():
    task_listbox.delete(0, 'end')
def close():
    print(tasks)
    guiWindow.destroy()
def retrieve_database():
    while(len(tasks) != 0):
        tasks.pop()
    for row in the_cursor.execute('Select title from tasks'):
        tasks.append(row[0])
#main function
if __name__ == "__main__":
    guiWindow=tk.Tk()
    guiWindow.title("TO-DO-LIST")
    guiWindow.geometry("500x500")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="pink")
    the_connection=sql.connect('listOfTasks.db')
    the_cursor=the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')
    tasks=[]
    #defining frames
    header_frame=tk.Frame(guiWindow,bg="plum")
    functions_frame=tk.Frame(guiWindow,bg="plum")
    listbox_frame=tk.Frame(guiWindow,bg="plum")
    #placing frames in the app
    header_frame.pack(fill="both")
    functions_frame.pack(side="left",expand=True,fill="both")
    listbox_frame.pack(side="right",expand=True,fill="both")
    #defining labels
    header_label=ttk.Label(header_frame,text="The TO-DO-LIST",font=("lucida handwriting",'30'),background="plum",foreground="Navy")
    header_label.pack(padx=20,pady=20)
    task_label=ttk.Label(functions_frame,text="Enter Task To Perform :",font=("calibri","15","bold"),background="plum",foreground="#000000")
    task_label.place(x=30,y=55)
    task_field=ttk.Entry(functions_frame,font=("calibri","12"),width=30,background="Black",foreground="DarkBlue")
    task_field.place(x=30,y=100)
    #adding buttons
    add=ttk.Button(functions_frame,text="Add Task",width=26,command=add_task)
    add.place(x=30,y=140)
    delete=ttk.Button(functions_frame,text="Delete Task",width=26,command=delete_task)
    delete.place(x=30,y=180)
    delete_all=ttk.Button(functions_frame,text="Delete All",width=26,command=delete_all_tasks)
    delete_all.place(x=30,y=220)
    exit=ttk.Button(functions_frame,text="Exit",width=26,command=close)
    exit.place(x=30,y=260)
    task_listbox=tk.Listbox(listbox_frame,width=30,height=20,selectmode="SINGLE",background="Purple",foreground="White",selectbackground="plum",selectforeground="Black")
    task_listbox.place(x=30,y=30)
    retrieve_database()
    list_update()
    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()