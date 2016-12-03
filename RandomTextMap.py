import sys
from random import random, randrange
from collections import deque
class RandomTextMap:

    def print_map(self):
        for row in self.matrix:
            for cell in row:
                sys.stdout.write(str(cell))

            print

    def __add_water_neighbor_to_queue(self, h, w, deque):
        if h > 0 and self.matrix[h-1][w] != '#':
            deque.append((h - 1, w))
        if h < self.height - 1 and self.matrix[h+1][w] != '#':
            deque.append((h + 1, w))
        if w > 0 and self.matrix[h][w-1] != '#':
            deque.append((h, w - 1))
        if w < self.width - 1 and self.matrix[h][w+1] != '#':
            deque.append((h, w + 1))

    def __init__(self, width, height, water_chance, num_island_seeds, land_water_ratio):
        self.matrix = [['~' for x in range(width)] for y in range(height)]
        self.height = height
        self.width = width

        height_seeds = [randrange(0, height) for i in xrange(num_island_seeds)]
        width_seeds = [randrange(0, width) for i in xrange(num_island_seeds)]
        seeds = zip(height_seeds, width_seeds)

        coast = deque()
        for (h, w) in seeds:
            self.matrix[h][w] = '#'
            self.__add_water_neighbor_to_queue(h,w, coast)

        # self.print_map()
        # print
        # print
        land = 8
        while coast:
            (h, w) = coast.popleft()
            if self.matrix[h][w] == '#':
                continue

            if (random() < water_chance):
                self.matrix[h][w] = '#'
                self.__add_water_neighbor_to_queue(h,w, coast)
                land += 1
                if (land/land_water_ratio >= self.height * self.width):
                    break
            else:
                coast.append((h, w))


        self.print_map()


random_map = RandomTextMap(height=100,width=100, water_chance=.3, num_island_seeds=8, land_water_ratio=.3)


