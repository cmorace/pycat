"""The image module contains functions for loading or creating image data."""
from typing import Tuple, Union

from pyglet.image import Animation, CheckerImagePattern, SolidColorImagePattern, Texture
from pyglet.resource import ResourceNotFoundException
from pyglet.resource import animation as pyglet_animation
from pyglet.resource import image as pyglet_image

from pycat.debug.print import print_failure as debug_failure

class Image():

    @staticmethod
    def get_solid_color_texture(width: int = 2, 
                                height: int = 2, 
                                rgba: Tuple[int, int, int, int] 
                                      = (255, 255, 255, 255)) -> Texture:
        solid_pattern = SolidColorImagePattern(rgba)
        texture = solid_pattern.create_image(width, height).get_texture()
        texture.anchor_x = texture.width / 2
        texture.anchor_y = texture.height / 2
        return texture

    @staticmethod
    def get_checker_texture(width: int = 2,
                            height: int = 2,
                            rgba_a: Tuple = (255, 0, 0, 150),
                            rgba_b: Tuple = (0, 0, 0, 150)) -> Texture:
        checker_pattern = CheckerImagePattern(rgba_a, rgba_b)
        texture = checker_pattern.create_image(width, height).get_texture()
        texture.anchor_x = texture.width / 2
        texture.anchor_y = texture.height / 2
        return texture

    @staticmethod
    def get_image_from_file(img_file: str) -> Union[Animation, Texture]:
        if img_file.endswith(".svg"):
            debug_failure("svg support not yet implemented")
            img = Image.get_checker_texture(width=20, height=20)
        elif img_file.endswith(".gif"):
            img = Image.get_animation_from_file(img_file)
        else:
            img = Image.get_texture_from_file(img_file)
        return img

    @staticmethod
    def get_texture_from_file(img_file: str) -> Texture:
        try:
            texture: Texture = pyglet_image(img_file)
            texture.anchor_x = texture.width / 2
            texture.anchor_y = texture.height / 2
        except ResourceNotFoundException:
            debug_failure("oops, image '" + img_file + "' is not found")
            texture = Image.get_checker_texture()
        return texture

    @staticmethod
    def get_animation_from_file(gif_file: str, dt: float = 0.1) -> Animation:
        try:
            animation: Animation = pyglet_animation(gif_file)
        except ResourceNotFoundException:
            debug_failure("oops, image '" + gif_file + "' is not found")
            images = [
                Image.get_checker_texture(rgba_a=(255, 0, 0, 150), 
                                          rgba_b=(0, 0, 0, 150)),
                Image.get_checker_texture(rgba_a=(0, 0, 0, 150),
                                          rgba_b=(255, 0, 0, 150)),
            ]
            animation = Animation.from_image_sequence(images, duration=dt)
        # set origin to image center
        x: float = animation.get_max_width() / 2
        y: float = animation.get_max_height() / 2
        for frame in animation.frames:
            frame.image.anchor_x = x
            frame.image.anchor_y = y
        return animation