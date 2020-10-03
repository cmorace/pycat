"""script to auto-crop png images."""

from os import listdir, makedirs
from os.path import basename, exists
import sys

from PIL import Image
from numpy import array, argwhere, min, max

# todo: add support for GIF images
input_folder = str(sys.argv[1])
output_folder = input_folder + "/images_cropped/"
files = [basename(f) for f in listdir(input_folder) if f.endswith('.png')]
if len(files) == 0:
    print("no .png images in '{}' to process".format(input_folder))
    quit()

images = [array(Image.open(input_folder + "/" + f)) for f in files]
for i in range(len(images)):
    region = argwhere(images[i][..., 3])
    min_i, max_i = min(region[:, 0]), max(region[:, 0])
    min_j, max_j = min(region[:, 1]), max(region[:, 1])
    p_image = Image.fromarray(images[i][min_i:max_i, min_j:max_j, ...])
    if not exists(output_folder):
        makedirs(output_folder)
    p_image.save(output_folder + "/" + files[i])
    print("saved file", output_folder + "/" + files[i])
