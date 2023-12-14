import json
import sys
import cv2
import numpy as np
from check_weapon import compare_images_shapes

from get_chars import generate_random_string, sort_components_by_left, merge_near_components

def get_name(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    width = gray.shape[1] * 3
    height = gray.shape[0] * 3
    size = (width, height)

    gray = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)
    cv2.imwrite("name_1.png", gray)

    _, threshold = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)

    cv2.imwrite("name_2.png", threshold)
    
    _, _,  stats, _ = cv2.connectedComponentsWithStats(threshold)

    stats = sort_components_by_left(stats)
    print(len(stats))
    merge_near_components(stats, 0, 6),
    print(len(stats))

    chars = []

    for i in range(1, len(stats)):
        x = stats[i][cv2.CC_STAT_LEFT]
        y = stats[i][cv2.CC_STAT_TOP]
        w = stats[i][cv2.CC_STAT_WIDTH]
        h = stats[i][cv2.CC_STAT_HEIGHT]

        # print(y,y+h, x,x+w)

        chars.append(threshold[y:y+h, x:x+w])

    name = ""

    for char in chars:
        name += check_char(char)
    
    print(name)

def check_char(img):
    with open("./chars_2.json") as file:
        chars = json.loads(file.read())

    min_score = sys.maxsize
    min_score_char = None

    for char in chars:
        char_img = cv2.imread(char["filename"], cv2.IMREAD_GRAYSCALE)
        score = compare_images_shapes(char_img, img)

        # print(char["char"])
        # print(score)
        # print()

        if score < min_score:
            min_score = score
            min_score_char = char


    # print(min_score_char["char"])
    # print(min_score)

    # input()

    return min_score_char["char"]
