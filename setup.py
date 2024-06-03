#! /usr/bin/env python3
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


def select_language(lang_val):
    if lang_val == "Français":
        my_msg = {
            "ti_img_x": "Images en largeur",
            "msg_img_x": "Entrez le nombre d'images en largeur:",
            "ti_img_y": "Images en hauteur",
            "msg_img_y": "Entrez le nombre d'images en hauteur:",
            "ti_gutter": "Gouttière",
            "msg_gutter": "Entrez la distance entre images:",
            "ti_1_img": "Image unique",
            "msg_1_img": "Entrez la position (coordonnées) de l'image:",
            "ti_g_type": "Type de groupe",
            "msg_g_type": "             Entrez la valeur:\n- normal=0,\n- central=1,\n- double=2,\n- page entière=3",
            "ti_x_error": "Erreur de la valeur x",
            "msg_x_error": "Valeur x trop élevée!",
            "ti_y_error": "Erreur de la valeur y",
            "msg_y_error": "Valeur y trop élevée!",
        }
    elif lang_val == "Deutsch":
        my_msg = {
            "ti_img_x": "Bilder in der Breite",
            "msg_img_x": "Anzahl Bilder in der Breite eingeben:",
            "ti_img_y": "Bilder in der Höhe",
            "msg_img_y": "Anzahl BIlder in der Höhe eingeben:",
            "ti_gutter": "Spaltenzwischenraum",
            "msg_gutter": "Distanz zwischen Bildern eingeben:",
            "ti_1_img": "Einzelbild",
            "msg_1_img": "Position (Koordinaten) des Bildes eingeben:",
            "ti_g_type": "Typ der Bildergruppe",
            "msg_g_type": "             Wert eingeben:\n- normal=0,\n- zentral=1,\n- doppelt=2,\n- ganze Seite=3",
            "ti_x_error": "X Wert fehlerhaft",
            "msg_x_error": "X Wert zu hoch!",
            "ti_y_error": "Y Wert fehlerhaft",
            "msg_y_error": "Y Wert zu hoch!",
        }
    else:  # English as default possibility
        my_msg = {
            "ti_img_x": "Images per row",
            "msg_img_x": "Enter the number of images per row:",
            "ti_img_y": "Images per column",
            "msg_img_y": "Enter the number of images per column:",
            "ti_gutter": "Gutter",
            "msg_gutter": "Enter distance between images:",
            "ti_1_img": "Single image",
            "msg_1_img": "Enter image position (coordinates):",
            "ti_g_type": "Group type",
            "msg_g_type": "             Enter the type:\n- normal=0,\n- central=1,\n- double=2,\n- whole page=3",
            "ti_x_error": "X value error",
            "msg_x_error": "X value higher than no. of images per row!",
            "ti_y_error": "Y value error",
            "msg_y_error": "Y value higher than no. of images per column!",
        }
    return my_msg


def select_unit(chosen_unit):
    if chosen_unit == "cm":
        my_units = scribus.UNIT_CENTIMETRES
    elif chosen_unit == "inches":
        my_units = scribus.UNIT_INCHES
    elif chosen_unit == "points":
        my_units = scribus.UNIT_POINTS
    elif chosen_unit == "picas":
        my_units = scribus.UNIT_PICAS
    elif chosen_unit == "ciceros":
        my_units = scribus.UNIT_CICERO
    else:  # mm by default
        my_units = scribus.UNIT_MILLIMETERS
    return my_units


def changepath():
    global script_path
    script_path = filedialog.askdirectory()
    global change_path
    change_path["text"] = "Change current path to script directory: " + script_path
    os.chdir(script_path)
    return


setup_window = Tk()
setup_window.title("Setup photobook scripts for scribus")

explication = ttk.Label(
    setup_window,
    text="Please check path to the scripts directory (Click to change):",
)
explication.grid(row=0, column=0)


script_path = os.getcwd()
change_path = ttk.Button(
    setup_window,
    text="Change current path to script directory: " + script_path,
    command=changepath,
)
change_path.grid(row=1, column=0)

# show_path = ttk.Label(setup_window, text="current path:" + script_path)
# show_path.grid(row=1, column=0)

unit_label = ttk.Label(
    setup_window,
    text="Please choose your measurement unit:",
    justify="left",
)
unit_label.grid(row=2, column=0)

chosen_unit = StringVar(value="mm")
unit_choices = ttk.Combobox(
    setup_window,
    textvariable=chosen_unit,
    justify="left",
)
unit_choices["values"] = ("mm", "cm", "points", "inches", "picas", "ciceros")
unit_choices.grid(row=3, column=0)
# chosen_lang = StringVar(value="Français")
# lang_choices = ttk.Combobox(setup_window, textvariable=chosen_lang)
# lang_choices["values"] = ("Français", "English", "Deutsch")
# lang_choices.grid(row=1, column=0)
language_label = ttk.Label(
    setup_window,
    text="Please choose your preferred menu language: ",
)
language_label.grid(row=4, column=0)

chosen_lang = StringVar(value="Français")
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


my_units = select_unit(chosen_unit)
my_msg = select_language(chosen_lang)

setup_window.mainloop()
print(chosen_unit.get(), "   ", chosen_lang.get(), "  ", script_path)
