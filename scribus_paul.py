import sys
try:
    import scribus
except ImportError:
    print("Unable to import the 'scribus' module. This script will only run within the Python interpreter embedded in Scribus. Try Script->Execute Script.")
    sys.exit(1)
if not scribus.haveDoc():
    scribus.messageBox('Scribus -Script Error', "No document open", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)


def acta_img_size1D_central(n_picts, margin1, margin2, gutter, page, txt_size=0):
    return (page-margin1-margin2-n_picts*txt_size-(n_picts-1)*gutter)/n_picts
    
def acta_pos1D(n_picts,margin,pict_size,gutter):
    return margin+(n_picts-1)*(pict_size+gutter)
    
def pict_size1D(n_picts, margin1, margin2, gutter, page):
    return (page-margin1-margin2-(n_picts-1)*gutter)/n_picts

def pict_pos1D(n_picts,margin,pict_size,gutter):
    return margin+(n_picts-1)*(pict_size+gutter)
    
def split_image(initial_img, xs_page, ys_page, x_n_picts=3, y_n_picts=1,gutter=0.5):
	imgs_size=scribus.getSize(initial_img)
	if scribus.isLocked(initial_img):
		scribus.lockObject(initial_img)
	xs_whole_size=imgs_size[0]
	ys_whole_size=imgs_size[1]
	imgs_pos=scribus.getPosition(initial_img)
	x_margins=(imgs_pos[0],xs_page-(imgs_pos[0]+xs_whole_size))
	y_margins=(imgs_pos[1],ys_page-(imgs_pos[1]+ys_whole_size))
	xsize=pict_size1D(x_n_picts,x_margins[0], x_margins[1], gutter, xs_page)
	ysize=pict_size1D(y_n_picts,y_margins[0], y_margins[1], gutter, ys_page)
	for nx in range(1,x_n_picts+1):
		for ny in range(1,y_n_picts+1):
			xpict=pict_pos1D(nx,x_margins[0],xsize,gutter)
			ypict=pict_pos1D(ny,y_margins[0],ysize,gutter)
			image_name=scribus.createImage(xpict, ypict, xsize, ysize)
			scribus.setFillColor("Black",image_name)
			if not scribus.isLocked(image_name):
				scribus.lockObject(image_name)
	scribus.deleteObject(initial_img)


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
# text frame x size (width) and ys are considered constant, image size will be adapted
# this will replace either top, middle or bottom group (panel)
path_to_base="/home/paul/Documents/dessins-présentations/Scribus/Models2edit/Annales_base.sla"
n_groups=3 # number of "days" on each page, 3 (top, middle, bottom) not likely to change
gutter=3.0
top_group=["Acta_jour","Acta_mois","Acta_txt","Acta_img"]
below_groups=["Acta_jour","Acta_txt","Acta_img"]
g_pos={} #dictionary of group element sizes and positions
g_pos["Acta_txt"]={"xs":acta_img_size1D_central(1, left_margin, right_margin, 0, xs_page)}
g_pos["Acta_txt"]["ys"]=20.0

g_pos["Acta_jour"]={"xs":12.5,"ys":8.0}
g_pos["Acta_mois"]={"xs":35.0,"ys":8.0}
g_pos["Acta_img"]={}

#calculate image size
g_pos["Acta_img"]["xs"]=g_pos["Acta_txt"]["xs"]
g_pos["Acta_img"]["ys"]=acta_img_size1D_central(n_groups, top_margin, bottom_margin, gutter, ys_page, g_pos["Acta_txt"]["ys"] )



#determine or calculate delta vs top left coordinates (x_topleft, y_topleft)
if type_page==0:#left page
	g_pos["Acta_txt"].update({"dx":0.0,"dy":0.0})
	g_pos["Acta_img"].update({"dx":0.0,"dy":g_pos["Acta_txt"]["ys"]})
	g_pos["Acta_jour"].update({"dx":1.0,"dy":0.5})
	g_pos["Acta_mois"].update({"dx":16.0,"dy":-4.0})
else:#right page
	g_pos["Acta_txt"].update({"dx":0.0,"dy":0.0})
	g_pos["Acta_img"].update({"dx":0.0,"dy":g_pos["Acta_txt"]["ys"]})
	g_pos["Acta_jour"].update({"dx":-13.5+g_pos["Acta_txt"]["xs"],"dy":0.5})
	g_pos["Acta_mois"].update({"dx":-51+g_pos["Acta_img"]["xs"],"dy":-4.0})

# get frames from file into clipboard

scribus.openDoc(path_to_base)
scribus.copyObjects(top_group)
scribus.closeDoc()
# copy the original group depending on position (with or without mois)

n_group=int(scribus.valueDialog("Position à changer:", "Entrez la valeur, 1=top, etc:","2"))
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
y_topleft=acta_pos1D(n_group,top_margin,g_pos["Acta_img"]["ys"]+g_pos["Acta_txt"]["ys"],gutter)
# paste objects and then for each element according to its name (find method!) change its size and position
current_g=scribus.pasteObjects()
for elem in current_g:
	for elem_g in top_group:
		if elem.find(elem_g)!=-1:
			if scribus.isLocked(elem):
				scribus.lockObject(elem)
			scribus.moveObjectAbs(x_topleft+g_pos[elem_g]["dx"], y_topleft+g_pos[elem_g]["dy"] , elem)
			scribus.sizeObject(g_pos[elem_g]["xs"], g_pos[elem_g]["ys"] , elem)
			#if not scribus.isLocked(elem):
			scribus.lockObject(elem)
for elem in current_g:
	if elem.find("Acta_img")!=-1:
		split_image(elem, xs_page, ys_page, x_n_picts=3, y_n_picts=1,gutter=0.5)


scribus.setUnit(initial_units)



