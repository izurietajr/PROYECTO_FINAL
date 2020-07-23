#!/usr/bin/env python3
import matplotlib.image as plt_img
import numpy as np
from PIL import Image as pil_image
from functools import reduce
from math import sqrt


class Image:

    def __init__(self):
        self.route = "."
        self.image = None
        self.array = None
        self.height, self.width, self.dat = (0,0,0)

    def load_file(self, route):
        self.route = route
        self.image = plt_img.imread(route)
        self.array = self.image.tolist()
        self.height, self.width, self.dat = self.image.shape

    def load_array(self, array):
        self.array = array
        self.height = len(array)
        self.width = len(array[0])

    def I(self, x, y):
        """ Devuelve rgb en x, y """
        return tuple(self.array[x][y])

    def I_m(self, x, y, color=0):
        """ Devuelve un color de x, y """
        triple = self.array[x][y]
        return triple[color]

    def I_normal(self, x, y):
        """ Devuelve rgb en [0, 1] """
        (i, j, k) = self.I(x, y)
        return (i/255, j/255, k/255)

    def I_mnormal(self, x, y, color=0):
        """ Devuelve color en [0, 1] """
        i = self.I_m(x, y, color)
        return i/255

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
        """ Ejecución de func sobre cada pixel """
        for x, y in self.iterator():
            self.array[x][y] = func(*self.I(x, y))


    def hu_moments(self):

        def moment_pq(p, q):
            """ Momentos geométricos """
            sum = 0
            for x, y in self.iterator():
                sum += x**p * y**q * self.I_mnormal(x, y)
            return sum

        m00 = moment_pq(0, 0)
        m01 = moment_pq(0, 1)
        m11 = moment_pq(1, 1)
        m10 = moment_pq(1, 0)
        m20 = moment_pq(2, 0)
        m02 = moment_pq(0, 2)

        def central_moment_20(a, b, c):
            """ Momentos centrales """
            return (a-(b**2/c))/(c**2)

        n20 = central_moment_20(m20, m10, m00)
        n02 = central_moment_20(m02, m01, m00)
        n11 = central_moment_20(m11, sqrt(m10*m01), m00)

        self.X, self.Y = (n20+n02, (n20-n02)**2+4*(n11**2))

        return (self.X, self.Y)
