# import sys
import scribus
from script_path import script_path

# from collections import namedtuple
import scribus_paul as sp


sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

if scribus.selectionCount() < 2:
    scribus.messageBox(
        "Scribus-Script Error",
        "Not enough frames to swap, need at least 2",
        scribus.ICON_WARNING,
        scribus.BUTTON_OK,
    )
else:
    IMG1 = sp.get_object_info(scribus.getSelectedObject(0))
    IMG2 = sp.get_object_info(scribus.getSelectedObject(1))
    # as tuples are immutable, create new namedtuple keeping the xy coordinates but changing the name and the content (eg text vs image etc) and size of the other frame
    new_img1 = sp.object_info(
        name=IMG2.name,
        x=IMG1.x,
        y=IMG1.y,
        xs=IMG2.xs,
        ys=IMG2.ys,
        rot=IMG2.rot,
        mleft=0.0,
        mright=0.0,
        mtop=0.0,
        mbottom=0.0,
        page_type=0,
    )
    new_img2 = sp.object_info(
        name=IMG1.name,
        x=IMG2.x,
        y=IMG2.y,
        xs=IMG1.xs,
        ys=IMG1.ys,
        rot=IMG1.rot,
        mleft=0.0,
        mright=0.0,
        mtop=0.0,
        mbottom=0.0,
        page_type=0,
    )
    sp.movesize(new_img1)
    sp.movesize(new_img2)

scribus.setUnit(initial_units)
