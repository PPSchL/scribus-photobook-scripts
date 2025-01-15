import scribus
from script_path import script_path
import scribus_paul as sp

sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

if scribus.selectionCount() < 1:
    scribus.messageBox(
        "Scribus-Script Error",
        "No selection, need to select an image before splitting it!",
        scribus.ICON_WARNING,
        scribus.BUTTON_OK,
    )
else:
    initial_img = sp.get_object_info(scribus.getSelectedObject())
    x_n_picts, y_n_picts, gutter = sp.get_n_images_gutter(
        my_msg,
        my_defaults["xn_split"],
        my_defaults["yn_split"],
        my_defaults["gutter_split"],
    )

    sp.split_image("resize", initial_img, x_n_picts, y_n_picts, gutter)

scribus.setUnit(initial_units)
