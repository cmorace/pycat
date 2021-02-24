from pycat.core import Window

window = Window()
label = window.create_label()
label.text = "hello, world!"
label.x = 10000
label.y = 10000
window.run()
