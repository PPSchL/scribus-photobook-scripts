import scribus
from script_path import script_path
import scribus_paul as sp
import scribus_acta as sa


my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
# get initial units and set units to mm
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

gutter = my_defaults["acta_gutter"]
# get page margins, size and type (left or right)
page = sp.get_page_info()
path_to_base, n_groups, top_group, below_groups, g_pos = sa.set_acta_data(
    "normal", page, script_path, gutter
)
sa.draw_normal_page(
    page, path_to_base, n_groups, gutter, top_group, below_groups, g_pos
)

scribus.setUnit(initial_units)
