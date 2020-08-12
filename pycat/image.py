from typing import Optional, Tuple

from pyglet.image import Animation, CheckerImagePattern, Texture
from pyglet.resource import ResourceNotFoundException
from pyglet.resource import image as pyglet_image
from pyglet.resource import animation as pyglet_animation

from .debug import print_failure as debug_failure


def get_texture_from_file(img_file_path: Optional[str]) -> Texture:
    try:
        texture: Texture = pyglet_image(img_file_path)

    except ResourceNotFoundException:
        if img_file_path is not None:
            debug_failure("oops, '" + img_file_path + "' is not found")
        texture = get_checker_texture()

    # set origin to image center
    texture.anchor_x = texture.width / 2
    texture.anchor_y = texture.height / 2

    return texture


def get_checker_texture(
    rgba_a: Tuple = (255, 0, 0, 150),
    rgba_b: Tuple = (0, 0, 0, 150),
    width: int = 100,
    height: int = 100,
) -> Texture:
    checker_pattern = CheckerImagePattern(rgba_a, rgba_b)
    return checker_pattern.create_image(width, height).get_texture()


def get_animation_from_file(gif_file_path: Optional[str]) -> Animation:
    try:
        animation: Animation = pyglet_animation(gif_file_path)

    except ResourceNotFoundException:
        if gif_file_path is not None:
            debug_failure("oops, '" + gif_file_path + "' is not found")

        images = [
            get_checker_texture((255, 0, 0, 150), (0, 0, 0, 150)),
            get_checker_texture((0, 0, 0, 150), (255, 0, 0, 150)),
        ]
        animation = Animation.from_image_sequence(images, duration=0.1)

    # set origin to image center
    x: float = animation.get_max_width() / 2
    y: float = animation.get_max_height() / 2
    for frame in animation.frames:
        frame.image.anchor_x = x
        frame.image.anchor_y = y
    return animation
