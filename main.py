import cv2
import time
from numpy.typing import NDArray

from get_chars import sort_components_by_left

from src.services.kill_attributes import KillAttributes
from src.services.agent import AgentService
from src.services.player import PlayerService
from src.services.weapon import WeaponService

RED_CARD = (86, 91, 240)
YELLOW_CARD = (119,231,236)

CARD_COLOR_ERROR = 2

AGENT_IMAGE_WIDTH = 56

class Main:
    agent_service = AgentService()
    weapon_service = WeaponService()
    player_service = PlayerService()

    def get_card_info(self, card: NDArray):
        width = card.shape[1]
        height = card.shape[0]

        agent_killer_img = card[:height,:AGENT_IMAGE_WIDTH+1]
        agent_killed_img = card[:height,width-AGENT_IMAGE_WIDTH:width]

        #cv2.imshow("Kill Log", card)

        #cv2.imshow("Agent Killer", agent_killer_img)
        #cv2.imshow("Agent Killed", agent_killed_img)

        cv2.waitKey()

        card_threshold, stats = self._get_stats_from_card(card)

        #cv2.imshow("Card Threshold", card_threshold)

        player_killer_name_chars_stats = stats[0]
        player_killed_name_chars_stats = stats[-1]

        player_killer = self._get_player_info(card_threshold, agent_killer_img, player_killer_name_chars_stats) 
        player_killed = self._get_player_info(card_threshold, agent_killed_img, player_killed_name_chars_stats) 
        weapon_name = self._get_weapon_name(card_threshold, stats)
        kill_attributes = self._get_kill_attributes_from_stats(stats)

        return {
            "player_killer": player_killer,
            "player_killed": player_killed,
            "weapon_name": weapon_name,
            "kill_attributes": kill_attributes
        }

    def _separate_stats(self, stats):
        separated_stats = []
        current_stats = []

        for i in range(2, len(stats)):
            current_stats.append(stats[i-1])
            current_x = stats[i][cv2.CC_STAT_LEFT] 
            last_x = stats[i-1][cv2.CC_STAT_LEFT] + stats[i-1][cv2.CC_STAT_WIDTH] 
            if current_x - last_x >= 23:
                separated_stats.append(current_stats)
                current_stats = []

        current_stats.append(stats[-1])
        separated_stats.append(current_stats)

        return separated_stats

    def _get_weapon_name(self, card_threshold, stats):
        weapon_image = self._get_image_from_stat(card_threshold, stats[1][0])
        return self.weapon_service.get_weapon_name(weapon_image)

    def _get_kill_attributes_from_stats(self, stats):
        kill_attributes_stats = []

        for i in range(2, len(stats)-1):
            kill_attributes_stats.append(stats[i])

        return KillAttributes.get_kill_attributes_from_stats(kill_attributes_stats)

    def _get_player_info(self, card_threshold, agent_img, player_name_chars_stats):
    
        player_info = {
            "nickname": "",
            "agent_name": ""
        }

        player_chars_images = self._get_chars_from_stats(card_threshold, player_name_chars_stats)
        player_info["agent_name"] = self.agent_service.get_agent_name(agent_img)
        player_info["nickname"] = self.player_service.get_player_name(player_chars_images)

        return player_info

    def _get_stats_from_card(self, card):
        width = card.shape[1]
        height = card.shape[0]

        card_crop = card[:height, AGENT_IMAGE_WIDTH: width-AGENT_IMAGE_WIDTH]

        card_crop_gray = cv2.cvtColor(card_crop, cv2.COLOR_BGR2GRAY) 

        width = card_crop_gray.shape[1] * 3
        height = card_crop_gray.shape[0] * 3
        size = (width, height)

        card_crop_gray = cv2.resize(card_crop_gray, size, interpolation=cv2.INTER_AREA)

        _, card_crop_threshold = cv2.threshold(card_crop_gray, 210, 255, cv2.THRESH_BINARY)

        _, _,  stats, _ = cv2.connectedComponentsWithStats(card_crop_threshold)
        stats = sort_components_by_left(stats)
        separated_stats = self._separate_stats(stats)

        return card_crop_threshold, separated_stats

    def _merge_near_chars_components(self, stats, dist_x, dist_y):
        i = 1

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

    def _get_chars_from_stats(self, threshold, stats):
        self._merge_near_chars_components(stats, 0, 6)
        
        return self._get_images_from_stats(threshold, stats)
        
        
    def _get_images_from_stats(self, threshold, stats):
        images = []
        for stat in stats:
            images.append(self._get_image_from_stat(threshold, stat))
            
        cv2.waitKey()
        return images

    def _get_image_from_stat(self, threshold, stat):
        x = stat[cv2.CC_STAT_LEFT]
        y = stat[cv2.CC_STAT_TOP]
        w = stat[cv2.CC_STAT_WIDTH]
        h = stat[cv2.CC_STAT_HEIGHT]

        #cv2.imshow(f"{time.time()}", threshold[y:y+h, x:x+w])

        return threshold[y:y+h, x:x+w]

def main():

    instance = Main()

    for i in range(1, 15):
        start = time.time()
        img = cv2.imread(f"./game_samples/{i}.png")
        info = instance.get_card_info(img)
        print(info)
        end = time.time()
        print(end - start)

if __name__ == "__main__":
    main()
