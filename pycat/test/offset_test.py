from pycat.core import Window

w = Window(enforce_window_limits=False)

s = w.create_sprite(image='img/bear.png')
w.offset.x = w.width-s.width/2
w.offset.y = s.height/2
w.run()
