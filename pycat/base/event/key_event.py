"""Implements the KeyCode and KeyEvent classes."""
from pyglet.window import key
from typing import Any


def print_key_dictionary():
    """Print all members of the `pyglet.window.key` module.

    This is useful for setting new constant KeyCode values.
    """
    for c in key.__dict__:
        print("    " + c + " = key." + c)


class KeyCode:
    """The KeyCode class defines constants for key symbols.

    Key symbols which can be represented by normal ascii characters
    are not included. Instead use the `KeyEvent`'s `event.character`
    property and compare with the symbol's string representation.
    Printing KeyEvents will print out the constant's name if you are
    unsure which constant to use for comparison.

    The KeyCode class includes constants for:
    - Modifier Keys (for comparing the KeyEvent.modifier property)
    - Number Pad Key Symbols
    - Function Key Symbols
    - Arrow Key Symbols
    """

    # Modifier Keys
    MOD_SHIFT = key.MOD_SHIFT
    MOD_CTRL = key.MOD_CTRL
    MOD_ALT = key.MOD_ALT
    MOD_CAPSLOCK = key.MOD_CAPSLOCK
    MOD_NUMLOCK = key.MOD_NUMLOCK
    MOD_WINDOWS = key.MOD_WINDOWS
    MOD_COMMAND = key.MOD_COMMAND
    MOD_OPTION = key.MOD_OPTION
    MOD_FUNCTION = key.MOD_FUNCTION
    MOD_ACCEL = key.MOD_ACCEL  # macos: command, other: control
    MOD_NONE = 0

    # Number Pad Keys
    NUM_0 = key.NUM_0
    NUM_1 = key.NUM_1
    NUM_2 = key.NUM_2
    NUM_3 = key.NUM_3
    NUM_4 = key.NUM_4
    NUM_5 = key.NUM_5
    NUM_6 = key.NUM_6
    NUM_7 = key.NUM_7
    NUM_8 = key.NUM_8
    NUM_9 = key.NUM_9

    # Function Keys
    F1 = key.F1
    F2 = key.F2
    F3 = key.F3
    F4 = key.F4
    F5 = key.F5
    F6 = key.F6
    F7 = key.F7
    F8 = key.F8
    F9 = key.F9
    F10 = key.F10
    F11 = key.F11
    F12 = key.F12

    # Arrow Keys
    LEFT = key.LEFT
    UP = key.UP
    RIGHT = key.RIGHT
    DOWN = key.DOWN

    # other symbol codes
    BACKSPACE = key.BACKSPACE
    TAB = key.TAB
    RETURN = key.RETURN
    ENTER = key.ENTER
    SPACE = key.SPACE
    FUNCTION = key.FUNCTION
    LSHIFT = key.LSHIFT
    RSHIFT = key.RSHIFT
    LCTRL = key.LCTRL
    RCTRL = key.RCTRL
    CAPSLOCK = key.CAPSLOCK
    LALT = key.LALT
    RALT = key.RALT
    LWINDOWS = key.LWINDOWS
    RWINDOWS = key.RWINDOWS
    LCOMMAND = key.LCOMMAND
    RCOMMAND = key.RCOMMAND
    LOPTION = key.LOPTION
    ROPTION = key.ROPTION


class KeyEvent:
    """The KeyEvent class is used for event handling.

    Instances of the KeyEvent class are passed as arguments
    from event dispatchers to event listeners.

    Properties:
    -symbol
    """

    def __init__(self, symbol: int, modifier: int = KeyCode.MOD_NONE):
        """Construct new instance of KeyEvent class."""
        self.__symbol = symbol
        self.__modifier = modifier

    @property
    def symbol(self) -> int:
        """Return `KeyCode` for key symbol."""
        return self.__symbol

    @property
    def modifier(self) -> int:
        """Get the modifier value.

        Can be compared to `KeyCode` MOD constants.
        Returns `MOD_NONE` if no modifier key is pressed/released.
        """
        return self.__modifier

    @property
    def character(self) -> str:
        """Return string representation for typeable KeyCodes."""
        if 32 <= self.symbol <= 126:  # it's an ascii value
            if self.modifier == KeyCode.MOD_SHIFT:
                if 97 <= self.symbol <= 122:
                    return chr(self.symbol - 32)  # upper-case letter
                elif self.symbol == 92:
                    return "|"  # Fixes a bug in pyglet (tested on MacOS)
                else:
                    return chr(self.symbol)
            else:
                return chr(self.symbol)
        elif self.symbol == KeyCode.ENTER:
            return '\n'
        else:
            return ""  # key can't be compared to standard string (use KeyCode)

    @property
    def symbol_string(self) -> str:
        """Print the KeyCode constant name."""
        return key.symbol_string(self.symbol)

    @property
    def modifier_string(self) -> str:
        """Print the KeyCode modifier name."""
        if self.modifier is KeyCode.MOD_NONE:
            return "None"
        return key.modifiers_string(self.modifier)

    def __str__(self):
        """Print the event properties."""
        return ("{ symbol: " + self.symbol_string +
                ", modifier: " + self.modifier_string +
                ", character: '" + self.character + "' }")

    def __eq__(self, key: Any) -> bool:
        """Overload equality comparison operator for KeyEvent class.

        KeyEvents can be checked against all typeable ascii characters
        or KeyCode Constants
        """
        if key:
            if isinstance(key, str):
                return self.character == key
            elif isinstance(key, int):
                return self.symbol == key
        return False
