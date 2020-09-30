# pycat-tools README

Adds commands for 'Auto-Crop' and 'Open Image Editor' to right click menu. The click must be on a folder.


## Features

- 'Auto-Crop' will crop all PNG images in a folder, removing any fully transparent pixels along the border of the orignal image. The cropped images are saved in a sub-folder called 'images_cropped'

- 'Open Image Editor' will open a window where a user can manually edit the images in the folder. On the left side of the windowis the original image and on the right is the autocropped image. User's can manually manipulate the image's

   - scale (mouse scroll or up and down arrows)
   - rotation (the 'r' key will rotate the image by 90 degrees)
   - image orientation (the 'f' key will flip the image along the x-axis)

 Use the right and left arrow keys to cycle through the images and press the 'enter' key to save the edited image

 Edited images are saved to a subfolder called 'images_edited'

## Requirements

Python and Pycat 0.0.6 must be installed

## Extension Settings

No extension settings yet.
Should probably add settings for python path to allow for virtualenvs

## Known Issues


## Release Notes

### 0.0.1
2020-09-30 - Initial release of pycat-tools

## Attribution
Icon by <a href="https://pixabay.com/users/squarefrog-9690118/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4754631">Ed Zilch</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4754631">Pixabay</a>
