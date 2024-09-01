import scribus
from script_path import script_path
import scribus_paul as sp

sp.check_doc_present()
my_lang, my_msg, my_units = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

page = sp.get_page_info()
page_available = sp.page_available(page)

n_lines, ratio, gutter, direction, aspect_type = sp.get_nlines_ratio(
    my_msg,
    n_lines=3,
    ratio="4/3",
    gutter=3.0,
    direction="left2right",
    aspect_type="constant",
)
image_list = sp.make_list_of_asymmetric_images(
    my_msg, page_available, n_lines, ratio, gutter, direction, aspect_type
)
if image_list != "ratio error":
    sp.draw_list_of_images(image_list)

scribus.setUnit(initial_units)
