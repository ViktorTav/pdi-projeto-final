import json
import cv2
import numpy as np


def check_agent(img):
    # TODO: Deixar a lista de agentes carregadas previamentes
    # Seus histogramas também

    with open("./agents.json") as file:
        agents = json.loads(file.read())

    max_score = -1
    max_score_agent = None
    for agent in agents:
        agent_img = cv2.imread(agent["filename"], cv2.IMREAD_UNCHANGED)
        score = compare_images(agent_img, img)

        if score > max_score:
            max_score = score
            max_score_agent = agent

    print(max_score_agent["name"])
    print(max_score)


def create_histogram(img):
    bins = 8
    bins_range = 256//bins
    histogram = np.zeros((bins, bins, bins), np.uint8)

    height = img.shape[0]
    width = img.shape[1]

    for x in range(0, height):
        for y in range(0, width):

            blue = img[x][y][0]//bins_range
            green = img[x][y][1]//bins_range
            red = img[x][y][2]//bins_range

            histogram[blue][green][red] += 1

    return histogram


def compare_images(img, img2):
    img_histogram = create_histogram(img)
    img2_histogram = create_histogram(img2)

    bins = img_histogram.shape[0]

    score = 0

    # Aqui fazermos a comparação do histograma por método de intersecção.

    for x in range(bins):
        for y in range(bins):
            for z in range(bins):
                score += min(img_histogram[x]
                             [y][z], img2_histogram[x][y][z])

    return score
