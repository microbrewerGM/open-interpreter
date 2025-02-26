import os
import platform
import time

try:
    import pyautogui
except:
    # Optional packages
    pass


class Keyboard:
    """A class to simulate keyboard inputs"""

    def __init__(self, computer):
        self.computer = computer

    def write(self, text, interval=0.1, **kwargs):
        """
        Type out a string of characters.

        Args:
            text (str): The string to be typed out.
            interval (int or float, optional): The delay between pressing each character key. Defaults to 0.1.
        """
        time.sleep(0.15)
        pyautogui.write(text, interval=interval)
        time.sleep(0.15)

    def press(self, keys, presses=1, interval=0.1, **kwargs):
        """
        Press a key or a sequence of keys.

        If keys is a string, it is treated as a single key and is pressed the number of times specified by presses.
        If keys is a list, each key in the list is pressed once.

        Args:
            keys (str or list): The key(s) to be pressed.
            presses (int, optional): The number of times to press the key. Defaults to 1.
            interval (float, optional): The delay between each key press. Defaults to 0.1.
        """
        time.sleep(0.15)
        if isinstance(keys, str):
            pyautogui.press(keys, presses=presses, interval=interval)
        elif isinstance(keys, list):
            for key in keys:
                pyautogui.press(key, interval=interval)
        time.sleep(0.15)

    def hotkey(self, *args, interval=0.1, **kwargs):
        """
        Press a sequence of keys in the order they are provided, and then release them in reverse order.

        Args:
            *args: The keys to be pressed.
        """
        time.sleep(0.15)
        modifiers = {
            "command": "command down",
            "control": "control down",
            "option": "option down",
            "shift": "shift down",
        }
        if "darwin" in platform.system().lower() and len(args) == 2:
            # pyautogui.hotkey seems to not work, so we use applescript
            # Determine which argument is the keystroke and which is the modifier
            keystroke, modifier = args if args[0] not in modifiers else args[::-1]

            # Map the modifier to the one that AppleScript expects
            modifier = modifiers[modifier]

            if keystroke == "space":
                keystroke = " "

            # Create the AppleScript
            script = f"""
            tell application "System Events"
                keystroke "{keystroke}" using {modifier}
            end tell
            """

            # Execute the AppleScript
            os.system("osascript -e '{}'".format(script))
        else:
            pyautogui.hotkey(*args, interval=interval)
        time.sleep(0.15)

    def down(self, key):
        """
        Simulate the pressing down of a key.

        Args:
            key (str): The key to be pressed down.
        """
        time.sleep(0.15)
        pyautogui.keyDown(key)
        time.sleep(0.15)

    def up(self, key):
        """
        Simulate the releasing of a key.

        Args:
            key (str): The key to be released.
        """
        time.sleep(0.15)
        pyautogui.keyUp(key)
        time.sleep(0.15)
