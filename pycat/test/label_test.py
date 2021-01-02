from pycat.core import Window, Label, Color

window = Window(enforce_window_limits=False)


class CustomLabel(Label):
    def on_create(self):
        self.text = "Hello,"
        self.text += "\ncontent height seems a bit off"
        self.color = Color.ROSE
        self.font = "futura"
        self.font_size = 50
        self.x = window.width / 4
        self.y = window.height - 2 * self.font_size
        self.y_speed = 0
        self.background = window.create_sprite()
        self.background.width = self.content_width
        self.background.height = self.content_height
        self.background.x = self.x + self.background.width / 2
        self.background.y = self.y - self.background.height / 2
        self.background.color = Color.get_complement(self.color)

    def on_update(self, dt: float):
        self.y_speed -= 0.7
        self.y += self.y_speed
        self.background.y += self.y_speed
        if self.y - self.content_height < 0:
            self.y = self.content_height
            self.background.y = self.y - self.background.height / 2
            if self.y_speed < -5:
                self.y_speed *= -0.7
            else:
                self.y_speed = 0


window.create_label(CustomLabel)
window.run()
