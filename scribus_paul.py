import sys
import scribus
from collections import namedtuple
from my_messages import my_msg
object_info=namedtuple("object_info",["name","x","y","xs","ys","mleft","mright","mtop","mbottom","page_type"])


def check_doc_present():   
    if not scribus.haveDoc():
        scribus.messageBox(
            "Scribus -Script Error",
            "No document open",
            scribus.ICON_WARNING,
            scribus.BUTTON_OK)
        sys.exit(1)


# def acta_pos1D(n_picts, margin, pict_size, gutter):
#     return margin + (n_picts - 1) * (pict_size + gutter)


def pict_size1D(n_picts, margin1, margin2, gutter, page_size):
    return (page_size - margin1 - margin2 - (n_picts - 1) * gutter) / n_picts

def pict_pos1D(n_picts, margin, pict_size, gutter):
    return margin + (n_picts - 1) * (pict_size + gutter)

def get_page_info():
# get page margins, size and type (left or right)
    pagenum=scribus.currentPage()
    margins = scribus.getPageNMargins(pagenum)
    size = scribus.getPageNSize(pagenum)
    type_page = scribus.getPageType(pagenum)
    current_page=object_info(name=str(pagenum),x=0,y=0,xs=size[0],ys=size[1],mleft=margins[1],mright= margins[2],mtop=margins[0],mbottom= margins[3],page_type=type_page)
    return current_page

def page_available(page):
    return object_info(name=page.name,x=page.mleft,y=page.mtop,
    xs=page.xs-page.mleft-page.mright,
    ys=page.ys-page.mtop-page.mbottom,
    mleft=0,mright=0,mtop=0,mbottom=0,page_type=page.page_type)

def get_object_info(object_name):
    obj_size=scribus.getSize(object_name)
    xs = obj_size[0]
    ys = obj_size[1]
    obj_pos = scribus.getPosition(object_name)
    x=obj_pos[0]
    y=obj_pos[1]
    return object_info(name=object_name,x=x,y=y,xs=xs,ys=ys,mleft=0.0,mright=0.0,mtop=0.0,mbottom=0.0,page_type=0)

def set_object_info(object_name,x,y,xs,ys,mleft,mright,mtop,mbottom,page_type):
    return object_info(name=object_name,x=x,y=y,xs=xs,ys=ys,mleft=0.0,mright=0.0,mtop=0.0,mbottom=0.0,page_type=0)

def get_n_images_gutter(xnp=2,ynp=3,g=3.0):
    x_n_picts=int(scribus.valueDialog(my_msg["ti_img_x"], my_msg["msg_img_x"],str(xnp)))
    y_n_picts=int(scribus.valueDialog(my_msg["ti_img_y"], my_msg["msg_img_y"] ,str(ynp)))
    gutter=float(scribus.valueDialog(my_msg["ti_gutter"], my_msg["msg_gutter"] ,str(g)))
    return (x_n_picts,y_n_picts,gutter)

def movesize(obj):
    if scribus.isLocked(obj.name):
        scribus.lockObject(obj.name)
    scribus.moveObjectAbs(obj.x,obj.y , obj.name)
    scribus.sizeObject(obj.xs, obj.ys, obj.name)
    scribus.lockObject(obj.name)

def split_image(action,obj, x_n_picts=2, y_n_picts=3, gutter=1):
    # action can be "resize" or "create"
    new_xs = pict_size1D(x_n_picts, 0, 0, gutter, obj.xs)
    new_ys = pict_size1D(y_n_picts, 0,0, gutter, obj.ys)
    for nx in range(1, x_n_picts + 1):
        for ny in range(1, y_n_picts + 1):
            xpict = pict_pos1D(nx, obj.x, new_xs, gutter)
            ypict = pict_pos1D(ny, obj.y, new_ys, gutter)
            if (ny==1 and nx==1) and action=="resize":
                if scribus.isLocked(obj.name):
                    scribus.lockObject(obj.name)
                scribus.sizeObject(new_xs, new_ys, obj.name)
                scribus.lockObject(obj.name)
            else:
                image_name=scribus.createImage(xpict, ypict, new_xs, new_ys)
                scribus.setFillColor("Black",image_name)
                scribus.lockObject(image_name)


def create_1_image(obj, x_n_picts=2, y_n_picts=3, gutter=1,nx=1,ny=1):
    new_xs = pict_size1D(x_n_picts, 0, 0, gutter, obj.xs)
    new_ys = pict_size1D(y_n_picts, 0,0, gutter, obj.ys)
    xpict = pict_pos1D(nx, obj.x, new_xs, gutter)
    ypict = pict_pos1D(ny, obj.y, new_ys, gutter)   
    image_name=scribus.createImage(xpict, ypict, new_xs, new_ys)
    scribus.setFillColor("Black",image_name)
    scribus.lockObject(image_name)

def combine_images():
    all_imgs=[]
    for i in range(0, scribus.selectionCount()):
        all_imgs.append(scribus.getSelectedObject(i))
    # get the name of the first selected image which will be kept
    keep_img=all_imgs[0]
    # group the images to get the size and position of the total area
    initial_imgs=scribus.groupObjects(all_imgs)

    imgs_size=scribus.getSize(initial_imgs)
    xs=imgs_size[0]
    ys=imgs_size[1]

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
    scribus.sizeObject(xs, ys, keep_img)
    scribus.lockObject(keep_img)

def get_position4pict(x_n_picts,y_n_picts):
    position=False
    while not position:
        xypict=eval(scribus.valueDialog(my_msg["ti_1_img"], my_msg["msg_1_img"],"1,1"))
        if xypict[0]>x_n_picts:
            scribus.messageBox(my_msg["ti_x_error"],my_msg["msg_x_error"])
        elif xypict[1]>y_n_picts:
            scribus.messageBox(my_msg["ti_y_error"],my_msg["msg_y_error"])
        else:
            position=True
    return (xypict)

