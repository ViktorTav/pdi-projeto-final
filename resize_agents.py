import json
import cv2


def resize_agents():
    with open("./agents.json") as file:
        agents = json.loads(file.read())

    for agent in agents:
        agent_img = cv2.imread(agent["filename"], cv2.IMREAD_UNCHANGED)
        agent_img = cv2.resize(agent_img, (56, 28),
                               interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(f"./images/agents_resize/{agent['id']}.png", agent_img)



def resize_chars():
    with open("./chars.json") as file:
        agents = json.loads(file.read())

    for agent in agents:
        agent_img = cv2.imread(agent["filename"], cv2.IMREAD_UNCHANGED)
        width = int (agent_img.shape[1] * 0.15)
        height = int (agent_img.shape[0] * 0.14)
        size = (width, height)
        agent_img = cv2.resize(agent_img, size, interpolation=cv2.INTER_AREA)
        _, agent_img = cv2.threshold(agent_img, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f"./chars_resize/{agent['id']}.png", agent_img)

def flip_weapons():
    with open("./weapons.json") as file:
        agents = json.loads(file.read())

    for agent in agents:
        agent_img = cv2.imread(agent["filename"], cv2.IMREAD_GRAYSCALE)
        agent_img = cv2.flip(agent_img, 1)
        _, threshold = cv2.threshold(agent_img, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f"./images/weapons_resize/{agent['id']}.png", threshold)

flip_weapons()