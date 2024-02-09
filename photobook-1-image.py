import scribus
import scribus_paul as sp

sp.check_doc_present()
initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)

page=sp.get_page_info()
page_available=sp.page_available(page)
x_n_picts, y_n_picts, gutter=sp.get_n_images_gutter()
nx, ny=sp.get_position4pict(x_n_picts,y_n_picts)
sp.create_1_image(page_available, x_n_picts, y_n_picts, gutter,nx,ny)

scribus.setUnit(initial_units)

