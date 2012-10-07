import math

def awesome_positioning(slide, slides):
    if slide.index > 0:
        slide.x += 1000
        slide.y += 1000
        slide.rotate_y += 45


def documentation(slide, slides):
    x = 1000
    rotate_z = 0
    for slide in slides:
        if not slide.scale:
            slide.scale = 1
        if slide.index in (3, 7, 10):
            slide.y += 800
            slide.x += x
            x = -x
        if slide.id == 'hidden-title':
            slides[slide.index + 1].update(slides[slide.index - 1])
            rotate_z = 180
            slide.x += 1700
            slide.rotate_z = 90
        elif slide.id == 'overriding-the-defaults':
            slide.rotate_x = 180
            slide.y -= 800
            slide.x += x
            slide.z = -1000
            slides[slide.index + 1].update(slide)
        else:
            slide.rotate_z = rotate_z
            slide.x += x
            try:
                slides[slide.index + 1].update(slide)
            except IndexError:
                pass
    return True
