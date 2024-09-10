import scribus
from script_path import script_path
import scribus_paul as sp

sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

sp.combine_images()


scribus.setUnit(initial_units)
