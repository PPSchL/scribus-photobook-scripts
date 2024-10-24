import scribus
from collections import namedtuple
from script_path import script_path
import scribus_paul as sp
from scribus_paul import frame_rc, rc2xy

from tkinter import *
from tkinter.ttk import *


# a layout in row/column format is defined by the number of landscape photos/frames (L), portraits (P) and squares (S).
# Squares are not perfect squares but can differ from a square by xx%.
# as some layouts can have the same number of L,P and S and still be different eg, LPS vs SPL the number n spécifies the different layouts starting from 1
# the named tuple layout_rc  will then be used as key in the dictionary of all possible layouts as a list of frame_rc frame specifications
# the chosen layout can then be drawn by recalculating the positions and sizes as a function of page and gutter (plus maybe bleed) sizes
layout_rc = namedtuple("layout_rc", ["name", "L", "P", "S", "n"])


def draw_layout(layout, area, gutter):
    for frame_i in layout:
        sp.create_image(*rc2xy(frame_i, area, gutter))
    main_window.destroy()
    return


layouts = {
    layout_rc(name="4P", L=0, P=4, S=0, n=1): [
        frame_rc(c=2, r=2, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="2L", L=2, P=0, S=0, n=1): [
        frame_rc(c=2, r=2, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="6P-1", L=0, P=6, S=0, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="6P-2", L=0, P=6, S=0, n=2): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="6P-3", L=0, P=6, S=0, n=3): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="2P4L-1", L=4, P=2, S=0, n=1): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=2),
    ],
}

# take care of Units and initialize default values
sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)
# get page information from scribus
gutter = my_defaults["gutter"]
page = sp.get_page_info()
area = sp.page_available(page)
orientation = sp.get_orientation(area)


# construct generator for the layouts corresponding to the request
# selected_layouts = (l_key for l_key in layouts.keys() if (l_key.L, l_key.P) == (L, P))
# for lkey in selected_layouts:
#     draw_layout(layouts[lkey], area, gutter)


def filter_layouts(L, P, S, layouts):
    # construct generator for the layouts corresponding to the request: if () enclose the expression makes generator, with [] makes list
    selected_layouts = (
        l_key for l_key in layouts.keys() if (l_key.L, l_key.P, l_key.S) == (L, P, S)
    )
    return selected_layouts


def filter_similar(L, P, S, layouts, LPSpriority):
    if LPSpriority == "L":
        LPScompare_p = "l_key.L"
        LPScomparep = L
        LPScompare_np = "(sum(l_key.P,l_key.S))"
        LPScomparenp = P + S
    elif LPSpriority == "P":
        LPScompare_p = "l_key.P"
        LPScomparep = P
        LPScompare_np = "(sum(l_key.L,l_key.S))"
        LPScomparenp = L + S
    else:
        LPScompare_p = "l_key.S"
        LPScomparep = S
        LPScompare_np = "(sum(l_key.P,l_key.L))"
        LPScomparenp = L + P
    selected_layouts = (
        l_key
        for l_key in layouts.keys()
        if (
            (l_key.L, l_key.P, l_key.S) != (L, P, S)
            and eval(LPScompare_p) == LPScomparep
            and eval(LPScompare_np) == LPScomparenp
        )
    )
    return selected_layouts


def filter_same_number(L, P, S, layouts):
    # select all layouts with the same total number of photos
    selected_layouts = (
        l_key
        for l_key in layouts.keys()
        if (
            (l_key.L, l_key.P, l_key.S) != (L, P, S)
            and sum(l_key.L, l_key.P, l_key.S) == sum(L, P, S)
        )
    )
    return selected_layouts


def select_draw(L, P, S, layouts, orientation):
    choose_layout = Toplevel(
        main_window,
    )
    choose_layout.title("Choose layout")
    x0 = main_window.winfo_x()
    y0 = main_window.winfo_y()
    choose_layout.geometry("+%d+%d" % (x0 + 20, y0 + 100))
    # choose_frame = Frame(choose_layout)
    # choose_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    # choose_layout.columnconfigure(0, weight=1)
    # choose_layout.rowconfigure(0, weight=1)

    # the same layout can be used for portrait and landscape,
    # landscapes become portraits and vice-versa=> just invert in teh filter function
    if orientation == "Portrait":
        ok_layouts = filter_layouts(L, P, S, layouts)
    elif orientation == "Landscape":
        ok_layouts = filter_layouts(P, L, S, layouts)
    else:  # orientation=square TODO
        pass
    draw_buttons = {}
    button_r = 0
    button_c = 0
    for lkey in ok_layouts:
        draw_buttons[lkey] = Button(
            choose_layout,
            text=lkey.name,
            command=lambda lkey=lkey: draw_layout(
                layouts[lkey], area, gutter
            ),  # lambda lkey=lkey makes sure lkey is assigned the value of the key, not the last generated value
        )
        draw_buttons[lkey].grid(row=button_r, column=button_c)
        button_c += 1
    # similar layouts
    for or_i in ("L", "P", "S"):
        if orientation == "Portrait":
            similar_layouts = filter_similar(L, P, S, layouts, or_i)
        elif orientation == "Landscape":
            similar_layouts = filter_layouts(P, L, S, layouts, or_i)
        else:  # orientation=square TODO
            pass
        draw_buttons_similar = {}
        button_r += 2
        button_c = 0
        for lkey in similar_layouts:
            draw_buttons_similar[lkey] = Button(
                choose_layout,
                text=lkey.name,
                command=lambda lkey=lkey: draw_layout(
                    layouts[lkey], area, gutter
                ),  # lambda lkey=lkey makes sure lkey is assigned the value of the key, not the last generated value
            )
            draw_buttons_similar[lkey].grid(row=button_r, column=button_c)
            button_c += 1
    button_r += 2
    stop_top = Button(
        choose_layout,
        text="None are convenient, go back to ratio specification",
        command=choose_layout.destroy,
    )
    stop_top.grid(row=button_r, columnspan=10, sticky="nsew")


# *** tkinter loop
main_window = Tk()
style = Style()
style.theme_use("classic")
# style.configure("choosel.TFrame", background="DeepSkyBlue")
main_window.title("Build complex photo page")
main_frame = Frame(main_window, padding="2 2 4 4")
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(0, weight=1)

L_number = StringVar(value="0")
P_number = StringVar(value="6")
S_number = StringVar(value="0")


explication = Label(
    main_frame,
    text="Please enter the number of Landscape, Portrait and Square photographs",
)
explication.grid(row=0, column=0)

L_number_label = Label(main_frame, text="Landscape")
L_number_label.grid(row=1, column=0)
L_number_e = Entry(main_frame, textvariable=L_number)
L_number_e.grid(row=2, column=0)

P_number_label = Label(main_frame, text="Portrait")
P_number_label.grid(row=1, column=1)
P_number_e = Entry(main_frame, textvariable=P_number)
P_number_e.grid(row=2, column=1)
P_number.trace_add(
    "write",
    lambda: select_draw(
        eval(L_number_e.get()),
        eval(P_number_e.get()),
        eval(S_number_e.get()),
        layouts,
        orientation,
    ),
)

S_number_label = Label(main_frame, text="Square")
S_number_label.grid(row=1, column=2)
S_number_e = Entry(main_frame, textvariable=S_number)
S_number_e.grid(row=2, column=2)


do_it = Button(
    main_frame,
    text="Ok, show potenial layouts",
    command=lambda: select_draw(
        eval(L_number_e.get()),
        eval(P_number_e.get()),
        eval(S_number_e.get()),
        layouts,
        orientation,
    ),
)
do_it.grid(row=8, column=0)
# select_draw(
#     eval(L_number_e.get()), eval(P_number_e.get()), eval(S_number_e.get()), layouts
# )

stop_it = Button(main_frame, text="Finished, close all", command=main_window.destroy)
stop_it.grid(row=8, column=1)


main_window.mainloop()


# end of Tkinter loop
scribus.setUnit(initial_units)
