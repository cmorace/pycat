"""This is a small python application to quickly manipulate images.

-------------------------------------------------------------------------------
Instructions:
Before you run this application:
- In the same directory as this script you must have a folder named 'images'
- In the 'images' folder you must have at least one PNG image.
After you run this application:
1. Press the left and right arrow keys to cycle through the images. On the left
   side of the window you will see the original image and on the right side you
   will see the automatically cropped image.
2. Press the up and down arrow keys or scroll the mouse to change the scale of
   the cropped image.
3. Press the 'r' and 'f' keys to rotate and flip the cropped image.
4. Press the 'enter' key to save the image to file. The file will be saved
   to a folder named 'images_cropped' next to the input 'images' folder.
------------------------------------------------------------------------------
Note: Some images may contain pixels with small alpha values that are
       difficult to perceive with the human eye. These images may not
       be cropped as expected.
"""
from os import listdir, makedirs
from os.path import basename, exists
import sys

from PIL import Image
from numpy import flip, rot90

from pycat.base import BaseSprite as Sprite
from pycat.base import BaseWindow as Window
from pycat.base import NumpyImage, ImageFormat
from pycat.base import Animation, Texture
from pycat.base.event import KeyCode, KeyEvent, MouseEvent
from pycat.debug import draw_sprite_rects
from pycat.resource import set_resource_directory


# todo: add manual cropping for non-transparent images
# todo: add support for GIF images

input_folder = str(sys.argv[1])  # can assume is folder
output_folder = input_folder + "/images_edited/"
set_resource_directory(input_folder + "/")


img_files = [basename(f) for f in listdir(input_folder)
             if f.endswith(('.png', '.jpg', '.gif', '.bmp'))]
if len(img_files) == 0:
    print("no images in '{}' to process".format(input_folder))
    quit()


window = Window(title="Image Crop and Scale")


def get_cropped_sprite(current_sprite_index: int):
    current_sprite_index %= len(img_files)
    sprite = Sprite.create_from_file(img_files[current_sprite_index])
    if isinstance(sprite._sprite.image, Animation):
        frames = sprite._sprite.image.frames
        print("animation with", len(frames), "frames")
        for i in range(len(frames)):
            texture: Texture = frames[i].image
            print("frame", i, "format:", texture.get_image_data().format)
    else:
        image_data = sprite.texture.get_image_data()
        print("image format:", image_data.format)
        if image_data.format == "RGBA":
            image = NumpyImage.get_array_from_texture(sprite.texture)
            img = NumpyImage.crop_alpha_array(image)
            format = ImageFormat.RGBA
            sprite.texture = NumpyImage.get_texture_from_array(img, format)

    sprite.position = window.center
    return sprite


def save_scaled_sprite_image(scaled_sprite: Sprite, file: str):
    img_array = NumpyImage.get_array_from_texture(cropped_sprite.texture)
    pil_image = Image.fromarray(flip(img_array, 0))
    size = (round(scaled_sprite.width), round(scaled_sprite.height))
    pil_image = pil_image.resize(size, reducing_gap=3)
    pil_image.save(file)


current_sprite_index = 0
cropped_sprite = get_cropped_sprite(current_sprite_index)
window.set_clear_color(254, 232, 200, 0)
selection_sprite = Sprite.create_from_color((0, 255, 0, 100))


@window.on_draw
def draw():
    window.clear()
    cropped_sprite.draw()
    selection_sprite.draw()
    draw_sprite_rects([cropped_sprite, selection_sprite])


def on_key_press(key: KeyEvent):
    global cropped_sprite, current_sprite_index
    if key == KeyCode.ENTER:
        if not exists(output_folder):
            makedirs(output_folder)
        saved_file = output_folder + img_files[current_sprite_index]
        save_scaled_sprite_image(cropped_sprite, saved_file)
        print("image saved to " + saved_file)

    elif key == KeyCode.LEFT:
        current_sprite_index -= 1
        cropped_sprite = get_cropped_sprite(current_sprite_index)

    elif key == KeyCode.RIGHT:
        current_sprite_index += 1
        cropped_sprite = get_cropped_sprite(current_sprite_index)

    elif key == KeyCode.UP:
        cropped_sprite.scale *= 1.1
        selection_sprite.scale *= 1.1

    elif key == KeyCode.DOWN:
        cropped_sprite.scale *= 0.9
        selection_sprite.scale *= 0.9

    elif key == "r":
        img = NumpyImage.get_array_from_texture(cropped_sprite.texture)
        cropped_sprite.texture = NumpyImage.get_texture_from_array(
            rot90(img), ImageFormat.RGBA)

    elif key == "f":
        img = flip(NumpyImage.get_array_from_texture(cropped_sprite.texture),
                   0)
        cropped_sprite.texture = NumpyImage.get_texture_from_array(
            img, ImageFormat.RGBA)


def on_mouse_scroll(mouse: MouseEvent):
    if mouse.delta.y > 0:
        cropped_sprite.scale *= 1.05
        selection_sprite.scale *= 1.05
    elif mouse.delta.y < 0:
        cropped_sprite.scale *= 0.95
        selection_sprite.scale *= 0.95


def on_mouse_press(mouse: MouseEvent):
    selection_sprite.scale = 1
    selection_sprite.scale_x = 1
    selection_sprite.scale_y = 1
    selection_sprite.start_point = mouse.position


def on_mouse_drag(mouse: MouseEvent):
    delta = mouse.position - selection_sprite.start_point
    selection_sprite.scale_x = delta.x
    selection_sprite.scale_y = delta.y
    selection_sprite.position = selection_sprite.start_point + delta/2


window.run(on_key_press=on_key_press,
           on_mouse_scroll=on_mouse_scroll,
           on_mouse_press=on_mouse_press,
           on_mouse_drag=on_mouse_drag)
