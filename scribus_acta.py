import scribus
import scribus_paul as sp


def set_g_pos_moisjour(page, g_pos):
    def invert4rightpage(label, g_pos, page):
        # use previously defined identation vs left margin to calulate identation for right page  for "mois" or "jour" labels
        # right margin position relative to topleft corner=page size-right margin-left margin
        # label relative position=right margin position - label size- label identation used on left page
        g_pos[label].update(
            {
                "dx": page.xs
                - page.mright
                - page.mleft
                - g_pos[label]["xs"]
                - g_pos[label]["dx"],
                "dy": g_pos[label]["dy"],
            }
        )
        return g_pos

    g_pos["Acta_jour"] = {"xs": 12.5, "ys": 8.0}
    g_pos["Acta_mois"] = {"xs": 35.0, "ys": 8.0}

    # left page
    g_pos["Acta_jour"].update({"dx": 1.0, "dy": 0.5})
    g_pos["Acta_mois"].update({"dx": 16.0, "dy": -4.0})
    if page.page_type != 0:  # right page:
        # identation identical to left page, but negative vs right margin=> use data from left margin for calculation
        g_pos = invert4rightpage("Acta_jour", g_pos, page)
        g_pos = invert4rightpage("Acta_mois", g_pos, page)
    return g_pos


def set_g_pos_variable(group_type, g_pos, page, n_groups, gutter):
    if group_type == "normal":
        g_pos["Acta_txt"] = {"xs": 55.0}  # width of text frame determined here
        # image size= page available width - text width
        g_pos["Acta_img"] = {
            "xs": page.xs - page.mleft - page.mright - g_pos["Acta_txt"]["xs"]
        }
        # image and text height are identical and determnined by number of groups and gutter
        g_pos["Acta_img"]["ys"] = sp.pict_size1D(
            n_groups, page.mtop, page.mbottom, gutter, page.ys
        )
        g_pos["Acta_txt"]["ys"] = g_pos["Acta_img"]["ys"]
        # calculate text and image position relative to topleft corner coordinates
        if page.page_type == 0:  # left page
            # text is at the topleft corner, image is shifted to the right by the text-frame width
            g_pos["Acta_txt"].update({"dx": 0.0, "dy": 0.0})
            # image is at same y but shifted to the right by the text-frame width
            g_pos["Acta_img"].update({"dx": g_pos["Acta_txt"]["xs"], "dy": 0.0})
        else:  # right page
            # image is at the topleft corner, text is shifted by the image width
            g_pos["Acta_txt"].update({"dx": g_pos["Acta_img"]["xs"], "dy": 0.0})
            g_pos["Acta_img"].update({"dx": 0.0, "dy": 0.0})
    else:  # group_type=="central" or group_type=="double" or group_type=="whole page":
        # image and text frames take the whole available width of the page
        g_pos["Acta_txt"] = {"xs": page.xs - page.mleft - page.mright}
        g_pos["Acta_img"] = {"xs": g_pos["Acta_txt"]["xs"]}
        # text height set to 20 mm as sufficient for 3 lines
        if group_type == "central":
            g_pos["Acta_txt"]["ys"] = 20.0
            # image height determined by group height (number of groups and gutter)- text height determined above
            g_pos["Acta_img"]["ys"] = (
                sp.pict_size1D(n_groups, page.mtop, page.mbottom, gutter, page.ys)
                - g_pos["Acta_txt"]["ys"]
            )
        elif group_type == "double":
            # increase text heigh to 4 lines
            g_pos["Acta_txt"]["ys"] = 27.0
            # image height equals twice the group height (from number of groups and gutter) + gutter- text height determined above
            g_pos["Acta_img"]["ys"] = (
                2 * sp.pict_size1D(n_groups, page.mtop, page.mbottom, gutter, page.ys)
                + gutter
                - g_pos["Acta_txt"]["ys"]
            )
        else:  # group_type=="whole_page"
            # increase text heigh to 4 lines
            g_pos["Acta_txt"]["ys"] = 27.0
            # image height equals whole available page size-text height determined above
            g_pos["Acta_img"]["ys"] = (
                page.ys - page.mtop - page.mbottom - g_pos["Acta_txt"]["ys"]
            )
        # calculate text and image position relative to topleft corner coordinates
        # as the group is central, distances to topleft corner are identical for left anf right pages
        # text frame starts at topleft corner
        g_pos["Acta_txt"].update({"dx": 0.0, "dy": 0.0})
        # image frame is at left margin, shifted to the bottom by text height
        g_pos["Acta_img"].update({"dx": 0.0, "dy": g_pos["Acta_txt"]["ys"]})
    return g_pos


def set_acta_data(group_type, page):
    # *** define page layout decisions here ***
    # text frame x size (width) is considered constant, text frame height (y size) and image size will be adapted
    path_to_base = "/home/paul/Documents/dessins-présentations/Scribus/Models2edit/Annales_base.sla"
    n_groups = (
        3  # number of "days" on each page, 3 (top, middle, bottom) not likely to change
    )
    gutter = 3.0
    top_group = ["Acta_jour", "Acta_mois", "Acta_txt", "Acta_img"]
    below_groups = ["Acta_jour", "Acta_txt", "Acta_img"]
    g_pos = {}  # dictionary of group elements, which are themselves dictionaries of sizes and relative positions vs topleft
    # dictionaries used because mutable
    set_g_pos_moisjour(page, g_pos)  # identical for all group_types
    set_g_pos_variable(group_type, g_pos, page, n_groups, gutter)
    return (path_to_base, n_groups, gutter, top_group, below_groups, g_pos)


def copy_group(path_to_base, group_n, top_group, below_groups):
    if group_n == 1:
        group = top_group
    else:
        group = below_groups
    scribus.openDoc(path_to_base)
    scribus.copyObjects(group)
    scribus.closeDoc()


def paste_and_resize_group(
    group_type, page, n_groups, group_n, g_pos, top_group, gutter
):
    # calculate x_topleft and y_topleft according to number of group
    # x of topleft is always at the left margin
    x_topleft = page.mleft
    # y of topleft depends on the position of the group (group_n),the top margin and the gutter, as well as
    # the group y size calculated from the number of groups (n_groups), the margins, gutter and page size
    y_topleft = sp.pict_pos1D(
        group_n,
        page.mtop,
        sp.pict_size1D(n_groups, page.mtop, page.mbottom, gutter, page.ys),
        gutter,
    )

    # paste objects and then for each element according to its name (find method!) change its size and position
    current_g = scribus.pasteObjects()
    # iterate through pasted objects using their names in elem
    for elem in current_g:
        # iterate through element names ("Acta_jour", "Acta_mois", etc) to apply move and size
        for elem_g in top_group:
            if elem.find(elem_g) != -1:
                scribus.moveObjectAbs(
                    x_topleft + g_pos[elem_g]["dx"],
                    y_topleft + g_pos[elem_g]["dy"],
                    elem,
                )
                scribus.sizeObject(g_pos[elem_g]["xs"], g_pos[elem_g]["ys"], elem)
                scribus.lockObject(elem)
    # in an additional step, split image if group_type different from normal
    if group_type != "normal":
        gutter = 0.5
        if group_type == "central":
            x_n_picts = 3
            y_n_picts = 1
        elif group_type == "double":
            x_n_picts = 3
            y_n_picts = 2
        else:  # group_type="whole_page"
            x_n_picts = 3
            y_n_picts = 3
        for elem in current_g:
            if elem.find("Acta_img") != -1:
                elem_obj = sp.set_object_info(
                    elem,
                    x_topleft + g_pos["Acta_img"]["dx"],
                    y_topleft + g_pos["Acta_img"]["dy"],
                    g_pos["Acta_img"]["xs"],
                    g_pos["Acta_img"]["ys"],
                    0,
                    0,
                    0,
                    0,
                    0,
                )
                sp.split_image("resize", elem_obj, x_n_picts, y_n_picts, gutter)


def draw_1_group(
    group_type,
    page,
    path_to_base,
    n_groups,
    group_n,
    gutter,
    top_group,
    below_groups,
    g_pos,
):
    copy_group(path_to_base, group_n, top_group, below_groups)
    paste_and_resize_group(
        group_type, page, n_groups, group_n, g_pos, top_group, gutter
    )


def draw_normal_page(
    page, path_to_base, n_groups, gutter, top_group, below_groups, g_pos
):
    for group_n in range(1, n_groups + 1):
        draw_1_group(
            "normal",
            page,
            path_to_base,
            n_groups,
            group_n,
            gutter,
            top_group,
            below_groups,
            g_pos,
        )
