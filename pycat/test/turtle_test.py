from pycat.core import Window, Color, Point
from pycat.extensions.turtle import Turtle

window = Window()

turtle = window.create_sprite(Turtle)

turtle.position = Point(100,100)

turtle.move_forward(100)


turtle.position = Point(300,100)
turtle.pen_color = Color.RED
for _ in range(4):
    turtle.move_forward(50)
    turtle.turn_right(90)

turtle.position = Point(500,100)
turtle.pen_width = 4
for _ in range(180):
    turtle.move_forward(2)
    turtle.turn_left(2)

print(turtle.pen_color)
print(turtle.pen_width)

print(turtle.is_pen_down)

turtle.position = Point(600,300)
for _ in range(8):
    turtle.pen_up()
    turtle.move_forward(50)
    turtle.pen_down()
    turtle.move_forward(50)    
    turtle.turn_right(45)


window.run()

