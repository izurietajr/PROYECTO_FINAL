#!/usr/bin/env python3
import matplotlib.image as img
from PIL import Image as pil_image
from functools import reduce
import numpy as np


class Image:

    def __init__(self):
        self.route = "."
        self.image = None
        self.array = None
        self.height, self.width, self.dat = (0,0,0)

    def load_file(self, route):
        self.route = route
        self.image = img.imread(route)
        self.array = self.image.tolist()
        self.height, self.width, self.dat = self.image.shape

    def load_array(self, array):
        self.array = array
        self.height = len(array)
        self.width = len(array[0])

    def I(self, x, y):
        return tuple(self.array[x][y])

    def I_m(self, x, y, color=0):
        triple = self.array[x][y]
        return triple[color]

    def I_normal(self, x, y):
        triple = self.array[x][y][color]
        return self.array[x][y]

    def show(self, route=None):
        if route:
            self.route = route
        image_arr = np.asarray(self.array, dtype="uint8")
        img_file = pil_image.fromarray(image_arr, 'RGB')

        return img_file

    def iterator(self):
        for i in range(self.height):
            for j in range(self.width):
                yield (i,j)

    def map_over(self, func):
        for x, y in self.iterator():
            self.array[x][y] = func(*self.I(x, y))
