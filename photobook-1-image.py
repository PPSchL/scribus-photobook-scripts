import scribus
from script_path import script_path
import scribus_paul as sp

sp.check_doc_present()
my_lang, my_msg, my_units = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

page = sp.get_page_info()
page_available = sp.page_available(page)
x_n_picts, y_n_picts, gutter = sp.get_n_images_gutter(my_msg)
nx, ny = sp.get_position4pict(my_msg, x_n_picts, y_n_picts)
sp.create_1_image(page_available, x_n_picts, y_n_picts, gutter, nx, ny)

scribus.setUnit(initial_units)
