import math
import cv2
import numpy as np

class ImageMoments:
    
    @staticmethod
    def get_central_normalized_moments(img):
        moments = cv2.moments(img)

        central_normalized_moments = np.array([
            moments['nu20'],
            moments['nu11'],
            moments['nu02'],
            moments['nu30'],
            moments['nu21'],
            moments['nu12'],
            moments['nu03']
        ])

        return central_normalized_moments
    
    @staticmethod
    def get_shape_distance(moments1, moments2):
        distance = 0

        for i in range(len(moments1)):
            distance += math.fabs(moments2[i] - moments1[i])

        return distance
