import scribus
import scribus_paul as sp

sp.check_doc_present()
initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)

page=sp.get_page_info()
page_available=sp.page_available(page)
x_n_picts, y_n_picts, gutter=sp.get_n_images_gutter()
sp.split_image("create",page_available, x_n_picts, y_n_picts, gutter)

scribus.setUnit(initial_units)
