import scribus
from script_path import script_path
import scribus_paul as sp
import scribus_acta as sa


# get initial units and set units to mm
initial_units = scribus.getUnit()
my_msg, my_units = sp.get_config_data(script_path)

# get page margins, size and type (left or right)
page = sp.get_page_info()
path_to_base, n_groups, gutter, top_group, below_groups, g_pos = sa.set_acta_data(
    "normal", page, script_path
)
sa.draw_normal_page(
    page, path_to_base, n_groups, gutter, top_group, below_groups, g_pos
)

scribus.setUnit(initial_units)
