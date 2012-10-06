from impress.funcs import defaults


def awesome_positioning(directive, i, coord):
    coord.update(defaults)
    coord['x'] += 1000
    return coord
