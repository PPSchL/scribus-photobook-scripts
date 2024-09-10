import scribus
from script_path import script_path
import scribus_paul as sp
import scribus_acta as sa


# get initial units and set units to mm
initial_units = scribus.getUnit()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
gutter = my_defaults["acta_gutter"]
# define group types as list, allowing access through index which will be requested from user=>less typing for user
group_types = ["normal", "central", "double", "whole_page"]
# request group type, default = central
group_size = int(
    scribus.valueDialog(
        my_msg["ti_g_type"],
        my_msg["msg_g_type"],
        "1",
    )
)
group_type = group_types[group_size]
if group_type == "whole_page":
    group_n = 1
else:
    group_n = int(scribus.valueDialog(my_msg["ti_g_pos"], my_msg["msg_g_pos"], "2"))
    if group_type == "double":
        if group_n > 2:
            group_n = 2
    else:
        if group_n > 3:
            group_n = 3

# get page margins, size and type (left or right)
page = sp.get_page_info()
path_to_base, n_groups, gutter, top_group, below_groups, g_pos = sa.set_acta_data(
    group_type, page, script_path
)

sa.draw_1_group(
    group_type,
    page,
    path_to_base,
    n_groups,
    group_n,
    gutter,
    top_group,
    below_groups,
    g_pos,
)

scribus.setUnit(initial_units)
