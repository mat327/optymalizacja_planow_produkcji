from tkinter import *
import time
import os
import json

def load_config_from_file(main_window_terminal):
    sec = time.localtime() # get struct_time
    main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Checking config file ...")
    filesize = os.path.getsize("config.json") #size of file
    if filesize == 0: #if file is empty
        main_window_terminal.insert(END, "The file is empty.")
        config_dict = dict()
        return config_dict
    else:
        main_window_terminal.insert(END, "Opening config file ...")
        try:
            config_file = open("config.json", "r")
            bot_config_dict_str = config_file.read() #read file as a str
            config_dict = json.loads(bot_config_dict_str) #str to dic
            config_file.close()
            main_window_terminal.insert(END, "Data loaded to program memory, file closed.")
            return config_dict
        except:
            main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  [Error] Cannot open config file.")
            main_window_terminal.itemconfig(END, fg = "red")
            config_dict = dict()
            return config_dict

def write_config_to_file(config_dict, main_window_terminal):
    try:
        config_file = open("config.json", "w")
        json.dump(config_dict, config_file)
        config_file.close()
        sec = time.localtime()
        main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Config file updated, file closed.")
    except:
        sec = time.localtime()
        main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  [Error] Cannot rewritte config file.")
        main_window_terminal.itemconfig(END, fg = "red")

def save_config_window(main_window_terminal, main_window_button1, main_window_button2, main_window_button3, config_dict):
    save_config_windows = Toplevel()
    save_config_windows.title("Cutting Optimization - Save config to file")
    save_config_windows.grid_rowconfigure(1, weight=1)
    save_config_windows.grid_columnconfigure(1, weight=1)
    save_config_windows.grid_columnconfigure(0, weight=1)
    ask = Label(save_config_windows, text="Do you want save configuration to file ?")

    def onclick_yes_button():
        write_config_to_file(config_dict, main_window_terminal)
        main_window_button1.config(state=NORMAL)
        main_window_button2.config(state=NORMAL)
        #Disable solution_button if items are less than 2
        if len(config_dict) <= 2:
            sec = time.localtime() # get struct_time
            main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  To find a solution, the item list must contain at least two items.")
            main_window_terminal.itemconfig(END, fg = "yellow")
            main_window_button3.config(state=DISABLED)
        else:
            main_window_button3.config(state=NORMAL) 
        save_config_windows.destroy()
    
    def onclick_no_button():
        sec = time.localtime() # get struct_time
        main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Current changes saved in cache memory. After reopen the program changes will be lost.")
        main_window_terminal.itemconfig(END, fg = "yellow")
        main_window_button1.config(state=NORMAL)
        main_window_button2.config(state=NORMAL)
        #Disable solution_button if items are less than 2
        if len(config_dict) <= 2:
            sec = time.localtime() # get struct_time
            main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  To find a solution, the item list must contain at least two items.")
            main_window_terminal.itemconfig(END, fg = "yellow")
            main_window_button3.config(state=DISABLED)
        else:
            main_window_button3.config(state=NORMAL)
        save_config_windows.destroy()

    def on_closing():
        sec = time.localtime() # get struct_time
        main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Current changes saved in cache memory. After reopen the program changes will be lost.")
        main_window_terminal.itemconfig(END, fg = "yellow")
        main_window_button1.config(state=NORMAL)
        main_window_button2.config(state=NORMAL)
        #Disable solution_button if items are less than 2
        if len(config_dict) <= 2:
            sec = time.localtime() # get struct_time
            main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  To find a solution, the item list must contain at least two items.")
            main_window_terminal.itemconfig(END, fg = "yellow")
            main_window_button3.config(state=DISABLED)
        else:
            main_window_button3.config(state=NORMAL)
        save_config_windows.destroy()

    yes_button = Button(save_config_windows, text="    YES   ", command=onclick_yes_button)
    no_button = Button(save_config_windows, text="    NO   ", command=onclick_no_button)
    ask.grid(row = 0, column=0, columnspan=2, pady=5, padx=5)
    yes_button.grid(row = 1, column=0, pady=5, padx=15, sticky="en")
    no_button.grid(row = 1, column=1, pady=5, padx=15, sticky="wn")

    #save_config_windows.mainloop()
    save_config_windows.protocol("WM_DELETE_WINDOW", on_closing)