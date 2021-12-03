from pycat.core import Window, Label, Point, Color, Sprite

window = Window()

label1 = window.create_label(text='aaaaaaaaaaa', position=Point(300,300))
sprite = window.create_sprite(scale=30, color=Color.BLUE, position=Point(300,300))


label2 = window.create_label(text='AAAAAAAAAAAA', position=Point(500,300))
sprite = window.create_sprite(scale=30, color=Color.BLUE, position=Point(500,300))

label3 = window.create_label(text='With a tuple', position=(20,20))

print(label3.position)


window.run()
