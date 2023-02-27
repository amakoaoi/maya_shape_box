from maya import cmds


def change_color(hex_color):
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:], 16) / 255.0

    selection = cmds.ls(selection=True)
    shapes = cmds.listRelatives(selection, shapes=True)

    for shape in shapes:
        cmds.setAttr(shape + ".overrideEnabled", True)
        cmds.setAttr(shape + ".overrideRGBColors", True)
        cmds.setAttr(shape + ".overrideColorRGB", r, g, b)


def change_shape(shape_name):
    selection = cmds.ls(selection=True)
    shapes = cmds.listRelatives(selection, shapes=True)
    for shape in shapes:
        override_enabled = cmds.getAttr(shape + ".overrideEnabled")
        override_rgb_colors = cmds.getAttr(shape + ".overrideRGBColors")
        override_color_rgb = cmds.getAttr(shape + ".overrideColorRGB")
        parent = cmds.listRelatives(shape, parent=True)[0]
        cmds.delete(shape)

        new_nurbs = None

        if shape_name == "circle":
            new_nurbs = circle_shape()
        elif shape_name == "square":
            new_nurbs = square_shape()
        elif shape_name == "locator":
            new_nurbs = loc_shape()
        elif shape_name == "crossed_arrow":
            new_nurbs = crossed_arrow_shape()
        elif shape_name == "arrow":
            new_nurbs = arrow_shape()
        elif shape_name == "cube":
            new_nurbs = cube_shape()
        elif shape_name == "diamond":
            new_nurbs = diamond_shape()
        elif shape_name == "double_arrow":
            new_nurbs = double_arrow_shape()
        elif shape_name == "double_curved_arrow":
            new_nurbs = double_curved_arrow_shape()
        elif shape_name == "triangle":
            new_nurbs = triangle_shape()

        new_shape = cmds.listRelatives(new_nurbs, shapes=True)[0]
        cmds.parent(new_shape, parent, relative=True, shape=True)
        cmds.delete(new_nurbs)
        cmds.setAttr(new_shape + ".overrideEnabled", override_enabled)
        cmds.setAttr(new_shape + ".overrideRGBColors", override_rgb_colors)
        cmds.setAttr(new_shape + ".overrideColorRGB", override_color_rgb[0][0], override_color_rgb[0][1], override_color_rgb[0][2])
        cmds.rename(new_shape, "{}Shape".format(parent))

    cmds.select(selection)


def circle_shape():
    new_nurbs = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0))
    del_history(new_nurbs)
    return new_nurbs[0]


def triangle_shape():
    new_nurbs = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), s=2, d=1)
    del_history(new_nurbs)
    return new_nurbs[0]


def square_shape():
    new_nurbs = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), s=4, d=1)
    del_history(new_nurbs)
    return new_nurbs[0]


def arrow_shape():
    new_nurbs = cmds.curve(
        p=[(0, 0, 4), (3, 0, 1), (1, 0, 1), (1, 0, -4), (-1, 0, -4), (-1, 0, 1), (-3, 0, 1), (0, 0, 4)], d=1)
    del_history(new_nurbs)
    return new_nurbs


def double_arrow_shape():
    new_nurbs = cmds.curve(
        p=[(0, 0, 6), (3, 0, 3), (1, 0, 3), (1, 0, -3), (3, 0, -3), (0, 0, -6),
           (-3, 0, -3), (-1, 0, -3), (-1, 0, 3), (-3, 0, 3), (0, 0, 6)], d=1)
    del_history(new_nurbs)
    return new_nurbs


def diamond_shape():
    new_nurbs = cmds.curve(
        p=[(0, 0, 3), (1, 0, 1), (3, 0, 0), (1, 0, -1), (0, 0, -3), (-1, 0, -1), (-3, 0, 0), (-1, 0, 1), (0, 0, 3)], d=1)
    del_history(new_nurbs)
    return new_nurbs


def crossed_arrow_shape():
    new_nurbs = cmds.curve(
        p=[(0, 0, 6), (3, 0, 4), (1, 0, 4), (1, 0, 1), (4, 0, 1), (4, 0, 3), (6, 0, 0),
           (4, 0, -3), (4, 0, -1), (1, 0, -1), (1, 0, -4), (3, 0, -4), (0, 0, -6),
           (-3, 0, -4), (-1, 0, -4), (-1, 0, -1), (-4, 0, -1), (-4, 0, -3), (-6, 0, 0),
           (-4, 0, 3), (-4, 0, 1), (-1, 0, 1), (-1, 0, 4), (-3, 0, 4), (0, 0, 6)], d=1)
    del_history(new_nurbs)
    return new_nurbs


def double_curved_arrow_shape():
    new_nurbs = cmds.curve(p=[(0, 0, 6), (3, 0, 3), (1, 0, 3), (), (), (), (1, 0, -3), (3, 0, -3), (0, 0, -6),
           (-3, 0, -3), (-1, 0, -3), (-1, 0, 3), (-3, 0, 3), (0, 0, 6)], d=1)
    return new_nurbs


def cube_shape():
    new_nurbs = cmds.curve(
        p=[(2, -2, 2), (-2, -2, 2), (-2, -2, -2), (2, -2, -2), (2, -2, 2),
           (2, 2, 2), (-2, 2, 2), (-2, -2, 2), (-2, 2, 2), (-2, 2, -2), (-2, -2, -2), (-2, 2, -2),
           (2, 2, -2), (2, -2, -2), (2, 2, -2), (2, 2, 2)], d=1)
    del_history(new_nurbs)

    return new_nurbs


def loc_shape():
    new_nurbs = cmds.spaceLocator()
    del_history(new_nurbs)
    return new_nurbs


def del_history(shape):
    cmds.delete(shape, constructionHistory=True)
