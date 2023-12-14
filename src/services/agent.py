import json
import sys
import time
import cv2

from .image_moments import ImageMoments 
from .histogram import Histogram

class AgentService:

    AGENTS_JSON = "./agents.json"

    def __init__(self) -> None:
        self._agents = self._get_agents_info()

    def _get_agents_info(self):
        with open(self.AGENTS_JSON) as file:
            agents = json.loads(file.read())
            
        for agent in agents:
            agent_img = cv2.imread(agent["filename"], cv2.IMREAD_UNCHANGED)
            agent["histogram"] = Histogram.create_3d_histogram(agent_img)

        return agents

    def get_agent_name(self, img):
        max_score = -1
        max_score_agent = None

        img_histogram = Histogram.create_3d_histogram(img)
        for agent in self._agents:
            score = Histogram.compare_3d_histograms(img_histogram, agent["histogram"])

            if score > max_score:
                max_score = score
                max_score_agent = agent

        return max_score_agent["name"]
    
