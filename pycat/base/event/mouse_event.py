"""Implements the MouseEvent class."""
from pyglet.window import key, mouse
from pycat.geometry.point import Point
from pycat.base.event.key_event import KeyCode

class MouseButton:
    NONE = 0
    LEFT = mouse.LEFT
    MIDDLE = mouse.MIDDLE
    RIGHT = mouse.RIGHT
    

class MouseEvent:
    """Class for handling mouse events."""    

    def __init__(self,
                 x: int,
                 y: int,
                 dx: int = 0,
                 dy: int = 0,
                 button: int = MouseButton.NONE,
                 modifier: int = KeyCode.MOD_NONE):

        self.__x = x
        self.__y = y
        self.__dx = dx
        self.__dy = dy
        self.__button = button
        self.__modifier = modifier

    @property
    def position(self) -> Point:
        """Return the (x,y) position of the mouse event.

        This property is updated for every mouse event.
        """
        return Point(self.__x, self.__y)

    @property
    def delta(self) -> Point:
        """Return the change in mouse position since last mouse event.

        `Point` returned by:
        - `on_mouse_motion`
        - `on_mouse_drag`
        - `on_mouse_scroll`.

        `None` returned by all other mouse events

        :return: change in mouse position since last update
        :rtype: Optional[Point]
        """
        if self.__dx is not None and self.__dy is not None:
            return Point(self.__dx, self.__dy)
        else:
            return Point(0, 0)

    @property
    def button(self) -> int:
        """Return the mouse button.

        Returns either:
        - `MouseEvent.LEFT_BUTTON`
        - `MouseEvent.MIDDLE_BUTTON`
        - `MouseEvent.RIGHT_BUTTON`
        - `MouseEvent.NO_BUTTON`

        :return: mouse button
        :rtype: Optional[int]
        """
        return self.__button

    @property
    def modifier(self) -> int:
        """Return `KeyCode` if modifier key is pressed on mouse event.

        :return: modifier `KeyCode`
        :rtype: Optional[int]
        """
        return self.__modifier
        

    @property
    def button_string(self) -> str:
        """Return string for button property.

        Possible return values:
        - `"Left"`
        - `"Middle"`
        - `"Right"`
        - `"None"`

        :return: string for button property
        :rtype: str
        """
        if self.button == MouseButton.LEFT:
            return "Left"
        elif self.button == MouseButton.MIDDLE:
            return "Middle"
        elif self.button == MouseButton.RIGHT:
            return "Right"
        else:
            return "None"

    @property
    def modifier_string(self) -> str:
        """Return string for modifier property.

        :return: String for modifier property
        :rtype: str
        """
        if self.modifier == KeyCode.MOD_NONE:
            return "None"
        return key.modifiers_string(self.modifier)

    def __str__(self) -> str:
        """Return string of event properties.

        :return: String representation of `MouseEvent`.
        :rtype: str
        """
        return ("{ x: " + str(self.__x) +
                ", y: " + str(self.__y) +
                ", dx: " + str(self.__dx) +
                ", dy: " + str(self.__dy) +
                ", button: " + self.button_string +
                ", modifier: " + self.modifier_string + " }")
