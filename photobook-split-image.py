import scribus
from my_units import my_units
import scribus_paul as sp

sp.check_doc_present()
initial_units=scribus.getUnit()
scribus.setUnit(my_units)

initial_img=sp.get_object_info(scribus.getSelectedObject())
x_n_picts, y_n_picts, gutter=sp.get_n_images_gutter(xnp=2, ynp=1, g=1.0)

sp.split_image("resize",initial_img, x_n_picts, y_n_picts, gutter)

scribus.setUnit(initial_units)