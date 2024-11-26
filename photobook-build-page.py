import os
import scribus
from collections import namedtuple
from script_path import script_path
import scribus_paul as sp
from scribus_paul import frame_rc, rc2xy, get_unit_string, frame_fr, fr2xy

from tkinter import *
from tkinter.ttk import *


# a layout in row/column format is defined by the number of landscape photos/frames (L), portraits (P) and squares (S).
# Squares are not perfect squares but can differ from a square by xx%.
# as some layouts can have the same number of L,P and S and still be different eg, LPS vs SPL the number n spécifies the different layouts starting from 1
# the named tuple layout_rc  will then be used as key in the dictionary of all possible layouts as a list of frame_rc frame specifications
# the chosen layout can then be drawn by recalculating the positions and sizes as a function of page and gutter (plus maybe bleed) sizes
layout_rc = namedtuple("layout_rc", ["name", "L", "P", "S", "n"])
layout_fr = namedtuple("layout_fr", ["name", "L", "P", "S", "n"])

layouts = {
    layout_rc(name="L0P1S0-1", L=0, P=1, S=0, n=1): [
        frame_rc(c=1, r=1, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P2S0-1", L=0, P=2, S=0, n=1): [
        frame_rc(c=2, r=1, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=1, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L2P0S0-1", L=2, P=0, S=0, n=1): [
        frame_rc(c=2, r=2, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P0S1-1", L=1, P=0, S=1, n=1): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P0S1-2", L=1, P=0, S=1, n=2): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L0P0S3-1", L=0, P=0, S=3, n=1): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P0S3-2", L=0, P=0, S=3, n=2): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=2),
    ],
    layout_rc(name="L3P0S0-1", L=3, P=0, S=0, n=1): [
        frame_rc(c=1, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=1, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=1, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L1P2S0-1", L=1, P=2, S=0, n=1): [
        frame_rc(c=2, r=2, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L1P2S0-2", L=1, P=2, S=0, n=2): [
        frame_rc(c=2, r=2, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L0P4S0-1", L=0, P=4, S=0, n=1): [
        frame_rc(c=2, r=2, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=2, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P3S1-1", L=0, P=3, S=1, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=3, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P3S1-2", L=0, P=3, S=1, n=2): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=3, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L2P0S2-1", L=2, P=0, S=2, n=1): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L2P0S2-2", L=2, P=0, S=2, n=2): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L2P0S2-3", L=2, P=0, S=2, n=3): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P1S2-1", L=1, P=1, S=2, n=1): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P1S2-2", L=1, P=1, S=2, n=2): [
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P1S2-3", L=1, P=1, S=2, n=3): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P1S2-4", L=1, P=1, S=2, n=4): [
        frame_rc(c=2, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P3S0-1", L=1, P=3, S=0, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=3, ys_rc=1),
    ],
    layout_rc(name="L1P3S0-2", L=1, P=3, S=0, n=2): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=3, ys_rc=1),
    ],
    layout_rc(name="L1P3S0-3", L=1, P=3, S=0, n=3): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=3, ys_rc=1),
    ],
    layout_rc(name="L1P3S0-4", L=1, P=3, S=0, n=4): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=3, ys_rc=1),
    ],
    layout_rc(name="L0P4S0-2", L=0, P=4, S=0, n=2): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=3),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P4S0-3", L=0, P=4, S=0, n=3): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=3),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P1S4-1", L=0, P=1, S=4, n=1): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P1S4-2", L=0, P=1, S=4, n=2): [
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P1S4-3", L=0, P=1, S=4, n=3): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P1S4-4", L=0, P=1, S=4, n=4): [
        frame_rc(c=2, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L4P1S0-1", L=4, P=1, S=0, n=1): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=4),
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L4P1S0-2", L=4, P=1, S=0, n=2): [
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=4),
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L1P4S0-1", L=1, P=4, S=0, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P4S0-2", L=1, P=4, S=0, n=2): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P4S0-3", L=1, P=4, S=0, n=3): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P4S0-4", L=1, P=4, S=0, n=4): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P4S0-5", L=1, P=4, S=0, n=5): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P4S0-6", L=1, P=4, S=0, n=6): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P4S0-7", L=1, P=4, S=0, n=7): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L1P4S0-8", L=1, P=4, S=0, n=8): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L0P0S6-1", L=0, P=0, S=6, n=1): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L4P2S0-1", L=4, P=2, S=0, n=1): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=2),
    ],
    layout_rc(name="L4P2S0-2", L=4, P=2, S=0, n=2): [
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=2),
    ],
    layout_rc(name="L4P2S0-3", L=4, P=2, S=0, n=3): [
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=2),
    ],
    layout_rc(name="L4P2S0-4", L=4, P=2, S=0, n=4): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=2),
    ],
    layout_rc(name="L4P2S0-5", L=4, P=2, S=0, n=5): [
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=2),
    ],
    layout_rc(name="L4P2S0-6", L=4, P=2, S=0, n=6): [
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=2),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=2),
    ],
    layout_rc(name="L6P0S0-1", L=6, P=0, S=0, n=1): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L6P0S0-2", L=6, P=0, S=0, n=2): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L6P0S0-3", L=6, P=0, S=0, n=3): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L6P0S0-4", L=6, P=0, S=0, n=4): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L6P0S0-5", L=6, P=0, S=0, n=5): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
    ],
    layout_rc(name="L0P6S0-1", L=0, P=6, S=0, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P6S0-2", L=0, P=6, S=0, n=2): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P6S0-3", L=0, P=6, S=0, n=3): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P6S0-4", L=0, P=6, S=0, n=4): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L3P3S0-1", L=3, P=3, S=0, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L3P3S0-2", L=3, P=3, S=0, n=2): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L3P3S0-3", L=3, P=3, S=0, n=3): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L3P3S0-4", L=3, P=3, S=0, n=4): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L2P5S0-1", L=2, P=5, S=0, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L2P5S0-2", L=2, P=5, S=0, n=2): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L2P5S0-3", L=2, P=5, S=0, n=3): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L2P5S0-4", L=2, P=5, S=0, n=4): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L2P5S0-5", L=2, P=5, S=0, n=5): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L2P5S0-6", L=2, P=5, S=0, n=6): [
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=2, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L8P0S0-1", L=8, P=0, S=0, n=1): [
        frame_rc(c=2, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P9S0-1", L=0, P=9, S=0, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L0P13S0-1", L=0, P=13, S=0, n=1): [
        frame_rc(c=4, r=4, x_rc=2, y_rc=2, xs_rc=2, ys_rc=2),
        frame_rc(c=4, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=4, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=4, y_rc=2, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=4, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=3, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=4, y_rc=4, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L1P8S0-1", L=1, P=8, S=0, n=1): [
        frame_rc(c=4, r=4, x_rc=1, y_rc=2, xs_rc=4, ys_rc=2),
        frame_rc(c=4, r=4, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=4, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=1, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=2, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=3, y_rc=4, xs_rc=1, ys_rc=1),
        frame_rc(c=4, r=4, x_rc=4, y_rc=4, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L1P6S0-1", L=1, P=6, S=0, n=1): [
        frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=3, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=3, r=3, x_rc=3, y_rc=3, xs_rc=1, ys_rc=1),
    ],
    layout_rc(name="L1P0S4-1", L=1, P=0, S=4, n=1): [
        frame_rc(c=2, r=3, x_rc=1, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=1, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=2, xs_rc=2, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=1, y_rc=3, xs_rc=1, ys_rc=1),
        frame_rc(c=2, r=3, x_rc=2, y_rc=3, xs_rc=1, ys_rc=1),
    ],
}
layouts_fr = {
    layout_fr(name="L1P1S0-1-fr", L=1, P=1, S=0, n=1): [
        frame_fr(
            x_fr=0.0350594594, y_fr=0.4786823105, xs_fr=0.9567567568, ys_fr=0.4259927798
        ),
        frame_fr(
            x_fr=0.4738162462, y_fr=0.0606642599, xs_fr=0.4432432432, ys_fr=0.4508447653
        ),
    ],
}


def draw_layout(layout, area, gutter, orientation, tkwindow="none"):
    for frame_i in layout:
        if orientation == "Landscape":
            frame_draw = frame_rc(
                c=frame_i.r,
                r=frame_i.c,
                x_rc=frame_i.y_rc,
                y_rc=frame_i.c - frame_i.x_rc - frame_i.xs_rc + 2,
                xs_rc=frame_i.ys_rc,
                ys_rc=frame_i.xs_rc,
            )
        elif orientation == "Portrait":
            frame_draw = frame_i
        else:
            pass  # square yet TODO
        sp.create_image(*rc2xy(frame_draw, area, gutter))
    if tkwindow != "none":
        tkwindow.destroy()
    return


def draw_layout_fr(layout, area, orientation, tkwindow="none"):
    for frame_i in layout:
        if orientation == "Landscape":
            pass  # TODO
        elif orientation == "Portrait":
            frame_draw = frame_i
        else:
            pass  # square yet TODO
        sp.create_image(*fr2xy(frame_draw, area))
    if tkwindow != "none":
        tkwindow.destroy()
    return


def filter_layouts(L, P, S, layouts):
    # construct generator for the layouts corresponding to the request: if () enclose the expression makes generator, with [] makes list
    selected_layouts = (
        l_key for l_key in layouts.keys() if (l_key.L, l_key.P, l_key.S) == (L, P, S)
    )
    return selected_layouts


def filter_similar(L, P, S, layouts, LPSpriority):
    # select layputs with the same number of either L, P or S photos (depending on LPSpriority)
    # but allow the o
    # but any that change one L or P to S, or keep P+L constant in case of priority to S
    if LPSpriority == "L":
        LPScompare_p = "l_key.L"
        LPScomparep = L
        # LPScompare_np = "l_key.P+l_key.S)"
        # LPScomparenp = P + S
        LPScompare_np = "(l_key.P,l_key.S)"
        LPScomparenp = (P - 1, S + 1)
    elif LPSpriority == "P":
        LPScompare_p = "l_key.P"
        LPScomparep = P
        # LPScompare_np = "l_key.L+l_key.S"
        # LPScomparenp = L + S
        LPScompare_np = "(l_key.L,l_key.S)"
        LPScomparenp = (L - 1, S + 1)
    else:  # LPSpriority="S"
        LPScompare_p = "l_key.S"
        LPScomparep = S
        LPScompare_np = "l_key.P+l_key.L"
        LPScomparenp = L + P
    selected_layouts = (
        l_key
        for l_key in layouts.keys()
        if (
            (l_key.L, l_key.P, l_key.S) != (L, P, S)
            and (eval(LPScompare_p) == LPScomparep)
            and (eval(LPScompare_np) == LPScomparenp)
        )
    )
    return selected_layouts


def filter_same_total(L, P, S, layouts):
    # select all layouts with the same total number of photos
    selected_layouts = (
        l_key
        for l_key in layouts.keys()
        if (
            (l_key.L, l_key.P, l_key.S) != (L, P, S)
            and (l_key.L + l_key.P + l_key.S) == (L + P + S)
        )
    )
    return selected_layouts


def select_and_draw(
    root, button_imgs, L, P, S, gutter, layouts, orientation, buttons_per_row
):
    def draw_buttons(filtered_layouts, button_r, selection_window, buttons_per_row):
        # draws the button to a specified number of buttons per row
        # then increases the row coordinate
        # returns a tuple specifying success and new row coordinate
        button_dict = {}
        button_r_i = button_r
        button_c = 0
        for lkey in filtered_layouts:
            button_dict[lkey] = Button(
                selection_window,
                text=lkey.name,
                image=button_imgs[lkey],
                compound=TOP,  # "image",
                command=lambda lkey=lkey: draw_layout(
                    layouts[lkey], area, gutter, orientation, root
                ),  # lambda lkey=lkey makes sure lkey is assigned the value of the key, not the last generated value
            )
            button_dict[lkey].grid(row=button_r, column=button_c)
            # new row if button number equals buttons_per_row
            # button_c starts at 0, therefore number of buttons on row = (button_c+1)
            if button_c > 0 and (button_c + 1) % buttons_per_row == 0:
                button_r += 1
                button_c = 0
            else:
                button_c += 1
        if button_c > 0 or button_r > button_r_i:
            return ("success", button_r)
        else:
            return ("no layouts",)

    choose_layout = Toplevel(
        root,
    )
    choose_layout.title("Choose layout")
    x0 = root.winfo_x()
    y0 = root.winfo_y()
    choose_layout.geometry("+%d+%d" % (x0 + 20, y0 + 100))
    # TODO choose_frame = Frame(choose_layout)
    # choose_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    # choose_layout.columnconfigure(0, weight=1)
    # choose_layout.rowconfigure(0, weight=1)

    # the same layout can be used for portrait and landscape,
    # landscapes become portraits and vice-versa=> just invert in the filter function
    exact_label = Label(choose_layout, text="Perfect correspondance")
    exact_label.grid(row=0, column=0)
    if orientation == "Portrait":
        ok_layouts = filter_layouts(L, P, S, layouts)
    elif orientation == "Landscape":
        ok_layouts = filter_layouts(P, L, S, layouts)
    else:  # orientation=square TODO
        pass
    button_r = 2
    # draw the buttons and simultaneously test for success
    if (
        draw_buttons(ok_layouts, button_r, choose_layout, buttons_per_row)[0]
        == "no layouts"
    ):
        # only propose similar layouts if perfect fit does not exist
        exact_label.text = "No perfect correpondance found"
        button_r += 1
        similar_label = Label(choose_layout, text="Approximate correspondance")
        similar_label.grid(row=button_r, column=0)
        for or_i in ("L", "P"):
            if orientation == "Portrait":
                similar_layouts = filter_similar(L, P, S, layouts, or_i)
            elif orientation == "Landscape":
                similar_layouts = filter_similar(P, L, S, layouts, or_i)
            else:  # orientation=square TODO
                pass
            button_r += 2
            draw_outcome = draw_buttons(
                similar_layouts, button_r, choose_layout, buttons_per_row
            )
            if draw_outcome[0] == "success":
                button_r = draw_outcome[1]

        button_r += 1
        same_total_label = Label(choose_layout, text="All with same number of pictures")
        same_total_label.grid(row=button_r, column=0)
        button_r += 1
        same_total = filter_same_total(L, P, S, layouts)
        draw_outcome = draw_buttons(
            same_total, button_r, choose_layout, buttons_per_row
        )
        if draw_outcome[0] == "success":
            button_r = draw_outcome[1]

    button_r += 1
    stop_top = Button(
        choose_layout,
        text="None are convenient, go back to ratio specification",
        command=choose_layout.destroy,
    )
    stop_top.grid(row=button_r, columnspan=10, sticky="nsew")


def build_main(page, area, layouts, gutter, my_units):
    orientation = sp.get_orientation(area)

    # *** tkinter loop
    root = Tk()
    style = Style()
    style.theme_use("classic")

    # style.configure("choosel.TFrame", background="DeepSkyBlue")
    root.title("Build complex photo page")
    main_frame = Frame(root, padding="2 2 4 4")
    main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    L_number = StringVar(value="0")
    P_number = StringVar(value="6")
    S_number = StringVar(value="0")
    gutter_number = StringVar(value=gutter)

    # determine screen size to adapt button size to screen size, right now only for hd-type or 4K displays
    screen_width = root.winfo_screenwidth()
    if screen_width < 2000:
        screen_type = "hd"
    else:
        screen_type = "4K"
    # determine page orientation to adapt layouts
    if orientation == "Portrait":
        prefix = "P-"
    elif orientation == "Landscape":
        prefix = "L-"
    else:  # orientation=square
        prefix = "S-"
    buttons_per_row = 5  # TODO think about adapting the number of buttons per row according to screen and button size
    # have to create dictionary of button images before calling the button drawing function because only way to keep the images after
    # the drawing functions ends (garbage collection of local variables)
    # used prefix for orientation and screen_type from determinations above
    button_imgs = {}
    for lkey in layouts.keys():
        button_imgs[lkey] = PhotoImage(
            file=os.path.join(
                script_path,
                "docs",
                "img",
                screen_type,
                "".join([prefix, lkey.name, ".gif"]),
            )
        )

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

    S_number_label = Label(main_frame, text="Square")
    S_number_label.grid(row=1, column=2)
    S_number_e = Entry(main_frame, textvariable=S_number)
    S_number_e.grid(row=2, column=2)

    gutter_label = Label(
        main_frame, text="".join(["Gutter (", get_unit_string(my_units), ")"])
    )
    gutter_label.grid(row=1, column=5)
    gutter_number_e = Entry(main_frame, textvariable=gutter_number)
    gutter_number_e.grid(row=2, column=5)

    do_it = Button(
        main_frame,
        text="Ok, show possible layouts",
        command=lambda: select_and_draw(
            root,
            button_imgs,
            eval(L_number_e.get()),
            eval(P_number_e.get()),
            eval(S_number_e.get()),
            eval(gutter_number_e.get()),
            layouts,
            orientation,
            buttons_per_row,
        ),
    )
    do_it.grid(row=8, column=0)

    stop_it = Button(main_frame, text="Finished, close all", command=root.destroy)
    stop_it.grid(row=8, column=2)

    root.mainloop()
    # end of Tkinter loop


def generate_icons(
    my_units, my_defaults, page, gutter, layout_name, export, exportpath
):
    orientation = sp.get_orientation(page)
    if orientation == "Portrait":
        prefix = "P-"
    elif orientation == "Landscape":
        prefix = "L-"
    else:  # orientation=square
        prefix = "S-"
    layout_selection = layouts
    # if a name is given, only this layout is used to generate a page
    if layout_name != "all":
        layout_selection = (
            l_key for l_key in layouts.keys() if (l_key.name) == layout_name
        )
    for l_key in layout_selection:
        draw_layout(layouts[l_key], page, gutter, orientation)
        # if all layouts are requested, all the layouts in layouts are generated and the page exported to a png file carrying the name of the layout
        # these files can then be converted to a GIF of smaller size using imagemagick convert and rotated to also generate landscape icons
        if layout_name == "all" or export:
            image_page = scribus.ImageExport()
            image_page.type = "PNG"
            image_path = os.path.join(exportpath, "".join([prefix, l_key.name, ".png"]))
            image_page.saveAs(image_path)
            scribus.newPage(-1)
            scribus.deletePage(1)


# def main():
# take care of Units and initialize default values
sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)
# get page information from scribus
gutter = my_defaults["gutter"]
page = sp.get_page_info()
if scribus.selectionCount() > 0:
    area_name = scribus.getSelectedObject(0)
    area = sp.get_object_info(area_name)
    if scribus.isLocked(area.name):
        scribus.lockObject(area.name)
    scribus.deleteObject(area_name)
else:
    area = sp.page_available(page)

build_main(page, area, layouts, gutter, my_units)
""" *** setup utility to generate icon files ***
- to add layouts and test them, comment the preceding line and uncomment the line after this explanation section
- to only test a single layout without writing the icon to disk, enter the layout name instead of "all" and set export to False
e.g.  layout_name="L0P1S0-1"
- to write the icons to disk enter layout_name="all", and check/change the exportpath at your convenience. 
*** Caution: if layout_name="all", the function will write to disk even if export==False
- you can also add a single icon by providing its name, setting export to True and checking the export path
- then run the script in scribus, and reverse comment/uncomment to run the normal script
- the icons should be generated in portrait mode, landscape can then be generated by rotation in imagemagick convert when generating the GIF files needed by tkinter 
"""
# generate_icons(
#     my_units,
#     my_defaults,
#     area,
#     gutter,
#     layout_name="all",
#     export=True,
#     exportpath="/home/paul/IMG-en-cours/scribus_prepare",
# )

scribus.setUnit(initial_units)


# if __name__ == "__main__":
#     main()
