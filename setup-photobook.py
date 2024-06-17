#! /usr/bin/env python3
import scribus
import os
import pickle
from scribus_paul import get_config_data


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
        script_path = os.getcwd()
        chosen_lang = "Français"
        chosen_unit = "mm"
    else:
        cfgpath = os.path.join(script_path, ".photobook", "phb.cfg")
        if os.path.isfile(cfgpath):
            # config file exist => read
            my_lang, my_msg, my_units = get_config_data(script_path)
            chosen_lang = my_lang
            chosen_unit = int2Unit[my_units]
        else:
            # script_path ok, but no config file => initialize by default values
            script_path = os.getcwd()
            chosen_lang = "Français"
            chosen_unit = "mm"
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


# *****************
print("Setup photobook scripts for scribus")
script_path_i, chosen_lang_i, chosen_unit_i = init_after_check_previous_config()

script_path = scribus.valueDialog(
    "Select scripts directory",
    "Change current path to script directory: ",
    script_path_i,
)


chosen_unit = scribus.valueDialog(
    "Select measurement units",
    "Please enter one of these:\nmm\ncm\npoints\ninches\npicas\nciceros\nCurrent units: ",
    chosen_unit_i,
)

my_lang = scribus.valueDialog(
    "Select Menu language",
    "Please enter one of these:\nFrançais\nDeutsch\nEnglish\nCurrent language: ",
    chosen_lang_i,
)

my_units = select_unit(chosen_unit)
my_msg = select_msgs(my_lang)

# create python source file stating script_path for later import
dircfgpath = os.path.join(script_path, "script_path.py")
with open(dircfgpath, "w") as dirfile:
    dirfile.write("script_path='" + script_path + "'")

cfgpath = os.path.join(script_path, ".photobook", "phb.cfg")
with open(cfgpath, "wb") as file4cfg:
    pickle.dump(my_lang, file4cfg)
    pickle.dump(my_units, file4cfg)
    pickle.dump(my_msg, file4cfg)
