from pycat.window import Window
from pycat.sprite import Sprite

window = Window()

window.create_sprite(tags=['one'])

print(window.get_all_sprites())
window.dump_all_sprites()

window.create_sprite(tags=['two'])

print(window.get_all_sprites())
window.dump_all_sprites()

window.run()