import scribus
from my_units import my_units
import scribus_paul as sp

sp.check_doc_present()
initial_units = scribus.getUnit()
scribus.setUnit(my_units)

sp.combine_images()


scribus.setUnit(initial_units)
