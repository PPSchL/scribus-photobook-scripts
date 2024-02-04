import sys
try:
    import scribus
except ImportError:
    print("Unable to import the 'scribus' module. This script will only run within the Python interpreter embedded in Scribus. Try Script->Execute Script.")
    sys.exit(1)
if not scribus.haveDoc():
    scribus.messageBox('Scribus -Script Error', "No document open", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)


initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)
initial_imgs=scribus.groupObjects()

imgs_size=scribus.getSize(initial_imgs)
xsize=imgs_size[0]
ysize=imgs_size[1]

imgs_pos=scribus.getPosition(initial_imgs)
xpict=imgs_pos[0]
ypict=imgs_pos[1]

image_name=scribus.createImage(xpict, ypict, xsize, ysize)
scribus.lockObject(image_name)
scribus.setFillColor("Black",image_name)

if scribus.isLocked(initial_imgs):
    scribus.lockObject(initial_imgs)
scribus.deleteObject(initial_imgs)
scribus.setUnit(initial_units)



