import cv2
import numpy as np

from check_agent import check_agent
from check_weapon import check_weapon


def main():
    agent = cv2.imread("./agent.png")

    check_agent(agent)

    weapon = cv2.imread("./vandal.png", cv2.IMREAD_GRAYSCALE)

    _, weapon = cv2.threshold(weapon, 128, 255, cv2.THRESH_BINARY)

    check_weapon(weapon)


if __name__ == "__main__":
    main()
