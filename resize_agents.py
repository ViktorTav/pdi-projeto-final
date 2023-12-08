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
