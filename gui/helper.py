from typing import Dict, Callable

import PySimpleGUI as sg


class EventLoop:
    def __init__(self) -> None:
        self.handler: Dict[str, Callable] = {}

    def generate_key(self):
        from uuid import uuid4

        return uuid4().hex

    def on(self, event: sg.Element | str, handler: Callable):
        if isinstance(event, sg.Element):
            key = event.key
        else:
            key = event
        self.handler[key] = handler

    def on_refresh(self):
        pass

    REFRESH = "___refresh"

    def run(self, window):
        while True:
            # Display and interact with the Window
            event, values = window.read()  # Part 4 - Event loop or Window.read call
            if event == sg.WINDOW_CLOSED:
                break

            print(event)
            print(values)

            if event in self.handler:
                handler = self.handler[event]
                res = handler(event, values)
                if res == EventLoop.REFRESH:
                    break

        # Do something with the information gathered
        if values:
            print("Hello", values[0], "! Thanks for trying PySimpleGUI")

        # # Finish up by removing from the screen
        # window.close()
