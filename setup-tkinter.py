#! /usr/bin/env python3
import os
import pickle
from scribus_paul import get_config_data
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


def set_defaults():
    script_path = os.getcwd()
    chosen_lang = StringVar(value="Français")
    chosen_unit = StringVar(value="mm")
    return (script_path, chosen_lang, chosen_unit)


def set_my_defaults(my_units):
    my_defaults = {
        "bleed": 5.0,
        "xn": 2,
        "yn": 3,
        "gutter": 3,
        "xn_split": 2,
        "yn_split": 2,
        "gutter_split": 1.0,
        "asym_n-lines": 3,
        "asym_ratio": "4/3",
        "asym_gutter": 3.0,
        "asym_direction": "left2right",
        "asym_aspect": "constant",
        "acta_gutter": 3.0,
    }
    conversion_factor = {
        scribus.UNIT_CENTIMETRES: 0.1,
        scribus.UNIT_INCHES: 1 / 25.4,
        scribus.UNIT_POINTS: 1 / 25.4 * 72,
        scribus.UNIT_PICAS: 1 / 25.4 * 6,
        scribus.UNIT_CICERO: 1 / 4.51165812456,
    }
    n_digits4unit = {
        # target a precision of 1/100 of a pt (300 dpi=>~ 4 dots/point)
        scribus.UNIT_CENTIMETRES: 4,
        scribus.UNIT_INCHES: 4,
        scribus.UNIT_POINTS: 2,
        scribus.UNIT_PICAS: 3,
        scribus.UNIT_CICERO: 3,
    }
    if my_units != scribus.UNIT_MILLIMETERS:
        for dkey in ("bleed", "gutter", "gutter_split", "asym_gutter", "acta_gutter"):
            my_defaults[dkey] = round(
                conversion_factor[my_units] * my_defaults[dkey], n_digits4unit[my_units]
            )

    return my_defaults


# def init_after_check_previous_config():
#     # check whether previous config exists, if yes get data from it for initialization
#     # if not initialize with default french values :-)

#     # scribus stores units as int, need way to convert to name
#     # could have used list, but dictionary allows future use of non-contiguous values
#     int2Unit = {0: "points", 1: "mm", 2: "inches", 3: "picas", 4: "cm", 5: "ciceros"}

#     try:
#         from script_path import script_path


#         """ current working directory of scribus python is not the script directory!
#         but scribus python imports from the script directory, import is thus an
#         indirect (and the only?) way of getting the script_path and using it"""
#     except:
#         # script_path not yet defined => initialize by default values
#         script_path, chosen_lang, chosen_unit = set_defaults()
#     else:
#         cfgpath = os.path.join(script_path, ".photobook", "phb.cfg")
#         if os.path.isfile(cfgpath):
#             # config file exist => read
#             my_lang, my_msg, my_units, my_defaults = get_config_data(script_path)
#             chosen_lang = StringVar(value=chosen_lang)
#             chosen_unit = StringVar(value=chosen_unit)
#         else:
#             # script_path ok, but no config file => initialize by default values
#             script_path, chosen_lang, chosen_unit = set_defaults()
#     return (script_path, chosen_lang, chosen_unit)
def init_after_check_previous_config():
    # check whether previous config exists, if yes get data from it for initialization
    # if not initialize with default french values :-)

    # scribus stores units as int, need way to convert to name
    # could have used list, but dictionary allows future use of non-contiguous values
    int2Unit = {0: "points", 1: "mm", 2: "inches", 3: "picas", 4: "cm", 5: "ciceros"}

    try:
        from script_path import script_path

        """ current working directory of scribus python is not the script directory!
        but scribus python imports from the script directory, import is thus an
        indirect (and the only?) way of getting the script_path and using it"""
    except:
        # script_path not yet defined => initialize by default values
        script_path, chosen_lang, chosen_unit = set_defaults()
    else:
        cfgpath = os.path.join(script_path, ".photobook", "phb.cfg")
        if os.path.isfile(cfgpath):
            # config file exist => read
            my_lang, my_msg, my_units, my_defaults = get_config_data(script_path)
            chosen_lang = my_lang
            chosen_unit = int2Unit[my_units]
        else:
            # script_path ok, but no config file => initialize by default values
            script_path, chosen_lang, chosen_unit = set_defaults()
    return (script_path, chosen_lang, chosen_unit)


def select_msgs(lang_val):
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
            "ti_g_pos": "Position du nouveau groupe",
            "msg_g_pos": "Entrez la valeur, 1=top, etc:",
            "ti_ratio_error": "Erreur de rapport image",
            "msg_ratio_error": "Image trop large!",
            "ti_nlines": "Lignes d'images",
            "msg_nlines": "Entrez le nombre de lignes d'images",
            "ti_ratio": "Rapport d'image",
            "msg_ratio": "Entrez le rapport d'image, typiquement 3/2 ou 4/3:",
            "ti_direction": "Direction",
            "msg_direction": "Entrez la direction, typiquement de gauche à droite, "
            "left2right"
            "",
            "ti_aspect": "Aspect de la page",
            "msg_aspect": "Entrez le type, typiquement constant, toutes les grandes images du même côté:",
        }
    elif lang_val == "Deutsch":
        my_msg = {
            "ti_img_x": "Bilder in der Breite",
            "msg_img_x": "Anzahl Bilder in der Breite eingeben:",
            "ti_img_y": "Bilder in der Höhe",
            "msg_img_y": "Anzahl Bilder in der Höhe eingeben:",
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
            "ti_g_pos": "Position der neuen Bildergruppe",
            "msg_g_pos": "Wert eingeben, 1=top, etc:",
            "ti_ratio_error": "Problem mit Seitenverhältnis",
            "msg_ratio_error": "Bild breiter als Seite!",
            "ti_nlines": "Anzahl der Bildzeilen",
            "msg_nlines": "Anzahl der Zeilen angeben:",
            "ti_ratio": "Bildverhältnis",
            "msg_ratio": "Bildverhältnis eingeben, typisch 3/2 oder 4/3:",
            "ti_direction": "Zeilenrichtung",
            "msg_direction": "Richtung eingeben, typisch von links nach rechts, left2right",
            "ti_aspect": "Richtungstyp",
            "msg_aspect": "Richtungstyp eingeben, typisch constant, alle grossen Bilder zur selben Seite:",
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
            "ti_g_pos": "Position of the new group",
            "msg_g_pos": "Entrez position, 1=top, etc:",
            "ti_ratio_error": "Ratio error",
            "msg_ratio_error": "Image width larger than page!",
            "ti_nlines": "Picture rows",
            "msg_nlines": "Enter the number of picture rows",
            "ti_ratio": "Image ratio",
            "msg_ratio": "Entrez the image ratio, typically 3/2 ou 4/3:",
            "ti_direction": "Direction",
            "msg_direction": "Entrez direction, typically left2right",
            "ti_aspect": "Direction type",
            "msg_aspect": "Entrez direction type, typically "
            "constant"
            ", all large images on the same side:",
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


def write_setup_files(script_path):
    # create python source file stating script_path for later import
    dircfgpath = os.path.join(script_path, "script_path.py")
    with open(dircfgpath, "w") as dirfile:
        dirfile.write("script_path='" + script_path + "'")

    cfgpath = os.path.join(script_path, ".photobook", "phb.cfg")
    with open(cfgpath, "wb") as file4cfg:
        pickle.dump(my_lang, file4cfg)
        pickle.dump(my_units, file4cfg)
        pickle.dump(my_msg, file4cfg)
        pickle.dump(my_defaults, file4cfg)


setup_window = Tk()
setup_window.title("Setup photobook scripts for scribus")
script_path, chosen_lang, chosen_unit = init_after_check_previous_config()
chosen_lang = StringVar(value=chosen_lang)
chosen_unit = StringVar(value=chosen_unit)
# chosen_lang = StringVar(value=my_lang)
# chosen_unit = StringVar(value=int2Unit[my_units])

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

# show_path = ttk.Label(setup_window, text="current path:" + script_path)
# show_path.grid(row=1, column=0)

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
my_units = select_unit(chosen_unit.get())
my_lang = chosen_lang.get()
my_msg = select_msgs(my_lang)


my_defaults = set_my_defaults(my_units)
write_setup_files(script_path)
