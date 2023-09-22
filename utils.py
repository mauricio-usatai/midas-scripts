from __future__ import annotations

from spinners import Spinners
from twilio.rest import Client as TwilioClient

from settings import Settings


settings = Settings()


class DotSpinner:
    __slots__ = (
        "text",
        "frames",
        "current_index",
    )

    def __init__(self, text: str = ""):
        self.text = text
        self.current_index = 0
        self.frames = Spinners.dots12.value["frames"]

    def __next__(self) -> None:
        if self.current_index == len(self.frames):
            self.current_index = 0
        print(f"{self.frames[self.current_index]} {self.text}", end="\r")
        self.current_index += 1


class SMSMessenger:
    __slots__ = ("client",)

    def __init__(self):
        self.client = TwilioClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)

    def send(self, message: str):
        message = self.client.messages.create(
            body=message,
            from_=settings.FROM_NUMBER,
            to=settings.TO_NUMBER,
        )
