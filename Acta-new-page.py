import scribus
import scribus_paul as sp
import scribus_acta as sa

def acta_img_size1D(n_picts, margin1, margin2, gutter, page, txt_size=0):
    return (page-margin1-margin2-txt_size-(n_picts-1)*gutter)/n_picts
    
def acta_pos1D(n_picts,margin,pict_size,gutter):
    return margin+(n_picts-1)*(pict_size+gutter)
    

#get initial units and set units to mm
initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)

# get page margins, size and type (left or right)
page=sp.get_page_info()
path_to_base,n_groups,gutter,top_group,below_groups,g_pos=sa.set_acta_data("normal",page)
sa.draw_whole_page(page,path_to_base,n_groups,gutter,top_group,below_groups,g_pos)

scribus.setUnit(initial_units)

