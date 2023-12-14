import json
import sys

import cv2

from .image_moments import ImageMoments

class WeaponService:
    WEAPONS_JSON = "./weapons.json"

    def __init__(self) -> None:
        self._weapons = self._get_weapons_info()
    
    def _get_weapons_info(self):
        with open(self.WEAPONS_JSON) as file:
            weapons = json.loads(file.read())
            
        for weapon in weapons:
            weapon_img = cv2.imread(weapon["filename"], cv2.IMREAD_GRAYSCALE)
            weapon["moments"] = ImageMoments.get_central_normalized_moments(weapon_img)

        return weapons
    
    def get_weapon_name(self, img):
        min_score = sys.maxsize
        min_score_char = None

        weapon_moments = ImageMoments.get_central_normalized_moments(img)

        for weapon in self._weapons: 
            score = ImageMoments.get_shape_distance(weapon["moments"], weapon_moments)

            if score < min_score:
                min_score = score
                min_score_char = weapon

        return min_score_char["name"]