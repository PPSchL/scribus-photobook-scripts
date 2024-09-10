import scribus
from script_path import script_path
import scribus_paul as sp

sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

page = sp.get_page_info()
page_available = sp.page_with_bleed(page, my_defaults["bleed"])
# by default set do 2 by 2 pictures and gutter equal to 0
x_n_picts, y_n_picts, gutter = sp.get_n_images_gutter(my_msg, xnp=2, ynp=2, gutter=0.0)
sp.split_image("create", page_available, x_n_picts, y_n_picts, gutter)

scribus.setUnit(initial_units)
