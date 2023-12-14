import numpy as np


class Histogram:
    HISTOGRAM_3D_BINS = 8

    @staticmethod
    def create_3d_histogram(img, bins = None):
        bins = bins or Histogram.HISTOGRAM_3D_BINS

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

    @staticmethod
    def compare_3d_histograms(histogram1, histogram2):
        bins = histogram1.shape[0]

        score = 0

        # Aqui fazermos a comparação do histograma por método de intersecção.

        for x in range(bins):
            for y in range(bins):
                for z in range(bins):
                    score += min(histogram1[x]
                                [y][z], histogram2[x][y][z])

        return score