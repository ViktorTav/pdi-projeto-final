import json
import sys
import cv2
import numpy as np
from check_weapon import compare_images_shapes

from get_chars import generate_random_string, sort_components_by_left, merge_near_components

def get_name(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)
    width = threshold.shape[1] * 3
    height = threshold.shape[0] * 3
    size = (width, height)
    threshold = cv2.resize(threshold, size, interpolation=cv2.INTER_AREA)
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
    with open("./chars.json") as file:
        chars = json.loads(file.read())

    min_score = sys.maxsize
    min_score_char = None

    for char in chars:
        char_img = cv2.imread(char["filename"], cv2.IMREAD_GRAYSCALE)
        _, char_img = cv2.threshold(char_img, 128, 255, cv2.THRESH_BINARY)
        score = compare_images_shapes(char_img, img)

        if score < min_score:
            min_score = score
            min_score_char = char

    return min_score_char["char"]

def main():

    img = cv2.imread("./name.png")
    get_name(img)
    

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray_blur = cv2.GaussianBlur(gray, (11, 11), 0)

    # canny = cv2.Canny(gray, 100, 200)

    # lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, None, 1, 10)

    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         l = lines[i][0]
    #         cv2.line(gray, (l[0], l[1]), (l[2], l[3]),
    #                  (0, 0, 255), 3, cv2.LINE_AA)

    # cv2.imshow("sla", canny)
    # cv2.waitKey()

    # height = img.shape[0]
    # width = img.shape[1]

    # first_line = img[0]

    # colors = []

    # for y in range(0, width):
    #     red = first_line[y][2]
    #     green = first_line[y][1]
    #     blue = first_line[y][0]

    #     red_percentage = red - max(green, blue)
    #     yellow_percentage = abs(red-green) + (red+green) - blue/(red+green)
    #     green_percentage = (green+blue)/2 - red

    #     pixel_info = {
    #         "color": None,
    #         "position": None
    #     }

    #     if red_percentage > 0.5:
    #         pixel_info["color"] = "red"
    #         first_line[y] = 0.2
    #     elif red > 0.4 and green > 0.4 and blue/(red+green) < 0.3:
    #         pixel_info["color"] = "yellow"
    #         first_line[y] = 0.5
    #     elif green_percentage > 0.2:
    #         pixel_info["color"] = "green"
    #         first_line[y] = 1

    #     if pixel_info["color"]:
    #         pixel_info["position"] = (0, y)
    #         colors.append(pixel_info)

    # cv2.imwrite("new_img.png", img*255)

    # print(colors)


if __name__ == "__main__":
    main()
