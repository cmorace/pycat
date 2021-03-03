from pycat.core import Window, Color, Point

window = Window()
w, h, n = window.width, window.height, 50
grid_size = w/n

for i in range(n):
    j = i*grid_size
    if i % 5 == 0:
        window.create_line(Point(0, j), Point(w, j), 2, Color.BLUE)
        window.create_line(Point(j, 0), Point(j, h), 2, Color.BLUE)
    else:
        l1 = window.create_line(Point(0, j), Point(w, j), 1, Color.BLUE)
        l2 = window.create_line(Point(j, 0), Point(j, h), 1, Color.BLUE)
        l1.opacity = 100
        l2.opacity = 100

window.set_clear_color(255, 255, 255)
window.run()
