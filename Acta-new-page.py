import sys
try:
    import scribus
except ImportError:
    print("Unable to import the 'scribus' module. This script will only run within the Python interpreter embedded in Scribus. Try Script->Execute Script.")
    sys.exit(1)
if not scribus.haveDoc():
    scribus.messageBox('Scribus -Script Error', "No document open", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)


def acta_img_size1D(n_picts, margin1, margin2, gutter, page, txt_size=0):
    return (page-margin1-margin2-txt_size-(n_picts-1)*gutter)/n_picts
    
def acta_pos1D(n_picts,margin,pict_size,gutter):
    return margin+(n_picts-1)*(pict_size+gutter)
    

#get initial units and set units to mm
initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)

# get page margins, size and type (left or right)
margins=scribus.getPageNMargins(scribus.currentPage())
left_margin=margins[1]
right_margin=margins[2]
top_margin=margins[0]
bottom_margin=margins[3]
size=scribus.getPageNSize(scribus.currentPage())
xs_page=size[0]
ys_page=size[1]
type_page=scribus.getPageType(scribus.currentPage())


# *** define page layout decisions here ***
# text frame x size (width) is considered constant, text frame height (y size) and image size will be adapted
path_to_base="/home/paul/Documents/dessins-présentations/Scribus/Models2edit/Annales_base.sla"
n_groups=3 # number of "days" on each page, 3 (top, middle, bottom) not likely to change
gutter=3.0
top_group=["Acta_jour","Acta_mois","Acta_txt","Acta_img"]
below_groups=["Acta_jour","Acta_txt","Acta_img"]
g_pos={} #dictionary of group element sizes and positions
g_pos["Acta_txt"]={"xs":55.0}
g_pos["Acta_jour"]={"xs":12.5,"ys":8.0}
g_pos["Acta_mois"]={"xs":35.0,"ys":8.0}
g_pos["Acta_img"]={}

#calculate image size
g_pos["Acta_img"]["xs"]=acta_img_size1D(1, left_margin, right_margin, 0, xs_page, g_pos["Acta_txt"]["xs"])
g_pos["Acta_img"]["ys"]=acta_img_size1D(n_groups, top_margin, bottom_margin, gutter, ys_page, 0)
g_pos["Acta_txt"]["ys"]=g_pos["Acta_img"]["ys"]


#determine or calculate delta vs top left coordinates (x_topleft, y_topleft)
if type_page==0:#left page
	g_pos["Acta_txt"].update({"dx":0.0,"dy":0.0})
	g_pos["Acta_img"].update({"dx":g_pos["Acta_txt"]["xs"],"dy":0.0})
	g_pos["Acta_jour"].update({"dx":1.0,"dy":0.5})
	g_pos["Acta_mois"].update({"dx":16.0,"dy":-4.0})
else:#right page
	g_pos["Acta_txt"].update({"dx":g_pos["Acta_img"]["xs"],"dy":0.0})
	g_pos["Acta_img"].update({"dx":0.0,"dy":0.0})
	g_pos["Acta_jour"].update({"dx":41.5+g_pos["Acta_img"]["xs"],"dy":0.5})
	g_pos["Acta_mois"].update({"dx":4.0+g_pos["Acta_img"]["xs"],"dy":-4.0})

# get frames from file into clipboard

scribus.openDoc(path_to_base)
scribus.copyObjects(top_group)
scribus.closeDoc()
# copy the original group depending on position (with or without mois)
for n_group in range(1,n_groups+1):
	if n_group==1:
		scribus.openDoc(path_to_base)
		scribus.copyObjects(top_group)
		scribus.closeDoc()
	else:
		scribus.openDoc(path_to_base)
		scribus.copyObjects(below_groups)
		scribus.closeDoc()
#calculate x_topleft and y_topleft according to number of group
	x_topleft=left_margin
	y_topleft=acta_pos1D(n_group,top_margin,g_pos["Acta_img"]["ys"],gutter)
	# paste objects and then for each element according to its name (find method!) change its size and position
	current_g=scribus.pasteObjects()
	for elem in current_g:
		for elem_g in top_group:
			if elem.find(elem_g)!=-1:
				scribus.moveObjectAbs(x_topleft+g_pos[elem_g]["dx"], y_topleft+g_pos[elem_g]["dy"] , elem)
				scribus.sizeObject(g_pos[elem_g]["xs"], g_pos[elem_g]["ys"] , elem)
				if not scribus.isLocked(elem):
					scribus.lockObject(elem)



scribus.setUnit(initial_units)



