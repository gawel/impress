def awesome_positioning(slide, i, coord, slides):
    if i > 0:
        coord['x'] += 1000
        coord['y'] += 1000
        coord['rotate_y'] += 45
    return coord
