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
#create list of all selected images
all_imgs=[]
for i in range(0, scribus.selectionCount()):
	 all_imgs.append(scribus.getSelectedObject(i))
# get the name of the first selected image which will be kept
keep_img=all_imgs[0]
# group the images to get the size and position of the total area
initial_imgs=scribus.groupObjects(all_imgs)

imgs_size=scribus.getSize(initial_imgs)
xsize=imgs_size[0]
ysize=imgs_size[1]

imgs_pos=scribus.getPosition(initial_imgs)
xpict=imgs_pos[0]
ypict=imgs_pos[1]

# ungroup to delete all the images but the first
scribus.unGroupObjects(initial_imgs)
del all_imgs[0]
for img_name in all_imgs:
	if scribus.isLocked(img_name):
		scribus.lockObject(img_name)
	scribus.deleteObject(img_name)

# move and resize the first image which will occupy the area of all the selected images
if scribus.isLocked(keep_img):
	scribus.lockObject(keep_img)
scribus.moveObjectAbs(xpict,ypict , keep_img)
scribus.sizeObject(xsize, ysize, keep_img)
scribus.lockObject(keep_img)
#image_name=scribus.createImage(xpict, ypict, xsize, ysize)
#scribus.setFillColor("Black",image_name)

scribus.setUnit(initial_units)
