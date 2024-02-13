import scribus
import scribus_paul as sp
import scribus_acta as sa

   

#get initial units and set units to mm
initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)

# get page margins, size and type (left or right)
page=sp.get_page_info()
path_to_base,n_groups,gutter,top_group,below_groups,g_pos=sa.set_acta_data("normal",page)
sa.draw_normal_page(page,path_to_base,n_groups,gutter,top_group,below_groups,g_pos)

scribus.setUnit(initial_units)

