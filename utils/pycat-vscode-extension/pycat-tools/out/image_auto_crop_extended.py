"""script to auto-crop png images."""

from os import listdir, makedirs
from os.path import basename, exists
import sys

from PIL import Image
from pycat.base import BaseSprite as Sprite
from pycat.resource import set_resource_directory
from pycat.base import NumpyImage
from numpy import flip

# todo: add support for GIF images

input_folder = str(sys.argv[1])  # can assume is folder
output_folder = input_folder + "/images_cropped/"
set_resource_directory(input_folder + "/")

img_files = [basename(f) for f in listdir(input_folder)
             if f.endswith('.png')]
if len(img_files) == 0:
    print("no images in '{}' to process".format(input_folder))
    quit()

if not exists(output_folder):
    makedirs(output_folder)

# load the PNGs to texture memory
# this is slower but fixes a previous bug
for file in img_files:
    sprite = Sprite.create_from_file(file)
    image_data = sprite.texture.get_image_data()
    img_array = NumpyImage.get_array_from_texture(sprite.texture)
    img = NumpyImage.crop_alpha_array(img_array)
    pil_image = Image.fromarray(flip(img, 0))
    pil_image.save(output_folder + file)

# There is a bug in the code below, was not working for dw's png files.
# It was loading the images as RGB rather than RGBA
# I am curious why, it is much faster than loading each image to texture
# ----------------------------------------------------------------------
# images = [array(Image.open(input_folder + "/" + f)) for f in files]
# for i in range(len(images)):

#     region = argwhere(images[i][..., 3])  # <- error here, no alpha loaded

#     min_i, max_i = min(region[:, 0]), max(region[:, 0])
#     min_j, max_j = min(region[:, 1]), max(region[:, 1])
#     p_image = Image.fromarray(images[i][min_i:max_i, min_j:max_j, ...])
#     if not exists(output_folder):
#         makedirs(output_folder)
#     p_image.save(output_folder + "/" + files[i])
#     print("saved file", output_folder + "/" + files[i])
