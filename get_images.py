import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

import urllib.parse
import urllib.request

import requests

AGENTS_VALORANT_FILES_URL = "https://valorantfiles.com/agents"
AGENT_CARD_SELECTOR = ".card-img-top"
AGENT_CARD_IMAGE_NAME = "killfeedportrait.png"
AGENTS_IMAGES_PATH = "./images/agents"

WEAPONS_VALORANT_FILES_URL = "https://valorantfiles.com/weapons"
WEAPON_CARD_SELECTOR = ".card-img-top"
WEAPON_CARD_IMAGE_NAME = "killstreamicon.png"
WEAPONS_IMAGES_PATH = "./images/weapons"


def close_current_tab(driver: webdriver.Chrome):
    driver.get("about:blank")


def save_file(url: str, filename: str):
    request = requests.get(url, stream=True)

    with open(filename, "wb") as file:
        for chunk in request.iter_content():
            file.write(chunk)


def get_agents(driver: webdriver.Chrome):
    driver.get(AGENTS_VALORANT_FILES_URL)

    agent_cards = driver.find_elements(By.CSS_SELECTOR, AGENT_CARD_SELECTOR)
    agents = []

    for agent_card in agent_cards:
        url = urllib.parse.urlparse(agent_card.get_attribute("src"))
        path = url.path.split("/")

        path.pop()
        path.append(AGENT_CARD_IMAGE_NAME)

        url_parts = list(url)
        url_parts[url._fields.index("path")] = "/".join(path)

        agent_name = agent_card.get_attribute("title")
        agent_card_url = urllib.parse.urlunparse(url_parts)

        agents.append({
            "id": path[3],
            "name": agent_name,
            "url": agent_card_url
        })

    close_current_tab(driver)

    for agent in agents:
        agent["filename"] = f"{AGENTS_IMAGES_PATH}/{agent['id']}.png"

        print(agent)
        save_file(agent["url"], agent["filename"])

    with open("./agents.json", "w+") as file:
        file.write(json.dumps(agents, indent=4))


def get_weapons(driver: webdriver.Chrome):
    driver.get(WEAPONS_VALORANT_FILES_URL)

    weapons_cards = driver.find_elements(By.CSS_SELECTOR, WEAPON_CARD_SELECTOR)
    weapons = []

    for weapon_card in weapons_cards:
        url = urllib.parse.urlparse(weapon_card.get_attribute("src"))
        path = url.path.split("/")

        path.pop()
        path.append(WEAPON_CARD_IMAGE_NAME)

        url_parts = list(url)
        url_parts[url._fields.index("path")] = "/".join(path)

        weapon_name = weapon_card.get_attribute("title")
        weapon_card_url = urllib.parse.urlunparse(url_parts)

        weapons.append({
            "id": path[3],
            "name": weapon_name,
            "url": weapon_card_url
        })

    close_current_tab(driver)

    for weapon in weapons:
        weapon["filename"] = f"{WEAPONS_IMAGES_PATH}/{weapon['id']}.png"

        print(weapon)
        save_file(weapon["url"], weapon["filename"])

    with open("./weapons.json", "w+") as file:
        file.write(json.dumps(weapons, indent=4))


def main():
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": "./images/agents"
    }

    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(2)

    get_agents(driver)
    get_weapons(driver)


if __name__ == "__main__":
    main()
