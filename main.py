from threading import Thread, Event
from time import time
from typing import Callable
import numpy as np
import pyautogui
import cv2

WIDTH, HEIGHT = pyautogui.size()

CARD_HEIGHT = int(HEIGHT*0.031)
CARD_WIDTH = int(WIDTH/3+10)
CARD_LIMIT = 6
MARGIN = int(0.005*HEIGHT)

# Refs: https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval/48709380#48709380


class Interval:
    interval: float
    action: callable
    thread: Thread
    stopEvent: Event

    def __init__(self, interval: float, action: Callable) -> None:
        self.interval = interval
        self.action = action
        self.stopEvent = Event()
        self.thread = Thread(target=self._interval_handler)

        self.thread.start()

    def _interval_handler(self):
        nextTime = time() + self.interval
        while not self.stopEvent.wait(nextTime - time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


def get_cards(img):

    cards = []

    for i in range(0, CARD_LIMIT):
        card = np.zeros((CARD_HEIGHT, CARD_WIDTH, 3))

        card_y_position = (CARD_HEIGHT+MARGIN) * i

        card = img[card_y_position:card_y_position + CARD_HEIGHT][:][:]
        cards.append(card)

    return cards


def take_screenshot():
    return pyautogui.screenshot(region=(
        int(WIDTH-CARD_WIDTH),
        int(HEIGHT*0.08888),
        int(CARD_WIDTH),
        int(CARD_LIMIT*(CARD_HEIGHT+MARGIN*2))
    ))


def get_screen_info():
    screenshoot = take_screenshot()

    img = np.array(screenshoot.getdata(), dtype=np.uint8).reshape(
        (screenshoot.size[1], screenshoot.size[0], 3))

    cards = get_cards(img)

    for i in range(0, len(cards)):
        cards[i] = cv2.cvtColor(cards[i], cv2.COLOR_RGB2BGR)
        cv2.imwrite(f"./imgs/{time()}_card_{i}.png",
                    cards[i])


def main():
    interval = Interval(0.5, get_screen_info)


if __name__ == "__main__":
    main()
