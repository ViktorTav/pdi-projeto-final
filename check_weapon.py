import json
import math
import sys
import numpy as np
import cv2


def compare_images_shapes(img1, img2):
    img1_hu_moments = [moment[0]
                       for moment in cv2.HuMoments(cv2.moments(img1))]
    img2_hu_moments = [moment[0]
                       for moment in cv2.HuMoments(cv2.moments(img2))]

    for i in range(0, 7):
        img1_hu_moments[i] = -1 * \
            np.copysign(1.0, img1_hu_moments[i]) * \
            math.log10(abs(img1_hu_moments[i]))

        img2_hu_moments[i] = -1 * \
            np.copysign(1.0, img2_hu_moments[i]) * \
            math.log10(abs(img2_hu_moments[i]))

    score = get_shape_distance(img1_hu_moments, img2_hu_moments)

    return score


def get_shape_distance(hu_moments_1, hu_moments_2):
    distance = 0
    for i in range(0, 7):
        distance += math.fabs(1/hu_moments_2[i] - 1/hu_moments_1[i])

    return distance


def check_weapon(img):
    with open("./weapons.json") as file:
        weapons = json.loads(file.read())

    min_score = sys.maxsize
    min_score_weapon = None

    for weapon in weapons:
        weapon_img = cv2.imread(weapon["filename"], cv2.IMREAD_GRAYSCALE)
        _, weapon_img = cv2.threshold(weapon_img, 128, 255, cv2.THRESH_BINARY)
        score = compare_images_shapes(weapon_img, img)

        print(weapon["name"])
        print(score)

        if score < min_score:
            min_score = score
            min_score_weapon = weapon

    print(min_score_weapon["name"])
    print(min_score)
