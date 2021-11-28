from tkinter import *
from PIL import ImageTk, Image
import time
import os
import config

def enterLength(main_window_terminal, main_window_button1, main_window_button2, main_window_button3, config_dict):
    window = Toplevel()
    window.title("Cutting Optimization - Profile Length")
    window.geometry("700x350")
    window.grid_rowconfigure([3], weight=1)
    window.grid_columnconfigure([2], weight=1)

    def onclick_enter_button():
        isValueCorrect = True
        try:
            if int(length_entry.get()) <= 0:
                raise ValueError
            else:
                length_test = list()
                for x in range (1, len(config_dict)):
                    length_test.append(int(config_dict[str(x)][1]))
                if max(length_test) > int(length_entry.get()):
                    length_entry.delete(0, 'end') #clear entry
                    length_entry.insert(0, "Profile length too short.") #write text to entry
                    isValueCorrect = False
        except ValueError:
            isValueCorrect = False
            length_entry.delete(0, 'end') #clear entry
            length_entry.insert(0, "Entered wrong value.") #write text to entry

        if(isValueCorrect):
            config_dict['0'] = int(length_entry.get())
            sec = time.localtime() # get struct_time
            main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  New profile length saved "+ str(config_dict['0']) + " mm.")
            window.destroy()
            config.save_config_window(main_window_terminal, main_window_button1, main_window_button2, main_window_button3, config_dict)

    def on_closing():
        sec = time.localtime() # get struct_time
        main_window_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Setting new profile length not completed. The current length is still "+ str(config_dict['0']) + " mm.")
        main_window_terminal.itemconfig(END, fg = "yellow")
        main_window_button1.config(state=NORMAL)
        main_window_button2.config(state=NORMAL)
        main_window_button3.config(state=NORMAL)
        window.destroy()

    length_label = Label(window, text="Profile length (mm) : ")
    length_entry = Entry(window)
    enter_button = Button(window, text="    Enter   ", command=onclick_enter_button)

    global img #images must be global to work
    img = ImageTk.PhotoImage(Image.open("profile_length.gif"))  
    img_label=Label(window, image=img)

    feet_authors = Label(window, text= " Authors : M.Białek & M.Radojewski    ")
    feet_version = Label(window, text="     Version : 0.1 ")

    length_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
    length_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nw")
    enter_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n")
    img_label.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="new")
    feet_authors.grid(row=4, column=1, columnspan=2, sticky="e")
    feet_version.grid(row=4, column=0, sticky="w")

    length_entry.insert(0, str(config_dict['0']))

    window.protocol("WM_DELETE_WINDOW", on_closing)