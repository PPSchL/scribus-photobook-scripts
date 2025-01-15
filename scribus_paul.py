import sys
import os
import pickle
import scribus
from collections import namedtuple


# pictures and text frames as well as pages are described by a named tuple which will be used to draw the object
# this tuples specifies the name, position (x,y), size (xs,ys), rotation (rot) margins (mleft,mright,mtop,mbottom), and page-type (left, right or "center")
# margins are 0 for pictures and text frames
object_info = namedtuple(
    "object_info",
    [
        "name",
        "x",
        "y",
        "xs",
        "ys",
        "rot",
        "mleft",
        "mright",
        "mtop",
        "mbottom",
        "page_type",
    ],
)

""" frame_rc specifies the parameters that completely define the form and position of any frame in a coordinate system
defined by the number of columns (c) and rows (r). Each frame will have a size defined by the number of columns and rows
it occupies and a position defined by the column and row it starts at (starting from 1, top left will be c=1, r=1).
The advantage of this system is that it is independent of page size
"""
frame_rc = namedtuple(
    "frame_rc",
    ["c", "r", "x_rc", "y_rc", "xs_rc", "ys_rc"],
)
""" frame_fr specifies the parameters that define the different frames in fractional units (ie fractions of the available space)
eg: a frame that takes up the whole area (page) would have a fractional size of 1 in both x and y coordinates and start at (0,0) tuple:(0,0,1,1)
this system is also independent of page size
this system also allows for rotated images, use "rot" parameter for rotation expressed as counterclockwise degrees
"""
frame_fr = namedtuple(
    "frame_fr",
    ["x_fr", "y_fr", "xs_fr", "ys_fr", "rot"],
)


def get_config_data(script_p):
    cfgpath = os.path.join(script_p, ".photobook", "phb.cfg")
    my_msg = {}
    my_defaults = {}
    my_units = scribus.UNIT_MILLIMETERS
    with open(cfgpath, "rb") as file4cfg:
        my_lang = pickle.load(file4cfg)
        my_units = pickle.load(file4cfg)
        my_msg = pickle.load(file4cfg)
        my_defaults = pickle.load(file4cfg)

    return (my_lang, my_msg, my_units, my_defaults)


def check_doc_present():
    # partially copied from Gregory Pittman, see https://opensource.com/sites/default/files/ebooks/pythonscriptingwithscribus.pdf
    if not scribus.haveDoc():
        scribus.messageBox(
            "Scribus -Script Error",
            "No document open",
            scribus.ICON_WARNING,
            scribus.BUTTON_OK,
        )
        sys.exit(1)


def pict_size1D(n_picts, margin1, margin2, gutter, page_size):
    # calculates the size of an individual picture knowing the number of pictures and the gutter between pictures
    # apply separately for x and y direction (1 dimensional 1D)
    return (page_size - margin1 - margin2 - (n_picts - 1) * gutter) / n_picts


def pict_pos1D(n_picts, margin, pict_size, gutter):
    # calculates the position of an individual picture knowing the picture size and the uggter between pictures
    return margin + (n_picts - 1) * (pict_size + gutter)


def get_unit_string(chosen_unit):
    # get the name of a unit knowing its scribus integer code
    if chosen_unit == scribus.UNIT_CENTIMETRES:
        str_unit = "cm"
    elif chosen_unit == scribus.UNIT_INCHES:
        str_unit = "inches"
    elif chosen_unit == scribus.UNIT_POINTS:
        str_unit = "points"
    elif chosen_unit == scribus.UNIT_PICAS:
        str_unit = "picas"
    elif chosen_unit == scribus.UNIT_CICERO:
        str_unit = "ciceros"
    else:  # mm by default
        str_unit = "mm"
    return str_unit


def get_page_info():
    # get page margins, size and type (left or right)
    pagenum = scribus.currentPage()
    margins = scribus.getPageNMargins(pagenum)
    size = scribus.getPageNSize(pagenum)
    type_page = scribus.getPageType(pagenum)
    current_page = object_info(
        name=str(pagenum),
        x=0,
        y=0,
        xs=size[0],
        ys=size[1],
        rot=0,
        mleft=margins[1],
        mright=margins[2],
        mtop=margins[0],
        mbottom=margins[3],
        page_type=type_page,
    )
    return current_page


def page_available(page):
    # get the available size of the page, substracting the margins
    return object_info(
        name=page.name,
        x=page.mleft,
        y=page.mtop,
        xs=page.xs - page.mleft - page.mright,
        ys=page.ys - page.mtop - page.mbottom,
        rot=0,
        mleft=0,
        mright=0,
        mtop=0,
        mbottom=0,
        page_type=page.page_type,
    )


def page_with_bleed(page, bleed):
    # get the size of the whole page including the bleed areas
    return object_info(
        name=page.name,
        x=-bleed,
        y=-bleed,
        xs=page.xs + 2 * bleed,
        ys=page.ys + 2 * bleed,
        rot=0,
        mleft=0,
        mright=0,
        mtop=0,
        mbottom=0,
        page_type=page.page_type,
    )


def get_orientation(area):  # area must be an object like a page or drawing area
    if area.xs / area.ys > 1.1:
        orientation = "Landscape"
    elif area.xs / area.ys < (1 / 1.1):
        orientation = "Portrait"
    else:
        orientation = "Square"
    return orientation


def get_object_info(object_name):
    # use scribus methods to define the parameters describing a scribus object
    obj_size = scribus.getSize(object_name)
    xs = obj_size[0]
    ys = obj_size[1]
    obj_pos = scribus.getPosition(object_name)
    x = obj_pos[0]
    y = obj_pos[1]
    rotation = scribus.getRotation(object_name)
    return object_info(
        name=object_name,
        x=x,
        y=y,
        xs=xs,
        ys=ys,
        rot=rotation,
        mleft=0.0,
        mright=0.0,
        mtop=0.0,
        mbottom=0.0,
        page_type=0,
    )


def set_object_info(
    object_name, x, y, xs, ys, rot, mleft, mright, mtop, mbottom, page_type
):
    return object_info(
        name=object_name,
        x=x,
        y=y,
        xs=xs,
        ys=ys,
        rot=rot,
        mleft=0.0,
        mright=0.0,
        mtop=0.0,
        mbottom=0.0,
        page_type=0,
    )


def rc2xy(rc, area, gutter):
    # transform from row/column type coordinates to xy coordinates
    # depends on the page or area to draw upon
    # can be passed on directly to create_image function after expansion of returned tuple
    def rc2size(size_rc, unit_rc, gutter):
        return size_rc * unit_rc + (size_rc - 1) * gutter

    unit_xs = pict_size1D(rc.c, 0, 0, gutter, area.xs)
    unit_ys = pict_size1D(rc.r, 0, 0, gutter, area.ys)
    xs = rc2size(rc.xs_rc, unit_xs, gutter)
    ys = rc2size(rc.ys_rc, unit_ys, gutter)
    x = pict_pos1D(rc.x_rc, area.x, unit_xs, gutter)
    y = pict_pos1D(rc.y_rc, area.y, unit_ys, gutter)
    return (x, y, xs, ys)


def fr2xy(fr, area):
    # transform from fractional type type coordinates to xy coordinates
    # depends on the page or area to draw upon
    # can be passed on directly to create_image function after expansion of returned tuple
    x = area.x + fr.x_fr * area.xs
    y = area.y + fr.y_fr * area.ys
    xs = fr.xs_fr * area.xs
    ys = fr.ys_fr * area.ys
    rot = fr.rot
    return (x, y, xs, ys, rot)


def get_n_images_gutter(my_msg, xnp, ynp, gutter):
    x_n_picts = int(
        scribus.valueDialog(my_msg["ti_img_x"], my_msg["msg_img_x"], str(xnp))
    )
    y_n_picts = int(
        scribus.valueDialog(my_msg["ti_img_y"], my_msg["msg_img_y"], str(ynp))
    )
    gutter = float(
        scribus.valueDialog(my_msg["ti_gutter"], my_msg["msg_gutter"], str(gutter))
    )
    return (x_n_picts, y_n_picts, gutter)


def movesize(obj):
    if scribus.isLocked(obj.name):
        scribus.lockObject(obj.name)
    scribus.moveObjectAbs(obj.x, obj.y, obj.name)
    scribus.sizeObject(obj.xs, obj.ys, obj.name)
    scribus.rotateObjectAbs(obj.rot, obj.name)
    scribus.lockObject(obj.name)


def split_image(action, obj, x_n_picts, y_n_picts, gutter):
    # have to rotate all final images to the same degree around topleft corner
    # each image has different topleft corner=> group images and rotate as a whole
    # but need to save rotation of initial image
    rotation = obj.rot
    selected_imgs = []
    new_xs = pict_size1D(x_n_picts, 0, 0, gutter, obj.xs)
    new_ys = pict_size1D(y_n_picts, 0, 0, gutter, obj.ys)
    for nx in range(1, x_n_picts + 1):
        for ny in range(1, y_n_picts + 1):
            xpict = pict_pos1D(nx, obj.x, new_xs, gutter)
            ypict = pict_pos1D(ny, obj.y, new_ys, gutter)
            if (ny == 1 and nx == 1) and action == "resize":
                # first image only has to be resized and rotation put to 0,
                # because other images will be created with rotation = 0
                # and need this first frame to get the topleft corner for final rotation
                if scribus.isLocked(obj.name):
                    scribus.lockObject(obj.name)
                scribus.sizeObject(new_xs, new_ys, obj.name)
                selected_imgs.append(obj.name)
                scribus.rotateObjectAbs(0, obj.name)
                scribus.lockObject(obj.name)
            else:
                # other images are created and kept track of in the selected_imgs list for final rotation
                image_name = scribus.createImage(xpict, ypict, new_xs, new_ys)
                scribus.setFillColor("Black", image_name)
                selected_imgs.append(image_name)
                scribus.lockObject(image_name)
    # have to rotate the final images around the topleft corner=> group all images, topleft corner is thus conserved
    group_imgs = scribus.groupObjects(selected_imgs)
    scribus.rotateObjectAbs(rotation, group_imgs)
    # ungroup to get the final independent images
    scribus.unGroupObjects(group_imgs)


def create_1_image(obj, x_n_picts, y_n_picts, gutter, nx, ny):
    # create image in row/column for mat by its coordinates
    new_xs = pict_size1D(x_n_picts, 0, 0, gutter, obj.xs)
    new_ys = pict_size1D(y_n_picts, 0, 0, gutter, obj.ys)
    xpict = pict_pos1D(nx, obj.x, new_xs, gutter)
    ypict = pict_pos1D(ny, obj.y, new_ys, gutter)
    image_name = scribus.createImage(xpict, ypict, new_xs, new_ys)
    scribus.setFillColor("Black", image_name)
    scribus.lockObject(image_name)


def create_image(xpict, ypict, xs, ys, rot=0):
    # create image in xy coordinates, rotation does not have to be specified, default 0 degrees
    image_name = scribus.createImage(xpict, ypict, xs, ys)
    if rot != 0:
        scribus.rotateObjectAbs(rot, image_name)
    scribus.setFillColor("Black", image_name)
    scribus.lockObject(image_name)


def draw_list_of_images(images):
    # images must be tuple of (x,y,xs,ys, [rot])
    for iter_image in images:
        create_image(
            *iter_image
        )  # expand image tuple iter_image to get 4 or 5 (if rot is specified) parameters


def get_nlines_ratio(my_msg, n_lines, ratio, gutter, direction, aspect_type):
    # dialog to get information on the number of rows, ratio of primary image and gutter for asymmetric pages
    n_lines = int(
        scribus.valueDialog(my_msg["ti_nlines"], my_msg["msg_nlines"], str(n_lines))
    )
    ratio = eval(
        scribus.valueDialog(my_msg["ti_ratio"], my_msg["msg_ratio"], str(ratio))
    )
    gutter = float(
        scribus.valueDialog(my_msg["ti_gutter"], my_msg["msg_gutter"], str(gutter))
    )
    direction = scribus.valueDialog(
        my_msg["ti_direction"], my_msg["msg_direction"], str(direction)
    )
    aspect_type = scribus.valueDialog(
        my_msg["ti_aspect"], my_msg["msg_aspect"], str(aspect_type)
    )
    return (n_lines, ratio, gutter, direction, aspect_type)


def make_list_of_asymmetric_images(
    my_msg, obj, n_rows, ratio, gutter, direction, aspect_type
):
    # create a list of x,y,xs,ys tuples for the different images of an asymmetric page
    def not_worthwile():
        scribus.messageBox(my_msg["ti_ratio_error"], my_msg["msg_ratio_error"])
        return "ratio error"

    # calculate row height of images as a function of page size, gutter  and number of rows
    ys = pict_size1D(n_rows, 0, 0, gutter, obj.ys)
    # ratio parameter defines x size of primary image
    xs1 = ys * ratio

    if (
        xs1 > obj.xs
    ):  # if primary image x size greater than page size, not worthwhile...
        image_list = not_worthwile()
        return image_list
    else:
        # calculate remaining x size for second image
        xs2 = obj.xs - xs1 - gutter
        if xs2 / ys < 0.5:  # if ratio of second image too extreme, reject
            image_list = not_worthwile()
            return image_list
        else:
            image_list = []
            for image_row in range(1, (n_rows + 1)):
                # calculate x and y position
                # y = topleft coordinate of row
                y = pict_pos1D(image_row, obj.y, ys, gutter)
                # x1 and x2 depend on direction
                x1 = obj.x
                x2 = x1 + xs1 + gutter
                if direction != "left2right":
                    x2 = x1
                    x1 = x1 + xs2 + gutter
                # add image defined as a tuple to list
                image_list.append((x1, y, xs1, ys))
                image_list.append((x2, y, xs2, ys))
                # if inversion at each new line: invert images at the end of each line
                if aspect_type != "constant":
                    if direction == "left2right":
                        direction = "right2left"
                    else:
                        direction = "left2right"
            return image_list


def combine_images():
    all_imgs = []
    for i in range(0, scribus.selectionCount()):
        all_imgs.append(scribus.getSelectedObject(i))

    # get the name of the first selected image which will be kept
    keep_img = all_imgs[0]
    # get the rotation of the first selected object that will be used to set the rotation of the combined image
    rotation = scribus.getRotation(keep_img)

    # group the images to get the size and position of the total area
    grouped_imgs = scribus.groupObjects(all_imgs)
    # rotate all the frames to 0 degrees, to avoid increasing the group size
    # because rotated images are larger in x and y directions
    # however this operation does not work with the current version of the scripter API (previous size conserved)
    # and would anyway not be valid for groups of disparate rotations of individual images
    # kept nonetheless for potential future use
    # scribus.rotateObjectAbs(0, grouped_imgs)
    scribus.setRotation(0, grouped_imgs)

    imgs_size = scribus.getSize(grouped_imgs)
    xs = imgs_size[0]
    ys = imgs_size[1]

    imgs_pos = scribus.getPosition(grouped_imgs)
    xpict = imgs_pos[0]
    ypict = imgs_pos[1]

    # ungroup to be able to delete all the images but the first
    # grouped_images and all_images are the same images
    scribus.unGroupObjects(grouped_imgs)
    # remove first image (which is being kept) from the list
    # then delete all the remaining objects
    del all_imgs[0]
    for img_name in all_imgs:
        if scribus.isLocked(img_name):
            scribus.lockObject(img_name)
        scribus.deleteObject(img_name)

    # move, resize and rotate the first image which will occupy the area of all the selected images
    if scribus.isLocked(keep_img):
        scribus.lockObject(keep_img)
    scribus.moveObjectAbs(xpict, ypict, keep_img)
    scribus.sizeObject(xs, ys, keep_img)
    scribus.rotateObjectAbs(rotation, keep_img)
    scribus.lockObject(keep_img)
    return keep_img


def get_position4pict(my_msg, x_n_picts, y_n_picts):
    # dialog to ask for a valid number of rows and columns to draw a single picture within a row/column grid
    position = False
    while not position:
        xypict = eval(
            scribus.valueDialog(my_msg["ti_1_img"], my_msg["msg_1_img"], "1,1")
        )
        if xypict[0] > x_n_picts:
            scribus.messageBox(my_msg["ti_x_error"], my_msg["msg_x_error"])
        elif xypict[1] > y_n_picts:
            scribus.messageBox(my_msg["ti_y_error"], my_msg["msg_y_error"])
        else:
            position = True
    return xypict
