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
margins=scribus.getPageNMargins(scribus.currentPage())
size=scribus.getPageNSize(scribus.currentPage())

x_page=size[0]
y_page=size[1]
x_n_picts=int(scribus.valueDialog("Images en largeur", "Entrez le nombre de photos en largeur:","2"))
y_n_picts=int(scribus.valueDialog("Images en hauteur", "Entrez le nombre de photos en hauteur:" ,"3"))
gutter=float(scribus.valueDialog("Gouttière", "Entrez la taille de la gouttière en mm" ,"3"))
xsize=pict_size1D(x_n_picts,margins[1], margins[2], gutter, x_page)
ysize=pict_size1D(y_n_picts,margins[0], margins[3], gutter, y_page)
for nx in range(1,x_n_picts+1):
    for ny in range(1,y_n_picts+1):
        # diff between left and right check margins from scribus
        xpict=pict_pos1D(nx,margins[1],xsize,gutter)
        ypict=pict_pos1D(ny,margins[0],ysize,gutter)
        image_name=scribus.createImage(xpict, ypict, xsize, ysize)
        scribus.lockObject(image_name)
        scribus.setFillColor("Black",image_name)
        #scribus.messageBox("Position","x:"+repr(xpict)+"  y:"+repr(ypict))
scribus.setUnit(initial_units)



