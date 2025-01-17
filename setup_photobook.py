#! /usr/bin/env python3
import scribus
import os
import pickle
from scribus_paul import get_config_data

conversion_factor = {
    scribus.UNIT_MILLIMETERS: 1,
    scribus.UNIT_CENTIMETRES: 0.1,
    scribus.UNIT_INCHES: 1 / 25.4,
    scribus.UNIT_POINTS: 1 / 25.4 * 72,
    scribus.UNIT_PICAS: 1 / 25.4 * 6,
    scribus.UNIT_CICERO: 1 / 4.51165812456,
}


def set_defaults():
    script_path = os.getcwd()
    chosen_lang = "Français"
    chosen_unit = "mm"
    return (script_path, chosen_lang, chosen_unit)


def set_my_defaults(my_units):
    my_defaults = {  # all distances in mm, convert to mm from your preferred unit
        "bleed": 5.0,  # bleed, should be identical to the one defined in your scribus file
        "xn": 2,  # number of images in x direction
        "yn": 3,  # number of images in the y direction
        "gutter": 3,
        "xn_split": 2,  # number of images in x direction for split-image
        "yn_split": 2,  # number of images in y direction for split-image
        "gutter_split": 1.0,  # gutter for split-image
        "asym_n-lines": 3,  # number of lines for the asymmetric script
        "asym_ratio": "4/3",
        "asym_gutter": 3.0,
        "asym_direction": "left2right",
        "asym_aspect": "constant",
        "acta_gutter": 3.0,  # gutter for the diary scripts
        "visual_center_xoffset": 2.5,  # x offset in percent
        "visual_center_yoffset": 2.5,  # y offset in percent
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
            "root.title": "Composition d'une page photo complexe",
            "explication": "Choisir la mise en page en fonction des photos en paysage, portrait et carré",
            "L_number_label": "Paysage",
            "P_number_label": "Portrait",
            "S_number_label": "Carré",
            "do_it": "Dispositions possibles",
            "show_all_same_number": "Toutes même total",
            "stop_it": "Terminé, tout fermer",
            "parameter_label": "Paramètres additionnels",
            "gutter_label": "Gouttière (",
            "bleed_or_not": "Inclure fond perdu",
            "acta_show": "Composer une page de journal",
            "no_layouts_label": "Pas de mise en page avec le nombre de photos choisi!",
            "choose_layout.title": "Choisir la disposition",
            "exact_label": "Correspondance parfaite",
            "no_exact_label": "Pas de correspondance parfaite!",
            "same_total_label": "Correspondance approximative: dispositions avec le même nombre de photos",
            "stop_top": "Aucune ne convient, revenir vers le menu principal",
            "w_acta.title": "Composer page de journal",
            "quick_draw_title": "Sélection rapide",
            "draw_3": "Dessiner page standard",
            "draw_2_top": "Dessiner double (en haut)",
            "draw_2_bottom": "Dessiner double (en bas)",
            "draw_full": "Dessiner page entière",
            "line_title": "Personnaliser lignes",
            "line_do_title": "Dessiner ligne donnée",
            "linedo": "dessiner",
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
            "root.title": "Komplexe Seite aufbauen",
            "explication": "Layout begründet auf Zahl der Querformat, Hochformat und Quadratischen Fotos auswählen",
            "L_number_label": "Querformat",
            "P_number_label": "Hochformat",
            "S_number_label": "Quadrat",
            "do_it": "Mögliche Layouts",
            "show_all_same_number": "Alle, gleiche Summe",
            "stop_it": "Fertig, Script schliessen",
            "parameter_label": "Zusätzliche Parameter",
            "gutter_label": "Steg (",
            "bleed_or_not": "Beschnitt mitbenutzen",
            "acta_show": "Tagebuch aufbauen",
            "no_layouts_label": "Keine Layouts mit dieser Foto-Gesamtzahl!",
            "choose_layout.title": "Layout auswählen",
            "exact_label": "Perfekte Übereinstimmung",
            "no_exact_label": "Keine perfekte Übereinstimmung!",
            "same_total_label": "Annähernde Übereinstimmung: Layouts mit der gleichen Foto-Gesamtzahl",
            "stop_top": "Keine sind ok, zurück zum Hauptmenu",
            "w_acta.title": "Tagebuch-Seite aufbauen",
            "quick_draw_title": "Schnelle Auswahl",
            "draw_3": "Standard-Seite zeichnen",
            "draw_2_top": "Doppel (oben) zeichnen",
            "draw_2_bottom": "Doppen (unten) zeichnen",
            "draw_full": "Gesamtseite zeichnen",
            "line_title": "Einzelner Zeilentyp",
            "line_do_title": "Zeile zeichnen",
            "linedo": "zeichnen",
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
            "msg_ratio": "Enter the image ratio, typically 3/2 ou 4/3:",
            "ti_direction": "Direction",
            "msg_direction": "Enter direction, typically left2right",
            "ti_aspect": "Direction type",
            "msg_aspect": "Entrez direction type, typically "
            "constant"
            ", all large images on the same side:",
            "root.title": "Build complex photo page",
            "explication": "Choose layout for a number of Landscape, Portrait and Square photographs",
            "L_number_label": "Landscape",
            "P_number_label": "Portrait",
            "S_number_label": "Square",
            "do_it": "Show possible layouts",
            "show_all_same_number": "All with same total",
            "stop_it": "Finished, close all",
            "parameter_label": "Additional parameters",
            "gutter_label": "Gutter (",
            "bleed_or_not": "Draw into bleed",
            "acta_show": "Build diary page",
            "no_layouts_label": "No layouts with the same number of pictures!",
            "choose_layout.title": "Choose layout",
            "exact_label": "Perfect correspondance",
            "no_exact_label": "No perfect correspondance!",
            "same_total_label": "Approximate correspondance: Layouts with the same number of pictures",
            "stop_top": "None are convenient, go back to ratio specification",
            "w_acta.title": "Build diary page",
            "quick_draw_title": "Quick selection",
            "draw_3": "Draw standard page",
            "draw_2_top": "Draw double (top)",
            "draw_2_bottom": "Draw double (bottom)",
            "draw_full": "Draw full page",
            "line_title": "Customize lines",
            "line_do_title": "Draw specific line",
            "linedo": "draw",
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


def write_setup_files(script_path, my_lang, my_units, my_msg, my_defaults):
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


def main():
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

    my_defaults = set_my_defaults(my_units)
    write_setup_files(script_path, my_lang, my_units, my_msg, my_defaults)


if __name__ == "__main__":
    main()
