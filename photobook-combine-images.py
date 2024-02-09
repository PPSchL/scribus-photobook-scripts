import scribus
import scribus_paul as sp

sp.check_doc_present()
initial_units=scribus.getUnit()
scribus.setUnit(scribus.UNIT_MILLIMETERS)

sp.combine_images()


scribus.setUnit(initial_units)



