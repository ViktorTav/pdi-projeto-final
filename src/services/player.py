import json
import sys

import cv2
from .image_moments import ImageMoments


class PlayerService:
    CHARS_JSON = "./chars.json"

    def __init__(self) -> None:
        self._chars = self._get_chars_info()

    def _get_chars_info(self):
        with open(self.CHARS_JSON) as file:
            chars = json.loads(file.read())
            
        for char in chars:
            char_img = cv2.imread(char["filename"], cv2.IMREAD_GRAYSCALE)
            char["moments"] = ImageMoments.get_central_normalized_moments(char_img)

        return chars
    
    def get_player_name(self, chars): 
        name = ""

        for char in chars:
            name+= self._get_char(char)

        cv2.waitKey()

        return name


    def _get_char(self, char):
        min_score = sys.maxsize
        min_score_char = None

        char_moments = ImageMoments.get_central_normalized_moments(char)

        # cv2.imshow(f"{time.time()}", char)
        # cv2.waitKey()

        for char_info in self._chars: 
            score = ImageMoments.get_shape_distance(char_info["moments"], char_moments)

            if score < min_score:
                min_score = score
                min_score_char = char_info

        return min_score_char["char"]