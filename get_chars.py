import random
import string
import cv2
import json

def merge_near_components(stats, dist_x, dist_y):
    i = 2

    num_labels = len(stats)

    while i < num_labels:
        x = stats[i][cv2.CC_STAT_LEFT]
        y = stats[i][cv2.CC_STAT_TOP]
        w = stats[i][cv2.CC_STAT_WIDTH]
        h = stats[i][cv2.CC_STAT_HEIGHT]

        x_2 = stats[i-1][cv2.CC_STAT_LEFT]
        y_2 = stats[i-1][cv2.CC_STAT_TOP]
        w_2 = stats[i-1][cv2.CC_STAT_WIDTH]
        h_2 = stats[i-1][cv2.CC_STAT_HEIGHT]

        min_y = min(y_2+h_2, y+h)
        max_y = max(y_2, y)

        if max_y-min_y <= dist_y and abs(x_2 - x) <= dist_x:
            new_y = min(y, y_2)
            new_x = min(x, x_2)

            stats[i][cv2.CC_STAT_LEFT] = new_x
            stats[i][cv2.CC_STAT_TOP] = new_y
            stats[i][cv2.CC_STAT_WIDTH] =  max(x+w, x_2+w_2) - new_x
            stats[i][cv2.CC_STAT_HEIGHT] = max(y+h, y_2+h_2) - new_y

            stats.pop(i-1)
            num_labels -= 1

        i += 1

def sort_components_by_left(stats):
    return sorted(
        stats, key=lambda x: x[cv2.CC_STAT_LEFT])


def generate_random_string(n = 15):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def get_chars():
    img = cv2.imread("./chars.png", cv2.IMREAD_GRAYSCALE)

    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    _, _,  stats, _ = cv2.connectedComponentsWithStats(img)

    stats = sort_components_by_left(stats)
    merge_near_components(stats, 13, 20)

    chars_info = []

    for i in range(1, len(stats)):
        x = stats[i][cv2.CC_STAT_LEFT]
        y = stats[i][cv2.CC_STAT_TOP]
        w = stats[i][cv2.CC_STAT_WIDTH]
        h = stats[i][cv2.CC_STAT_HEIGHT]

        img_char = img[y:y+h, x:x+w]

        name = generate_random_string()
        dest = f"./chars/{name}.png"

        chars_info.append({
            "char": chars[i-1],
            "filename":  dest,
            "id": name
        })


        cv2.imwrite(dest, img_char)

    with open("./chars.json", "w+") as file:
        file.write(json.dumps(chars_info, indent=4))

get_chars()