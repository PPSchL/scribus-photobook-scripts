import os
import scribus
from collections import namedtuple
from script_path import script_path
import scribus_paul as sp
from scribus_paul import frame_rc, frame_fr
import scribus_acta as sa

from tkinter import *
from tkinter.ttk import *


# a layout in row/column format is defined by the number of landscape photos/frames (L), portraits (P) and squares (S).
# Squares are not perfect squares but can differ from a square by xx%.
# as some layouts can have the same number of L,P and S and still be different eg, LPS vs SPL the number n spécifies the different layouts starting from 1
# the named tuple layout_rc  will then be used as key in the dictionary of all possible layouts as a list of frame_rc frame specifications
# the chosen layout can then be drawn by recalculating the positions and sizes as a function of page and gutter (plus maybe bleed) sizes
layout_rc = namedtuple("layout_rc", ["name", "L", "P", "S", "n"])
layout_fr = namedtuple("layout_fr", ["name", "L", "P", "S", "n"])


def get_layouts(orientation):
    if orientation == "square":
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
            layout_rc(name="L2P3S0-1", L=2, P=3, S=0, n=1): [
                frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=3, ys_rc=1),
                frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
                frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
                frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
                frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=3, ys_rc=1),
            ],
            layout_fr(name="L1P1S0-1-fr", L=1, P=1, S=0, n=1): [
                frame_fr(
                    x_fr=0.0350594594,
                    y_fr=0.4786823105,
                    xs_fr=0.9567567568,
                    ys_fr=0.4259927798,
                ),
                frame_fr(
                    x_fr=0.4738162462,
                    y_fr=0.0606642599,
                    xs_fr=0.4432432432,
                    ys_fr=0.4508447653,
                ),
            ],
            layout_fr(name="L1P5S0-1-fr", L=1, P=5, S=0, n=1): [
                frame_fr(
                    x_fr=0.0945947041635934,
                    y_fr=0.3194947948115103,
                    xs_fr=0.810810591672813,
                    ys_fr=0.3610104103769795,
                ),
                frame_fr(
                    x_fr=0.05216154746384606,
                    y_fr=0.7038651223105404,
                    xs_fr=0.270270197224271,
                    ys_fr=0.2707578077827346,
                ),
                frame_fr(
                    x_fr=0.38205635319798265,
                    y_fr=0.6924030417810713,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.7081373461490654,
                    y_fr=0.7178743318465581,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.10555492642659649,
                    y_fr=0.01231959703257136,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.6089782137896718,
                    y_fr=0.040338016104606925,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
            ],
            layout_fr(name="L1P5S0-2-fr", L=1, P=5, S=0, n=2): [
                frame_fr(
                    x_fr=0.0945947041635934,
                    y_fr=0.3194947948115103,
                    xs_fr=0.810810591672813,
                    ys_fr=0.3610104103769795,
                ),
                frame_fr(
                    x_fr=0.06169607942148007,
                    y_fr=0.6643846227090359,
                    xs_fr=0.270270197224271,
                    ys_fr=0.2707578077827346,
                ),
                frame_fr(
                    x_fr=0.378242540414929,
                    y_fr=0.05689435464717341,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.567026273176082,
                    y_fr=0.6631110582057613,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.06360298581300688,
                    y_fr=0.07090356418319119,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.6947890014083777,
                    y_fr=0.084912773719209,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
            ],
            layout_fr(name="L2P1S0-1-fr", L=2, P=1, S=0, n=1): [
                frame_fr(
                    x_fr=0.25429362496568675,
                    y_fr=0.3065129972889451,
                    xs_fr=0.3783782761139794,
                    ys_fr=0.3790609308958285,
                ),
                frame_fr(
                    x_fr=0.3310510967129167,
                    y_fr=0.6924030417810714,
                    xs_fr=0.6486484733382504,
                    ys_fr=0.2888083283015836,
                ),
                frame_fr(
                    x_fr=0.029759886851682172,
                    y_fr=0.009772468026022675,
                    xs_fr=0.648648473338251,
                    ys_fr=0.2888083283015835,
                ),
            ],
            layout_fr(name="L1P2S0-2-fr", L=1, P=2, S=0, n=2): [
                frame_fr(
                    x_fr=0.6490232480117345,
                    y_fr=0.26703249768744036,
                    xs_fr=0.3243242366691252,
                    ys_fr=0.32490936933928155,
                ),
                frame_fr(
                    x_fr=0.13082592560260262,
                    y_fr=0.6045270910551417,
                    xs_fr=0.810810591672813,
                    ys_fr=0.3610104103769795,
                ),
                frame_fr(
                    x_fr=0.027852980460155385,
                    y_fr=0.07599782219628858,
                    xs_fr=0.648648473338251,
                    ys_fr=0.2888083283015835,
                ),
            ],
            layout_fr(name="L2P3S0-2-fr", L=2, P=3, S=0, n=2): [
                frame_fr(
                    x_fr=-4.800963133253884e-17,
                    y_fr=0.0,
                    xs_fr=0.6612612627221811,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=-4.800963133253884e-17,
                    y_fr=0.5174486426255928,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.3387387372778186,
                    y_fr=0.33694343743710314,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.3387387372778186,
                    y_fr=0.6738868748742062,
                    xs_fr=0.6612612627221812,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.6774774745556374,
                    y_fr=0.19253927328631137,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
            ],
            layout_fr(name="L2P3S0-3-fr", L=2, P=3, S=0, n=3): [
                frame_fr(
                    x_fr=-4.800963133253884e-17,
                    y_fr=5.816278833849359e-07,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.6526876914657891,
                    y_fr=0.025702323357372263,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=-6.006004382920949e-07,
                    y_fr=0.5415161971933526,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.3387387372778186,
                    y_fr=0.6738868748742062,
                    xs_fr=0.6612612627221812,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.18115610719504605,
                    y_fr=0.2954669647596479,
                    xs_fr=0.6612612627221811,
                    ys_fr=0.32611312512579377,
                ),
            ],
            layout_fr(name="L2P2S0-1-fr", L=2, P=2, S=0, n=1): [
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.0,
                    xs_fr=0.6612612627221811,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.4933816696857161,
                    xs_fr=0.32252252544436255,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.3387387372778186,
                    y_fr=0.6738868748742064,
                    xs_fr=0.6612612627221813,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.6774774745556374,
                    y_fr=0.1672685445599223,
                    xs_fr=0.32252252544436255,
                    ys_fr=0.3261131251257938,
                ),
            ],
            layout_fr(name="L2P2S0-2-fr", L=2, P=2, S=0, n=2): [
                frame_fr(
                    x_fr=-6.006004382896944e-07,
                    y_fr=0.13898929880907876,
                    xs_fr=0.4864863550036878,
                    ys_fr=0.21660624622618774,
                ),
                frame_fr(
                    x_fr=-6.006004382896944e-07,
                    y_fr=0.5054151561556547,
                    xs_fr=0.4918918940832719,
                    ys_fr=0.4945848438443453,
                ),
                frame_fr(
                    x_fr=0.5081081059167283,
                    y_fr=0.0,
                    xs_fr=0.4918918940832719,
                    ys_fr=0.4945848438443453,
                ),
                frame_fr(
                    x_fr=0.5144894405283794,
                    y_fr=0.6444044549647336,
                    xs_fr=0.4864863550036888,
                    ys_fr=0.21660624622618735,
                ),
            ],
            layout_fr(name="L2P4S0-1-fr", L=2, P=4, S=0, n=1): [
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.0,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.6672678610320428,
                    y_fr=0.0,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.5557559536773473,
                    y_fr=0.3369434374371032,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.3489483508014136,
                    y_fr=0.6738868748742064,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.6738868748742064,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.11151190735469516,
                    y_fr=0.33694343743710375,
                    xs_fr=0.3327321389679569,
                    ys_fr=0.32611312512579443,
                ),
            ],
            layout_fr(name="L2P4S0-2-fr", L=2, P=4, S=0, n=2): [
                frame_fr(
                    x_fr=0.04385884700511637,
                    y_fr=0.033112677085132956,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.29555497183866314,
                    y_fr=0.6458684558021708,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.6710816738150964,
                    y_fr=0.01782990304584083,
                    xs_fr=0.270270197224271,
                    ys_fr=0.27075780778273467,
                ),
                frame_fr(
                    x_fr=0.15536109247831031,
                    y_fr=0.34189691476090944,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
                frame_fr(
                    x_fr=0.6043399501116583,
                    y_fr=0.36418930760168783,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
                frame_fr(
                    x_fr=0.037988751828198504,
                    y_fr=0.6283586753950428,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
            ],
            layout_fr(name="L3P1S0-1-fr", L=3, P=1, S=0, n=1): [
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.0,
                    xs_fr=1.0,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.3369434374371032,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.6672678610320428,
                    y_fr=0.3369434374371032,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.6738868748742064,
                    xs_fr=1.0,
                    ys_fr=0.3261131251257938,
                ),
            ],
            layout_fr(name="L3P1S0-2-fr", L=3, P=1, S=0, n=2): [
                frame_fr(
                    x_fr=0.31463955460192206,
                    y_fr=0.6489667407393181,
                    xs_fr=0.6510516491985866,
                    ys_fr=0.32611312512579443,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.3369434374371032,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.2936635842951273,
                    y_fr=0.026193698638163655,
                    xs_fr=0.6510516491985866,
                    ys_fr=0.32611312512579443,
                ),
                frame_fr(
                    x_fr=0.6672678610320428,
                    y_fr=0.34458482445674926,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
            ],
            layout_fr(name="L3P2S0-1-fr", L=3, P=2, S=0, n=1): [
                frame_fr(
                    x_fr=0.6520126098998285,
                    y_fr=0.3333433614002882,
                    xs_fr=0.3243242366691252,
                    ys_fr=0.3249093693392816,
                ),
                frame_fr(
                    x_fr=0.21351359094227312,
                    y_fr=0.018051102146732372,
                    xs_fr=0.6486484733382504,
                    ys_fr=0.28880832830158365,
                ),
                frame_fr(
                    x_fr=0.40235724861215494,
                    y_fr=0.6810264707941852,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.04004503422206277,
                    y_fr=0.34225831292320924,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.0322680326536181,
                    y_fr=0.6402724066894061,
                    xs_fr=0.3243242366691246,
                    ys_fr=0.3249093693392823,
                ),
            ],
            layout_fr(name="L3P2S0-2-fr", L=3, P=2, S=0, n=2): [
                frame_fr(
                    x_fr=0.6520126098998285,
                    y_fr=0.012044096164776424,
                    xs_fr=0.3243242366691252,
                    ys_fr=0.3249093693392816,
                ),
                frame_fr(
                    x_fr=0.20270278305330214,
                    y_fr=0.34296047148601383,
                    xs_fr=0.6486484733382504,
                    ys_fr=0.28880832830158365,
                ),
                frame_fr(
                    x_fr=0.40235724861215494,
                    y_fr=0.6810264707941852,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.04004503422206277,
                    y_fr=0.03178935999900691,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.0322680326536181,
                    y_fr=0.6402724066894061,
                    xs_fr=0.3243242366691246,
                    ys_fr=0.3249093693392823,
                ),
            ],
            layout_fr(name="L4P0S0-1-fr", L=4, P=0, S=0, n=1): [
                frame_fr(
                    x_fr=0.0819542658478734,
                    y_fr=0.569442443126229,
                    xs_fr=0.8251627412376201,
                    ys_fr=0.38269301167007314,
                ),
                frame_fr(
                    x_fr=0.030210202045291196,
                    y_fr=0.2983253515937222,
                    xs_fr=0.4054052958364065,
                    ys_fr=0.18050520518848978,
                ),
                frame_fr(
                    x_fr=0.2974773970781809,
                    y_fr=0.02419830719009594,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.49388875540544136,
                    y_fr=0.3276073071020774,
                    xs_fr=0.4864863550036878,
                    ys_fr=0.21660624622618774,
                ),
            ],
            layout_fr(name="L4P0S0-1-fr", L=4, P=0, S=0, n=2): [
                frame_fr(
                    x_fr=0.37564554411982237,
                    y_fr=0.0043321249245237845,
                    xs_fr=0.4945945960555146,
                    ys_fr=0.2445848438443453,
                ),
                frame_fr(
                    x_fr=-6.006004382896944e-07,
                    y_fr=0.2532490936933929,
                    xs_fr=0.4945945960555146,
                    ys_fr=0.2445848438443453,
                ),
                frame_fr(
                    x_fr=0.4538437211833785,
                    y_fr=0.502166062462262,
                    xs_fr=0.4945945960555146,
                    ys_fr=0.2445848438443453,
                ),
                frame_fr(
                    x_fr=0.13951948181155133,
                    y_fr=0.7510830312311311,
                    xs_fr=0.4945945960555146,
                    ys_fr=0.2445848438443453,
                ),
            ],
            layout_fr(name="L4P3S0-1-fr", L=4, P=3, S=0, n=1): [
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.0,
                    xs_fr=0.6438444439392725,
                    ys_fr=0.24187726576651797,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.25270757807782734,
                    xs_fr=0.6438444439392725,
                    ys_fr=0.24187726576651797,
                ),
                frame_fr(
                    x_fr=0.6924911041315334,
                    y_fr=0.06024295468503183,
                    xs_fr=0.27027019722427104,
                    ys_fr=0.253009393753291,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.5054151561556547,
                    xs_fr=0.6438444439392725,
                    ys_fr=0.24187726576651797,
                ),
                frame_fr(
                    x_fr=0.6924911041315334,
                    y_fr=0.3734953031233547,
                    xs_fr=0.27027019722427104,
                    ys_fr=0.253009393753291,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.7581227342334821,
                    xs_fr=0.6438444439392725,
                    ys_fr=0.24187726576651797,
                ),
                frame_fr(
                    x_fr=0.6924911041315334,
                    y_fr=0.6867476515616775,
                    xs_fr=0.27027019722427104,
                    ys_fr=0.2530093937532909,
                ),
            ],
            layout_fr(name="L4P3S0-2-fr", L=4, P=3, S=0, n=2): [
                frame_fr(
                    x_fr=0.024159152629658544,
                    y_fr=0.006367822516371692,
                    xs_fr=0.4864863550036878,
                    ys_fr=0.21660624622618774,
                ),
                frame_fr(
                    x_fr=0.5927013413119501,
                    y_fr=0.04241305163919101,
                    xs_fr=0.27027019722427104,
                    ys_fr=0.27075780778273467,
                ),
                frame_fr(
                    x_fr=0.5123271888605195,
                    y_fr=0.35405093191026776,
                    xs_fr=0.4864863550036888,
                    ys_fr=0.21660624622618735,
                ),
                frame_fr(
                    x_fr=0.0012762759313369387,
                    y_fr=0.5272557043555786,
                    xs_fr=0.4864863550036888,
                    ys_fr=0.21660624622618735,
                ),
                frame_fr(
                    x_fr=0.1404804425127934,
                    y_fr=0.7570187744266165,
                    xs_fr=0.4864863550036888,
                    ys_fr=0.21660624622618735,
                ),
                frame_fr(
                    x_fr=0.11788164982177704,
                    y_fr=0.2398155496467144,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
                frame_fr(
                    x_fr=0.6613499714069152,
                    y_fr=0.6358941101650356,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
            ],
        }
    else:
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
            layout_rc(name="L2P3S0-1", L=2, P=3, S=0, n=1): [
                frame_rc(c=3, r=3, x_rc=1, y_rc=1, xs_rc=3, ys_rc=1),
                frame_rc(c=3, r=3, x_rc=1, y_rc=2, xs_rc=1, ys_rc=1),
                frame_rc(c=3, r=3, x_rc=2, y_rc=2, xs_rc=1, ys_rc=1),
                frame_rc(c=3, r=3, x_rc=3, y_rc=2, xs_rc=1, ys_rc=1),
                frame_rc(c=3, r=3, x_rc=1, y_rc=3, xs_rc=3, ys_rc=1),
            ],
            layout_fr(name="L1P1S0-1-fr", L=1, P=1, S=0, n=1): [
                frame_fr(
                    x_fr=0.0350594594,
                    y_fr=0.4786823105,
                    xs_fr=0.9567567568,
                    ys_fr=0.4259927798,
                ),
                frame_fr(
                    x_fr=0.4738162462,
                    y_fr=0.0606642599,
                    xs_fr=0.4432432432,
                    ys_fr=0.4508447653,
                ),
            ],
            layout_fr(name="L1P5S0-1-fr", L=1, P=5, S=0, n=1): [
                frame_fr(
                    x_fr=0.0945947041635934,
                    y_fr=0.3194947948115103,
                    xs_fr=0.810810591672813,
                    ys_fr=0.3610104103769795,
                ),
                frame_fr(
                    x_fr=0.05216154746384606,
                    y_fr=0.7038651223105404,
                    xs_fr=0.270270197224271,
                    ys_fr=0.2707578077827346,
                ),
                frame_fr(
                    x_fr=0.38205635319798265,
                    y_fr=0.6924030417810713,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.7081373461490654,
                    y_fr=0.7178743318465581,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.10555492642659649,
                    y_fr=0.01231959703257136,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.6089782137896718,
                    y_fr=0.040338016104606925,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
            ],
            layout_fr(name="L1P5S0-2-fr", L=1, P=5, S=0, n=2): [
                frame_fr(
                    x_fr=0.0945947041635934,
                    y_fr=0.3194947948115103,
                    xs_fr=0.810810591672813,
                    ys_fr=0.3610104103769795,
                ),
                frame_fr(
                    x_fr=0.06169607942148007,
                    y_fr=0.6643846227090359,
                    xs_fr=0.270270197224271,
                    ys_fr=0.2707578077827346,
                ),
                frame_fr(
                    x_fr=0.378242540414929,
                    y_fr=0.05689435464717341,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.567026273176082,
                    y_fr=0.6631110582057613,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.06360298581300688,
                    y_fr=0.07090356418319119,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
                frame_fr(
                    x_fr=0.6947890014083777,
                    y_fr=0.084912773719209,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827341,
                ),
            ],
            layout_fr(name="L2P1S0-1-fr", L=2, P=1, S=0, n=1): [
                frame_fr(
                    x_fr=0.25429362496568675,
                    y_fr=0.3065129972889451,
                    xs_fr=0.3783782761139794,
                    ys_fr=0.3790609308958285,
                ),
                frame_fr(
                    x_fr=0.3310510967129167,
                    y_fr=0.6924030417810714,
                    xs_fr=0.6486484733382504,
                    ys_fr=0.2888083283015836,
                ),
                frame_fr(
                    x_fr=0.029759886851682172,
                    y_fr=0.009772468026022675,
                    xs_fr=0.648648473338251,
                    ys_fr=0.2888083283015835,
                ),
            ],
            layout_fr(name="L1P2S0-2-fr", L=1, P=2, S=0, n=2): [
                frame_fr(
                    x_fr=0.6490232480117345,
                    y_fr=0.26703249768744036,
                    xs_fr=0.3243242366691252,
                    ys_fr=0.32490936933928155,
                ),
                frame_fr(
                    x_fr=0.13082592560260262,
                    y_fr=0.6045270910551417,
                    xs_fr=0.810810591672813,
                    ys_fr=0.3610104103769795,
                ),
                frame_fr(
                    x_fr=0.027852980460155385,
                    y_fr=0.07599782219628858,
                    xs_fr=0.648648473338251,
                    ys_fr=0.2888083283015835,
                ),
            ],
            layout_fr(name="L2P3S0-2-fr", L=2, P=3, S=0, n=2): [
                frame_fr(
                    x_fr=-4.800963133253884e-17,
                    y_fr=0.0,
                    xs_fr=0.6612612627221811,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=-4.800963133253884e-17,
                    y_fr=0.5174486426255928,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.3387387372778186,
                    y_fr=0.33694343743710314,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.3387387372778186,
                    y_fr=0.6738868748742062,
                    xs_fr=0.6612612627221812,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.6774774745556374,
                    y_fr=0.19253927328631137,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
            ],
            layout_fr(name="L2P3S0-3-fr", L=2, P=3, S=0, n=3): [
                frame_fr(
                    x_fr=-4.800963133253884e-17,
                    y_fr=5.816278833849359e-07,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.6526876914657891,
                    y_fr=0.025702323357372263,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=-6.006004382920949e-07,
                    y_fr=0.5415161971933526,
                    xs_fr=0.3225225254443625,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.3387387372778186,
                    y_fr=0.6738868748742062,
                    xs_fr=0.6612612627221812,
                    ys_fr=0.32611312512579377,
                ),
                frame_fr(
                    x_fr=0.18115610719504605,
                    y_fr=0.2954669647596479,
                    xs_fr=0.6612612627221811,
                    ys_fr=0.32611312512579377,
                ),
            ],
            layout_fr(name="L2P2S0-1-fr", L=2, P=2, S=0, n=1): [
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.0,
                    xs_fr=0.6612612627221811,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.4933816696857161,
                    xs_fr=0.32252252544436255,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.3387387372778186,
                    y_fr=0.6738868748742064,
                    xs_fr=0.6612612627221813,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.6774774745556374,
                    y_fr=0.1672685445599223,
                    xs_fr=0.32252252544436255,
                    ys_fr=0.3261131251257938,
                ),
            ],
            layout_fr(name="L2P2S0-2-fr", L=2, P=2, S=0, n=2): [
                frame_fr(
                    x_fr=-6.006004382896944e-07,
                    y_fr=0.13898929880907876,
                    xs_fr=0.4864863550036878,
                    ys_fr=0.21660624622618774,
                ),
                frame_fr(
                    x_fr=-6.006004382896944e-07,
                    y_fr=0.5054151561556547,
                    xs_fr=0.4918918940832719,
                    ys_fr=0.4945848438443453,
                ),
                frame_fr(
                    x_fr=0.5081081059167283,
                    y_fr=0.0,
                    xs_fr=0.4918918940832719,
                    ys_fr=0.4945848438443453,
                ),
                frame_fr(
                    x_fr=0.5144894405283794,
                    y_fr=0.6444044549647336,
                    xs_fr=0.4864863550036888,
                    ys_fr=0.21660624622618735,
                ),
            ],
            layout_fr(name="L2P4S0-1-fr", L=2, P=4, S=0, n=1): [
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.0,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.6672678610320428,
                    y_fr=0.0,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.5557559536773473,
                    y_fr=0.3369434374371032,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.3489483508014136,
                    y_fr=0.6738868748742064,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.6738868748742064,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.11151190735469516,
                    y_fr=0.33694343743710375,
                    xs_fr=0.3327321389679569,
                    ys_fr=0.32611312512579443,
                ),
            ],
            layout_fr(name="L2P4S0-2-fr", L=2, P=4, S=0, n=2): [
                frame_fr(
                    x_fr=0.04385884700511637,
                    y_fr=0.033112677085132956,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.29555497183866314,
                    y_fr=0.6458684558021708,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.6710816738150964,
                    y_fr=0.01782990304584083,
                    xs_fr=0.270270197224271,
                    ys_fr=0.27075780778273467,
                ),
                frame_fr(
                    x_fr=0.15536109247831031,
                    y_fr=0.34189691476090944,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
                frame_fr(
                    x_fr=0.6043399501116583,
                    y_fr=0.36418930760168783,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
                frame_fr(
                    x_fr=0.037988751828198504,
                    y_fr=0.6283586753950428,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
            ],
            layout_fr(name="L3P1S0-1-fr", L=3, P=1, S=0, n=1): [
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.0,
                    xs_fr=1.0,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.3369434374371032,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.6672678610320428,
                    y_fr=0.3369434374371032,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.6738868748742064,
                    xs_fr=1.0,
                    ys_fr=0.3261131251257938,
                ),
            ],
            layout_fr(name="L3P1S0-2-fr", L=3, P=1, S=0, n=2): [
                frame_fr(
                    x_fr=0.31463955460192206,
                    y_fr=0.6489667407393181,
                    xs_fr=0.6510516491985866,
                    ys_fr=0.32611312512579443,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.3369434374371032,
                    xs_fr=0.6510516491985864,
                    ys_fr=0.3261131251257938,
                ),
                frame_fr(
                    x_fr=0.2936635842951273,
                    y_fr=0.026193698638163655,
                    xs_fr=0.6510516491985866,
                    ys_fr=0.32611312512579443,
                ),
                frame_fr(
                    x_fr=0.6672678610320428,
                    y_fr=0.34458482445674926,
                    xs_fr=0.3327321389679573,
                    ys_fr=0.3261131251257938,
                ),
            ],
            layout_fr(name="L3P2S0-1-fr", L=3, P=2, S=0, n=1): [
                frame_fr(
                    x_fr=0.6520126098998285,
                    y_fr=0.3333433614002882,
                    xs_fr=0.3243242366691252,
                    ys_fr=0.3249093693392816,
                ),
                frame_fr(
                    x_fr=0.21351359094227312,
                    y_fr=0.018051102146732372,
                    xs_fr=0.6486484733382504,
                    ys_fr=0.28880832830158365,
                ),
                frame_fr(
                    x_fr=0.40235724861215494,
                    y_fr=0.6810264707941852,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.04004503422206277,
                    y_fr=0.34225831292320924,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.0322680326536181,
                    y_fr=0.6402724066894061,
                    xs_fr=0.3243242366691246,
                    ys_fr=0.3249093693392823,
                ),
            ],
            layout_fr(name="L3P2S0-2-fr", L=3, P=2, S=0, n=2): [
                frame_fr(
                    x_fr=0.6520126098998285,
                    y_fr=0.012044096164776424,
                    xs_fr=0.3243242366691252,
                    ys_fr=0.3249093693392816,
                ),
                frame_fr(
                    x_fr=0.20270278305330214,
                    y_fr=0.34296047148601383,
                    xs_fr=0.6486484733382504,
                    ys_fr=0.28880832830158365,
                ),
                frame_fr(
                    x_fr=0.40235724861215494,
                    y_fr=0.6810264707941852,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.04004503422206277,
                    y_fr=0.03178935999900691,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.0322680326536181,
                    y_fr=0.6402724066894061,
                    xs_fr=0.3243242366691246,
                    ys_fr=0.3249093693392823,
                ),
            ],
            layout_fr(name="L4P0S0-1-fr", L=4, P=0, S=0, n=1): [
                frame_fr(
                    x_fr=0.0819542658478734,
                    y_fr=0.569442443126229,
                    xs_fr=0.8251627412376201,
                    ys_fr=0.38269301167007314,
                ),
                frame_fr(
                    x_fr=0.030210202045291196,
                    y_fr=0.2983253515937222,
                    xs_fr=0.4054052958364065,
                    ys_fr=0.18050520518848978,
                ),
                frame_fr(
                    x_fr=0.2974773970781809,
                    y_fr=0.02419830719009594,
                    xs_fr=0.5675674141709699,
                    ys_fr=0.2527072872638861,
                ),
                frame_fr(
                    x_fr=0.49388875540544136,
                    y_fr=0.3276073071020774,
                    xs_fr=0.4864863550036878,
                    ys_fr=0.21660624622618774,
                ),
            ],
            layout_fr(name="L4P0S0-1-fr", L=4, P=0, S=0, n=2): [
                frame_fr(
                    x_fr=0.37564554411982237,
                    y_fr=0.0043321249245237845,
                    xs_fr=0.4945945960555146,
                    ys_fr=0.2445848438443453,
                ),
                frame_fr(
                    x_fr=-6.006004382896944e-07,
                    y_fr=0.2532490936933929,
                    xs_fr=0.4945945960555146,
                    ys_fr=0.2445848438443453,
                ),
                frame_fr(
                    x_fr=0.4538437211833785,
                    y_fr=0.502166062462262,
                    xs_fr=0.4945945960555146,
                    ys_fr=0.2445848438443453,
                ),
                frame_fr(
                    x_fr=0.13951948181155133,
                    y_fr=0.7510830312311311,
                    xs_fr=0.4945945960555146,
                    ys_fr=0.2445848438443453,
                ),
            ],
            layout_fr(name="L4P3S0-1-fr", L=4, P=3, S=0, n=1): [
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.0,
                    xs_fr=0.6438444439392725,
                    ys_fr=0.24187726576651797,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.25270757807782734,
                    xs_fr=0.6438444439392725,
                    ys_fr=0.24187726576651797,
                ),
                frame_fr(
                    x_fr=0.6924911041315334,
                    y_fr=0.06024295468503183,
                    xs_fr=0.27027019722427104,
                    ys_fr=0.253009393753291,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.5054151561556547,
                    xs_fr=0.6438444439392725,
                    ys_fr=0.24187726576651797,
                ),
                frame_fr(
                    x_fr=0.6924911041315334,
                    y_fr=0.3734953031233547,
                    xs_fr=0.27027019722427104,
                    ys_fr=0.253009393753291,
                ),
                frame_fr(
                    x_fr=-3.840770506603107e-17,
                    y_fr=0.7581227342334821,
                    xs_fr=0.6438444439392725,
                    ys_fr=0.24187726576651797,
                ),
                frame_fr(
                    x_fr=0.6924911041315334,
                    y_fr=0.6867476515616775,
                    xs_fr=0.27027019722427104,
                    ys_fr=0.2530093937532909,
                ),
            ],
            layout_fr(name="L4P3S0-2-fr", L=4, P=3, S=0, n=2): [
                frame_fr(
                    x_fr=0.024159152629658544,
                    y_fr=0.006367822516371692,
                    xs_fr=0.4864863550036878,
                    ys_fr=0.21660624622618774,
                ),
                frame_fr(
                    x_fr=0.5927013413119501,
                    y_fr=0.04241305163919101,
                    xs_fr=0.27027019722427104,
                    ys_fr=0.27075780778273467,
                ),
                frame_fr(
                    x_fr=0.5123271888605195,
                    y_fr=0.35405093191026776,
                    xs_fr=0.4864863550036888,
                    ys_fr=0.21660624622618735,
                ),
                frame_fr(
                    x_fr=0.0012762759313369387,
                    y_fr=0.5272557043555786,
                    xs_fr=0.4864863550036888,
                    ys_fr=0.21660624622618735,
                ),
                frame_fr(
                    x_fr=0.1404804425127934,
                    y_fr=0.7570187744266165,
                    xs_fr=0.4864863550036888,
                    ys_fr=0.21660624622618735,
                ),
                frame_fr(
                    x_fr=0.11788164982177704,
                    y_fr=0.2398155496467144,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
                frame_fr(
                    x_fr=0.6613499714069152,
                    y_fr=0.6358941101650356,
                    xs_fr=0.2702701972242711,
                    ys_fr=0.2707578077827342,
                ),
            ],
        }
    return layouts


def draw_layout(lkey, layout, area, gutter, orientation, tkwindow="none"):
    if isinstance(lkey, layout_rc):
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
                frame_draw = frame_i
            sp.create_image(*sp.rc2xy(frame_draw, area, gutter))
    else:  # layout is of type fr
        for frame_i in layout:
            if orientation == "Landscape":
                frame_draw = frame_fr(
                    x_fr=frame_i.y_fr,
                    y_fr=1 - (frame_i.x_fr + frame_i.xs_fr),
                    xs_fr=frame_i.ys_fr,
                    ys_fr=frame_i.xs_fr,
                )
            elif orientation == "Portrait":
                frame_draw = frame_i
            else:
                frame_draw = frame_i
            sp.create_image(*sp.fr2xy(frame_draw, area))
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


def use_bleed(choice):
    if choice:
        return sp.page_with_bleed(page, bleed)
    else:
        return area


def select_and_draw(
    root, button_imgs, L, P, S, area, gutter, layouts, orientation, buttons_per_row
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
                    lkey, layouts[lkey], area, gutter, orientation, root
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
        ok_layouts = filter_layouts(
            L, P, S, layouts
        )  # TODO may have to create a specific layout dict for square pages
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


def draw_acta(root_win, page, linevar, Acta_button_imgs):
    def draw1(root_win, page, linevar, line_n):
        group_type = linevar[line_n - 1].get()
        path_to_base, n_groups, gutter, top_group, below_groups, g_pos = (
            sa.set_acta_data(group_type, page, script_path)
        )

        sa.draw_1_group(
            group_type,
            page,
            path_to_base,
            n_groups,
            line_n,
            gutter,
            top_group,
            below_groups,
            g_pos,
        )
        scribus.deselectAll()
        root_win.destroy()
        return

    def draw3(root_win, page, linevar):
        for group_n in range(1, 4):
            group_type = linevar[group_n - 1].get()
            path_to_base, n_groups, gutter, top_group, below_groups, g_pos = (
                sa.set_acta_data(group_type, page, script_path)
            )

            sa.draw_1_group(
                group_type,
                page,
                path_to_base,
                n_groups,
                group_n,
                gutter,
                top_group,
                below_groups,
                g_pos,
            )
        scribus.deselectAll()
        root_win.destroy()
        return

    def draw2(root_win, page, linevar, pos):
        # pos= tuple with: first= double position, second= single position
        # draw double at position given by pos[0]
        group_type = "double"
        path_to_base, n_groups, gutter, top_group, below_groups, g_pos = (
            sa.set_acta_data(group_type, page, script_path)
        )

        sa.draw_1_group(
            "double",
            page,
            path_to_base,
            n_groups,
            pos[0],
            gutter,
            top_group,
            below_groups,
            g_pos,
        )
        group_type = linevar[
            pos[1] - 1
        ].get()  # linevar from 0 to 2, position from 1 to 3
        path_to_base, n_groups, gutter, top_group, below_groups, g_pos = (
            sa.set_acta_data(group_type, page, script_path)
        )

        sa.draw_1_group(
            group_type,
            page,
            path_to_base,
            n_groups,
            pos[1],
            gutter,
            top_group,
            below_groups,
            g_pos,
        )
        scribus.deselectAll()
        root_win.destroy()
        return

    def drawfull(root_win, page):
        group_type = "whole_page"
        path_to_base, n_groups, gutter, top_group, below_groups, g_pos = (
            sa.set_acta_data(group_type, page, script_path)
        )

        sa.draw_1_group(
            "whole_page",
            page,
            path_to_base,
            n_groups,
            1,  # group_n=1 for whole page
            gutter,
            top_group,
            below_groups,
            g_pos,
        )
        scribus.deselectAll()
        root_win.destroy()
        return

    w_acta = Toplevel(
        root_win,
    )
    w_acta.title("Build diary page")
    x0 = root_win.winfo_x()
    y0 = root_win.winfo_y()
    w_acta.geometry("+%d+%d" % (x0 + 20, y0 + 150))

    quick_draw_title = Label(w_acta, text="Quick selection", style="Title.TLabel")
    quick_draw_title.grid(row=0, column=0, columnspan=3)

    draw_3 = Button(
        w_acta,
        text="Draw standard page",
        image=Acta_button_imgs["Acta_normal"],
        compound=BOTTOM,
        command=lambda: draw3(root_win, page, linevar),
    )
    draw_3.grid(row=1, column=0, rowspan=3)

    draw_2_top = Button(
        w_acta,
        text="Draw double (top)",
        image=Acta_button_imgs["Acta_double_top"],
        compound=BOTTOM,
        command=lambda: draw2(root_win, page, linevar, (1, 3)),
    )
    draw_2_top.grid(row=1, column=1, rowspan=3)

    draw_2_bottom = Button(
        w_acta,
        text="Draw double (bottom)",
        image=Acta_button_imgs["Acta_double_bottom"],
        compound=BOTTOM,
        command=lambda: draw2(root_win, page, linevar, (2, 1)),
    )
    draw_2_bottom.grid(row=1, column=2, rowspan=3)

    draw_full = Button(
        w_acta,
        text="Draw full page",
        image=Acta_button_imgs["Acta_full_page"],
        compound=BOTTOM,
        command=lambda: drawfull(root_win, page),
    )
    draw_full.grid(row=1, column=3, rowspan=3)

    line_title = Label(w_acta, text="Customize lines", style="Title.TLabel")
    line_title.grid(row=0, column=4)

    line1 = Combobox(
        w_acta,
        text="line 1",
        textvariable=linevar[0],
        state="readonly",
        values=("normal", "central"),
    )
    line1.grid(row=1, column=4)
    line2 = Combobox(
        w_acta,
        textvariable=linevar[1],
        state="readonly",
        values=("normal", "central"),
    )
    line2.grid(row=2, column=4)

    line3 = Combobox(
        w_acta,
        textvariable=linevar[2],
        state="readonly",
        values=("normal", "central"),
    )
    line3.grid(row=3, column=4)

    line_do_title = Label(w_acta, text="Draw specific line", style="Title.TLabel")
    line_do_title.grid(row=0, column=5)
    line1do = Button(
        w_acta, text="draw", command=lambda: draw1(root_win, page, linevar, 1)
    )
    line1do.grid(row=1, column=5)
    line2do = Button(
        w_acta, text="draw", command=lambda: draw1(root_win, page, linevar, 2)
    )
    line2do.grid(row=2, column=5)
    line3do = Button(
        w_acta, text="draw", command=lambda: draw1(root_win, page, linevar, 3)
    )
    line3do.grid(row=3, column=5)


def build_main(page, area, gutter, bleed, my_units):
    orientation = sp.get_orientation(area)
    layouts = get_layouts(orientation)
    # *** tkinter loop
    root = Tk()
    style = Style()
    style.theme_use("classic")
    style.configure("Title.TLabel", font=("Sans", "10", "bold"), foreground="#202020")

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
    bleed_onoff = BooleanVar(value=False)
    # have to define line variables for acta here to avoid them being garbage collected outside of draw_acta function
    linevar = []
    for line_n in range(3):
        linevar.append(StringVar(value="normal"))

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
    Acta_button_imgs = {}
    for img_name in (
        "Acta_normal",
        "Acta_double_top",
        "Acta_double_bottom",
        "Acta_full_page",
    ):
        Acta_button_imgs[img_name] = PhotoImage(
            file=os.path.join(
                script_path,
                "docs",
                "img",
                screen_type,
                "".join([img_name, ".gif"]),
            )
        )

    explication = Label(
        main_frame,
        text="Choose layout for a number of Landscape, Portrait and Square photographs",
        style="Title.TLabel",
    )
    explication.grid(row=0, column=0, columnspan=3, pady=10)

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

    do_it = Button(
        main_frame,
        text="Show possible layouts",
        command=lambda: select_and_draw(
            root,
            button_imgs,
            eval(L_number_e.get()),
            eval(P_number_e.get()),
            eval(S_number_e.get()),
            use_bleed(bleed_onoff.get()),
            eval(gutter_number_e.get()),
            layouts,
            orientation,
            buttons_per_row,
        ),
    )
    do_it.grid(row=8, column=0)

    stop_it = Button(main_frame, text="Finished, close all", command=root.destroy)
    stop_it.grid(row=8, column=2)

    specs_frame = Frame(root, padding="30 2 30 4")
    specs_frame.grid(column=1, row=0, sticky=(N, W, E, S))
    # specs_frame.rowconfigure(0, weight=1)
    parameter_label = Label(
        specs_frame, text="Additional parameters", style="Title.TLabel"
    )

    parameter_label.grid(row=0, column=0, pady=10)

    gutter_label = Label(
        specs_frame, text="".join(["Gutter (", sp.get_unit_string(my_units), ")"])
    )
    gutter_label.grid(row=1, column=0)
    gutter_number_e = Entry(specs_frame, textvariable=gutter_number)
    gutter_number_e.grid(row=2, column=0)

    bleed_or_not = Checkbutton(
        specs_frame,
        text="Draw into bleed",
        variable=bleed_onoff,
        offvalue=False,
        onvalue=True,
    )
    bleed_or_not.grid(row=3, column=0, pady=10)

    acta_frame = Frame(root, padding="2 2 4 4")
    acta_frame.grid(column=2, row=0, sticky=(N, W, E, S))
    acta_show = Button(
        acta_frame,
        text="Build diary page",
        image=Acta_button_imgs["Acta_normal"],
        compound=BOTTOM,
        style="Title.TLabel",
        command=lambda: draw_acta(root, page, linevar, Acta_button_imgs),
    )
    acta_show.grid(row=0, column=0)

    root.mainloop()
    # end of Tkinter loop


def generate_icons(
    my_units, my_defaults, page, gutter, layout_test, export, exportpath
):
    orientation = sp.get_orientation(page)
    layouts = get_layouts(orientation)
    if orientation == "Portrait":
        prefix = "P-"
    elif orientation == "Landscape":
        prefix = "L-"
    else:  # orientation=square
        prefix = "S-"
    layout_selection = layouts
    # if a name is given, only this layout is used to generate a page
    if layout_test != "all":
        layout_selection = (
            l_key
            for l_key in layouts.keys()
            if eval(layout_test)  # (l_key.name) == layout_name
        )
    for l_key in layout_selection:
        draw_layout(l_key, layouts[l_key], page, gutter, orientation)
        # if all layouts are requested, all the layouts in layouts are generated and the page exported to a png file carrying the name of the layout
        # these files can then be converted to a GIF of smaller size using imagemagick convert and rotated to also generate landscape icons
        if layout_test == "all" or export:
            image_page = scribus.ImageExport()
            image_page.type = "PNG"
            image_path = os.path.join(exportpath, "".join([prefix, l_key.name, ".png"]))
            image_page.saveAs(image_path)
            scribus.newPage(-1)
            scribus.deletePage(1)


def generate_fr_coordinates():
    # generates fractional coordinates from a page of frames prepared manually
    # within scribus select all frames in your preferred order before calling this script
    p = page  # gives acces to margins
    pa = sp.page_available(page)  # defines available page size (margins removed)
    dict_entry = ["""layout_fr(name="L0P0S0-1-fr", L=0, P=0, S=0, n=1): [\n"""]
    for frame_n in range(scribus.selectionCount()):
        name_n = scribus.getSelectedObject(
            frame_n
        )  # coorfinates are absolute, do not take into account margins
        i = sp.get_object_info(name_n)
        dict_entry.append(
            "frame_fr(x_fr="
            + str((i.x - p.mleft) / pa.xs)
            + ",y_fr="
            + str((i.y - p.mtop) / pa.ys)
            + ",xs_fr="
            + str(i.xs / pa.xs)
            + ",ys_fr="
            + str(i.ys / pa.ys)
            + "),\n"
        )
    dict_entry.append("],")
    scribus.messageBox(
        "Fractional coordinates of page items\nCopy and paste into program file",
        "".join(dict_entry),
        scribus.BUTTON_OK,
    )
    sys.exit(1)


# def main():
# take care of Units and initialize default values
sp.check_doc_present()
my_lang, my_msg, my_units, my_defaults = sp.get_config_data(script_path)
initial_units = scribus.getUnit()
scribus.setUnit(my_units)
# get page information from scribus
gutter = my_defaults["gutter"]
bleed = my_defaults["bleed"]
page = sp.get_page_info()
""" *** utility to generate fractional coordinates for the layout dictionary from manually designed scribus page ***
uncomment the line after this explanation section
"""
# generate_fr_coordinates()

if scribus.selectionCount() > 0:
    area_name = scribus.getSelectedObject(0)
    area = sp.get_object_info(area_name)
    if scribus.isLocked(area.name):
        scribus.lockObject(area.name)
    scribus.deleteObject(area_name)
else:
    area = sp.page_available(page)

build_main(page, area, gutter, bleed, my_units)
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
#     layout_test="""((l_key.name) == "L2P3S0-1")""",
#     # eg """"fr" in l_key.name """ or """((l_key.name) == "layout_name")"""
#     export=True,
#     exportpath="/home/paul/IMG-en-cours/scribus_prepare",
# )

scribus.setUnit(initial_units)


# if __name__ == "__main__":
#     main()
