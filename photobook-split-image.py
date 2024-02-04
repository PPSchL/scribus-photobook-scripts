import sys
try:
    import scribus
except ImportError:
    print("Unable to import the 'scribus' module. This script will only run within the Python interpreter embedded in Scribus. Try Script->Execute Script.")
    sys.exit(1)
if not scribus.haveDoc():
    scribus.messageBox('Scribus -Script Error', "No document open", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)

def pict_size1D(n_picts, margin1, margin2, gutter, page):
    return (page-margin1-margin2-(n_picts-1)*gutter)/n_picts

def pict_pos1D(n_picts,margin,pict_size,gutter):
    return margin+(n_picts-1)*(pict_size+gutter)


initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)
#initial_imgs=scribus.groupObjects()
initial_img=scribus.getSelectedObject(0) 
imgs_size=scribus.getSize(initial_img)

size=scribus.getPageNSize(scribus.currentPage())
x_page=size[0]
y_page=size[1]

x_whole_size=imgs_size[0]
y_whole_size=imgs_size[1]
imgs_pos=scribus.getPosition(initial_img)
x_margins=(imgs_pos[0],x_page-(imgs_pos[0]+x_whole_size))
y_margins=(imgs_pos[1],y_page-(imgs_pos[1]+y_whole_size))



x_n_picts=int(scribus.valueDialog("Images en largeur", "Entrez le nombre de photos en largeur:","2"))
y_n_picts=int(scribus.valueDialog("Images en hauteur", "Entrez le nombre de photos en hauteur:" ,"3"))
gutter=float(scribus.valueDialog("Gouttière", "Entrez la taille de la gouttière en mm" ,"5"))




xsize=pict_size1D(x_n_picts,x_margins[0], x_margins[1], gutter, x_page)
ysize=pict_size1D(y_n_picts,y_margins[0], y_margins[1], gutter, y_page)
for nx in range(1,x_n_picts+1):
    for ny in range(1,y_n_picts+1):
        xpict=pict_pos1D(nx,x_margins[0],xsize,gutter)
        ypict=pict_pos1D(ny,y_margins[0],ysize,gutter)
        image_name=scribus.createImage(xpict, ypict, xsize, ysize)
        scribus.lockObject(image_name)
        scribus.setFillColor("Black",image_name)
        #scribus.messageBox("Position","x:"+repr(xpict)+"  y:"+repr(ypict))
if scribus.isLocked(initial_img):
    scribus.lockObject(initial_img)
scribus.deleteObject(initial_img)
scribus.setUnit(initial_units)



