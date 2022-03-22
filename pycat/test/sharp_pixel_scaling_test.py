from pycat.core import Window

is_label_created_before = False

window = Window(is_sharp_pixel_scaling=True)

if is_label_created_before:
    label = window.create_label()
    label.text = 'image should be sharp'

s = window.create_sprite(image='img/pixelish.png', x=100, y=100, scale=30)

if not is_label_created_before:
    label = window.create_label()
    label.text = 'image should be sharp'


def on_update(dt):
    s.x += 1


window.run(update_function=on_update)
