import scribus
from script_path import script_path
import scribus_paul as sp

sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

if scribus.selectionCount() < 2:
    scribus.messageBox(
        "Scribus-Script Error",
        "Not enough images to combine, need at least 2",
        scribus.ICON_WARNING,
        scribus.BUTTON_OK,
    )
else:
    sp.combine_images()


scribus.setUnit(initial_units)
