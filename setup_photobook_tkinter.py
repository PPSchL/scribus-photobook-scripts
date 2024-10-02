#! /usr/bin/env python3
import os
import setup_photobook
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


def changepath():
    global script_path
    script_path = filedialog.askdirectory()
    global change_path
    change_path["text"] = "Change current path to script directory: " + script_path
    os.chdir(script_path)
    return


setup_window = Tk()
setup_window.title("Setup photobook scripts for scribus")
script_path, chosen_lang, chosen_unit = (
    setup_photobook.init_after_check_previous_config()
)
chosen_lang = StringVar(value=chosen_lang)
chosen_unit = StringVar(value=chosen_unit)


explication = ttk.Label(
    setup_window,
    text="Please check path to the scripts directory (Click to change):",
)
explication.grid(row=0, column=0)


change_path = ttk.Button(
    setup_window,
    text="Change current path to script directory: " + script_path,
    command=changepath,
)
change_path.grid(row=1, column=0)


unit_label = ttk.Label(
    setup_window,
    text="Please choose your measurement unit:",
    justify="left",
)
unit_label.grid(row=2, column=0)


unit_choices = ttk.Combobox(
    setup_window,
    textvariable=chosen_unit,
    justify="left",
)
unit_choices["values"] = ("mm", "cm", "points", "inches", "picas", "ciceros")
unit_choices.grid(row=3, column=0)

language_label = ttk.Label(
    setup_window,
    text="Please choose your preferred menu language: ",
)
language_label.grid(row=4, column=0)


r1 = ttk.Radiobutton(
    setup_window, text="Français", variable=chosen_lang, value="Français"
)
r2 = ttk.Radiobutton(
    setup_window, text="Deutsch", variable=chosen_lang, value="Deutsch"
)
r3 = ttk.Radiobutton(
    setup_window, text="English", variable=chosen_lang, value="English"
)
r1.grid(row=5, column=0)
r2.grid(row=6, column=0)
r3.grid(row=7, column=0)

stop_it = Button(setup_window, text="Ok, Done", command=setup_window.destroy)
stop_it.grid(row=8, column=0)

setup_window.mainloop()

my_units = setup_photobook.select_unit(chosen_unit.get())
my_lang = chosen_lang.get()
my_msg = setup_photobook.select_msgs(my_lang)
my_defaults = setup_photobook.set_my_defaults(my_units)
setup_photobook.write_setup_files(script_path, my_lang, my_units, my_msg, my_defaults)
