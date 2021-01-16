from pyglet.gl.gl import (
    glTexParameteri,
    GL_TEXTURE_2D,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_LINEAR,
    GL_NEAREST)


# todo: add boolean keyword argument to window and call before run
def set_sharp_pixel_scaling(is_sharp_pixel_scaling: bool):
    """Set to true to keep pixels sharp when scaling sprites.

    Use this function right before calling `window.run()`.
    """
    if is_sharp_pixel_scaling:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    else:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
