
import scribus
import scribus_paul as sp
import scribus_acta as sa


#get initial units and set units to mm
initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)
#define group types as list, allowing access through index which will be requested from user=>less typing for user
group_types=["normal","central","double","whole_page"]
#request group type, default = central
group_size = int(scribus.valueDialog("Type", '             Entrez la valeur:\n- normal=0,\n- central=1,\n- double=2,\n- page entière=3', "1"))
group_type=group_types[group_size]
if group_type=="whole_page":
    group_n=1
else:
    group_n = int(scribus.valueDialog("Position à changer:", "Entrez la valeur, 1=top, etc:", "2"))

# get page margins, size and type (left or right)
page=sp.get_page_info()
path_to_base,n_groups,gutter,top_group,below_groups,g_pos=sa.set_acta_data(group_type,page)

sa.draw_1_group(group_type,page,path_to_base,n_groups,group_n,gutter,top_group,below_groups,g_pos)

scribus.setUnit(initial_units)

