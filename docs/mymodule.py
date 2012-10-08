def awesome_positioning(slide, slides):
    if slide.index > 0:
        slide.x += 1000
        slide.y += 1000
        slide.rotate_y += 45


def documentation(slide, slides):
    if not slide.incr_x:
        slide.incr_x = 1000
        slide.incr_rotate_z = 0
    if not slide.scale:
        slide.scale = 1
    if slide.index in (3, 7, 10):
        slide.y += 800
        slide.x += slide.incr_x
        slide.incr_x = -slide.incr_x
    if slide.id == 'hidden-title':
        nslide = slides[slide.index + 1]
        nslide.update(slides[slide.index - 1])
        nslide.incr_rotate_z = 180
        slide.x += 1700
        slide.rotate_z = 90
    elif slide.id == 'overriding-the-defaults':
        slide.rotate_x = 180
        slide.y -= 800
        slide.x += slide.incr_x
        slide.z = -1000
    else:
        slide.rotate_z = slide.incr_rotate_z
        slide.x += slide.incr_x
