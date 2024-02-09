import scribus
import scribus_paul as sp


def acta_split_image(initial_img, xs_initial, ys_initial):
    sp.split_image("resize",initial_img, xs_initial, ys_initial, x_n_picts=3, y_n_picts=1, gutter=0.5)    

def acta_img_size1D(n_picts, margin1, margin2, gutter, page, txt_size=0):
    return (page-margin1-margin2-txt_size-(n_picts-1)*gutter)/n_picts
    
def acta_pos1D(n_picts,margin,pict_size,gutter):
    return margin+(n_picts-1)*(pict_size+gutter)


def acta_img_size1D_central(n_picts, margin1, margin2, gutter, page, txt_size=0):
    return (
        page - margin1 - margin2 - n_picts * txt_size - (n_picts - 1) * gutter
    ) / n_picts

def set_g_pos_normal(page,n_groups,gutter):
    g_pos={} #dictionary of group element sizes and positions, dictionary used because mutable
    g_pos["Acta_txt"]={"xs":55.0}
    g_pos["Acta_jour"]={"xs":12.5,"ys":8.0}
    g_pos["Acta_mois"]={"xs":35.0,"ys":8.0}
    g_pos["Acta_img"]={}

    #calculate image size
    g_pos["Acta_img"]["xs"]=acta_img_size1D(1, page.mleft, page.mright, 0, page.xs, g_pos["Acta_txt"]["xs"])
    g_pos["Acta_img"]["ys"]=acta_img_size1D(n_groups, page.mtop, page.mbottom, gutter, page.ys, 0)
    g_pos["Acta_txt"]["ys"]=g_pos["Acta_img"]["ys"]


    #determine or calculate delta vs top left coordinates (x_topleft, y_topleft)
    if page.page_type==0:#left page
        g_pos["Acta_txt"].update({"dx":0.0,"dy":0.0})
        g_pos["Acta_img"].update({"dx":g_pos["Acta_txt"]["xs"],"dy":0.0})
        g_pos["Acta_jour"].update({"dx":1.0,"dy":0.5})
        g_pos["Acta_mois"].update({"dx":16.0,"dy":-4.0})
    else:#right page
        g_pos["Acta_txt"].update({"dx":g_pos["Acta_img"]["xs"],"dy":0.0})
        g_pos["Acta_img"].update({"dx":0.0,"dy":0.0})
        g_pos["Acta_jour"].update({"dx":41.5+g_pos["Acta_img"]["xs"],"dy":0.5})
        g_pos["Acta_mois"].update({"dx":4.0+g_pos["Acta_img"]["xs"],"dy":-4.0})
    return g_pos

def set_g_pos_central(page,n_groups,gutter):
    g_pos = {}  # dictionary of group element sizes and positions
    g_pos["Acta_txt"] = {
        "xs": acta_img_size1D_central(1, page.mleft, page.mright, 0, page.xs)
    }
    g_pos["Acta_txt"]["ys"] = 20.0

    g_pos["Acta_jour"] = {"xs": 12.5, "ys": 8.0}
    g_pos["Acta_mois"] = {"xs": 35.0, "ys": 8.0}
    g_pos["Acta_img"] = {}

    # calculate image size
    g_pos["Acta_img"]["xs"] = g_pos["Acta_txt"]["xs"]
    g_pos["Acta_img"]["ys"] = acta_img_size1D_central(n_groups, page.mtop, page.mbottom, gutter, page.ys, g_pos["Acta_txt"]["ys"])
    # determine or calculate delta vs top left coordinates (x_topleft, y_topleft)
    if page.page_type:  # left page
        g_pos["Acta_txt"].update({"dx": 0.0, "dy": 0.0})
        g_pos["Acta_img"].update({"dx": 0.0, "dy": g_pos["Acta_txt"]["ys"]})
        g_pos["Acta_jour"].update({"dx": 1.0, "dy": 0.5})
        g_pos["Acta_mois"].update({"dx": 16.0, "dy": -4.0})
    else:  # right page
        g_pos["Acta_txt"].update({"dx": 0.0, "dy": 0.0})
        g_pos["Acta_img"].update({"dx": 0.0, "dy": g_pos["Acta_txt"]["ys"]})
        g_pos["Acta_jour"].update({"dx": -13.5 + g_pos["Acta_txt"]["xs"], "dy": 0.5})
        g_pos["Acta_mois"].update({"dx": -51 + g_pos["Acta_img"]["xs"], "dy": -4.0})
    return g_pos

def set_acta_data(action, page):
    # *** define page layout decisions here ***
    # text frame x size (width) is considered constant, text frame height (y size) and image size will be adapted
    path_to_base="/home/paul/Documents/dessins-présentations/Scribus/Models2edit/Annales_base.sla"
    n_groups=3 # number of "days" on each page, 3 (top, middle, bottom) not likely to change
    gutter=3.0
    top_group=["Acta_jour","Acta_mois","Acta_txt","Acta_img"]
    below_groups=["Acta_jour","Acta_txt","Acta_img"]
    if action=="normal":
        g_pos=set_g_pos_normal(page,n_groups,gutter)
    else:
        g_pos=set_g_pos_central(page,n_groups,gutter)   
    return (path_to_base,n_groups,gutter,top_group,below_groups,g_pos)

def paste_and_resize_group(action,page,group_n,g_pos,top_group,gutter):
    #calculate x_topleft and y_topleft according to number of group
    x_topleft=page.mleft
    if action=="central":
        y_topleft = acta_pos1D(group_n, page.mtop, g_pos["Acta_img"]["ys"] + g_pos["Acta_txt"]["ys"], gutter)
    else:
        y_topleft=acta_pos1D(group_n,page.mtop,g_pos["Acta_img"]["ys"],gutter)
    
    # paste objects and then for each element according to its name (find method!) change its size and position
    current_g=scribus.pasteObjects()
    for elem in current_g:
        for elem_g in top_group:
            if elem.find(elem_g)!=-1:
                scribus.moveObjectAbs(x_topleft+g_pos[elem_g]["dx"], y_topleft+g_pos[elem_g]["dy"] , elem)
                scribus.sizeObject(g_pos[elem_g]["xs"], g_pos[elem_g]["ys"] , elem)
                scribus.lockObject(elem)
    if action=="central":
        for elem in current_g:
            if elem.find("Acta_img") != -1:
                elem_obj=sp.set_object_info("Acta_img",x_topleft+g_pos["Acta_img"]["dx"],y_topleft+g_pos["Acta_img"]["dy"],g_pos["Acta_img"]["xs"],g_pos["Acta_img"]["ys"],0,0,0,0,0)
                sp.split_image("resize", elem_obj, x_n_picts=3, y_n_picts=1, gutter=0.5)
    


def copy_group(path_to_base,group_n, top_group,below_groups):
    if group_n==1:
        group=top_group
    else:
        group=below_groups
    scribus.openDoc(path_to_base)
    scribus.copyObjects(group)
    scribus.closeDoc()

def draw_whole_page(page,path_to_base,n_groups,gutter,top_group,below_groups,g_pos):
    for group_n in range(1,n_groups+1):
        draw_1_group("normal",page,path_to_base,group_n,gutter,top_group,below_groups,g_pos)

def draw_1_group(action,page,path_to_base,group_n,gutter,top_group,below_groups,g_pos):
    copy_group(path_to_base,group_n, top_group,below_groups)
    paste_and_resize_group(action,page,group_n,g_pos,top_group,gutter)


