from __future__ import annotations

from spinners import Spinners


class DotSpinner:
    def __init__(self, text: str = ""):
        self.text = text
        self.current_index = 0
        self.frames = Spinners.dots12.value["frames"]

    def __next__(self) -> None:
        if self.current_index == len(self.frames):
            self.current_index = 0
        print(f"{self.frames[self.current_index]} {self.text}", end="\r")
        self.current_index += 1
