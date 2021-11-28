from tkinter import *
import time
import os
import prof_length
import items_list
import config
import optimization
from tkinter import ttk

config_dict = dict()

#Kod GUI
main_gui = Tk()
main_gui.title("Cutting Optimization")
main_gui.geometry("700x400")
main_gui.grid_rowconfigure(1, weight=1)
main_gui.grid_columnconfigure(6, weight=1)

def onclick_prof_len_button():
    prof_len_button.config(state=DISABLED)
    items_list_button.config(state=DISABLED)
    solution_button.config(state=DISABLED)
    prof_length.enterLength(terminal, prof_len_button, items_list_button, solution_button, config_dict)

def onclick_items_list_button():
    prof_len_button.config(state=DISABLED)
    items_list_button.config(state=DISABLED)
    solution_button.config(state=DISABLED)
    items_list.enterSize(terminal, prof_len_button, items_list_button, solution_button, config_dict)

def onclick_solution_button():
    prof_len_button.config(state=DISABLED)
    items_list_button.config(state=DISABLED)
    solution_button.config(state=DISABLED)
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Finding solution ...")
    main_gui.update_idletasks() #update gui over tasks in code

    optimization.optimization(terminal, prof_len_button, items_list_button, solution_button, config_dict, progress)

scrollbar = Scrollbar(main_gui, orient="vertical")
terminal = Listbox(main_gui, yscrollcommand=scrollbar.set, background="black", foreground="white")
feet_author = Label(main_gui, text= " Authors : M. Białek & M. Radojewski  ")
feet_version = Label(main_gui, text="     Version : 0.1 ")
scrollbar.config(command=terminal.yview)
prof_len_button = Button(main_gui, text="Profile Length", command = onclick_prof_len_button)
items_list_button = Button(main_gui, text="Items List", command = onclick_items_list_button)
solution_button = Button(main_gui, text="Find Solution", command = onclick_solution_button)
progress = ttk.Progressbar(main_gui, orient=HORIZONTAL, mode="determinate")

terminal.grid(row=1, column=0, columnspan=7, padx=0, pady=0, sticky="nsew")
scrollbar.grid(row=1, column=7, sticky="ns")
prof_len_button.grid(row=0, column=0, padx=5, pady=5, ipadx=10)
items_list_button.grid(row=0, column=1, padx=5, pady=5, ipadx=13)
solution_button.grid(row=0, column=2, padx=5, pady=5, ipadx=13)
feet_author.grid(row=2, column=3, columnspan=4, sticky="e")
feet_version.grid(row=2, column=0, columnspan=3, sticky="w")
progress.grid(row= 0, column=3, columnspan=4, sticky = "e", padx= 30)

config_dict = config.load_config_from_file(terminal)
#Disable solution_button if items are less than 2
if len(config_dict) <= 2:
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  To find a solution, the item list must contain at least two items.")
    terminal.itemconfig(END, fg = "yellow")
    solution_button.config(state=DISABLED)
   
main_gui.mainloop()