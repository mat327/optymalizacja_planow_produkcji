from tkinter import *
from tkinter import ttk
from ttkwidgets import CheckboxTreeview
import time
import os
import config

def enterSize(main_window_terminal, main_window_button1, main_window_button2, main_window_button3, config_dict):
    window = Toplevel()
    window.title("Cutting Optimization - Items List")
    window.geometry("700x350")
    window.grid_rowconfigure(4, weight=1)
    window.grid_columnconfigure(0, weight=1)

    def chechboxlist_init(): #initalization chechboxlist
        global ct
        ct = CheckboxTreeview(window, show='tree')
        i = 1
        for x, y in config_dict.items():
            if x != "0":
                ct.insert('', "end", str(x), text="Item " + str(x) + " : Length " + str(y[1]) + " mm, Amount " + str(y[0]))
                i += 1
        ct.grid(row=1, column=0, columnspan=3, rowspan=4, sticky="nsew", padx=10)

    def onclick_add_button():
        isValueCorrect = True
        try:
            if int(entry_amount.get()) <= 0:
                raise ValueError
        except ValueError:
            isValueCorrect = False
            entry_amount.delete(0, 'end') #clear entry
            entry_amount.insert(0, "Entered wrong value.") #write text to entry

        try:
            if int(entry_length.get()) <= 0:
                raise ValueError
            else: 
                if int(entry_length.get()) > config_dict['0']:
                        isValueCorrect = False
                        entry_length.delete(0, 'end') #clear entry
                        entry_length.insert(0, "Length is too long.") #write text to entry
                else:
                    for y in config_dict.values(): #cannot add new item if antoher item already has the same length
                        if type(y) == list:
                            if int(entry_length.get()) == int(y[1]):
                                isValueCorrect = False
                                entry_length.delete(0, 'end') #clear entry
                                entry_length.insert(0, "Length already exist.") #write text to entry
                                break
        except ValueError:
            isValueCorrect = False
            entry_length.delete(0, 'end') #clear entry
            entry_length.insert(0, "Entered wrong value.") #write text to entry

        if(isValueCorrect):
            i = 0
            keys = list(config_dict.keys()) 
            for x in range(len(keys)): #looking for allowed index in dict
                if str(i) in keys: #if inedx already exist
                    i+=1
                else:
                    ct.insert('', "end", str(i), text="Item " + str(i) + " : Length " + str(entry_length.get()) + " mm, Amount " + str(entry_amount.get()))
                    config_dict[str(i)] = [int(entry_amount.get()), int(entry_length.get())]
                    break
            if i == len(keys): #if dict has indexes from 0 to dict len-1, add index = dict len
                ct.insert('', "end", str(i), text="Item " + str(i) + " : Length " + str(entry_length.get()) + " mm, Amount " + str(entry_amount.get()))
                config_dict[str(i)] = [int(entry_amount.get()), int(entry_length.get())]

    def onclick_delete_button():
        checked = ct.get_checked() #get checked items
        for x in checked: #for all checked items del all records with the same indexes as checked items
            config_dict.pop(x)
        ct.destroy() #destroy checkboxlist
        chechboxlist_init() #and generate new from updated dict

    def onclick_save_button():
        window.destroy()
        config.save_config_window(main_window_terminal, main_window_button1, main_window_button2, main_window_button3, config_dict)
    
    def on_closing():
        window.destroy()
        config.save_config_window(main_window_terminal, main_window_button1, main_window_button2, main_window_button3, config_dict)

    chechboxlist_init()
    
    feet_author = Label(window, text= " Authors : M. Białek & M. Radojewski  ")
    feet_version = Label(window, text="     Version : 0.1 ")
    delete_button = Button(window, text="Delete", command=onclick_delete_button)
    add_button = Button(window, text="Add item", command=onclick_add_button)
    save_button = Button(window, text="Save to file", command=onclick_save_button)
    label_list  = Label(window, text= "Current Items List", bd=10)
    label_new = Label(window, text="New item", bd=10)
    label_amount = Label(window, text="Amount of items : ")
    label_length = Label(window, text="Items Length (mm): ")
    entry_amount = Entry(window)
    entry_length = Entry(window)

    label_list.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10)
    label_new.grid(row = 0, column=3, columnspan=2, sticky="nsew")
    label_amount.grid(row = 1, column=3, sticky="w")
    label_length.grid(row = 2, column=3, sticky="w")
    entry_amount.grid(row = 1, column=4, sticky="e", pady=10, padx=10)
    entry_length.grid(row = 2, column=4, sticky="e", pady=10, padx=10)
    delete_button.grid(row=5, column=1, pady=10, padx=10)
    add_button.grid(row=3, column=4, pady=10)
    save_button.grid(row=5, column=2, pady=10, padx=10)
    feet_author.grid(row=6, column=3, columnspan=4, sticky="e")
    feet_version.grid(row=6, column=0, columnspan=3, sticky="w")

    window.protocol("WM_DELETE_WINDOW", on_closing)