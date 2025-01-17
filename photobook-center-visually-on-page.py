import scribus
from script_path import script_path
import scribus_paul as sp

sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)
page = sp.get_page_info()
page_available = sp.page_available(page)

if scribus.selectionCount() < 1:
    scribus.messageBox(
        "Scribus-Script Error",
        "No selection, need to select an image before centering it!",
        scribus.ICON_WARNING,
        scribus.BUTTON_OK,
    )
else:
    if scribus.selectionCount() == 1:  # single image to center
        initial_img = sp.get_object_info(scribus.getSelectedObject())
        sp.center_visual(initial_img, page_available, 2.5, 2.5)
    else:  # want to center a group of images
        all_imgs = []
        for i in range(0, scribus.selectionCount()):
            all_imgs.append(scribus.getSelectedObject(i))
        # group the images to get the size and position of the total area
        grouped_imgs = scribus.groupObjects(all_imgs)
        initial_group = sp.get_object_info(grouped_imgs)
        # visually center the group, then ungroup
        sp.center_visual(
            initial_group,
            page_available,
            my_defaults["visual_center_xoffset"],
            my_defaults["visual_center_yoffset"],
        )
        scribus.unGroupObjects(grouped_imgs)
        # ungrouping unlocks the images therefore
        # lock all images using their name that has not changed
        for img in all_imgs:
            if not scribus.isLocked(img):
                scribus.lockObject(img)
        scribus.deselectAll()

scribus.setUnit(initial_units)
