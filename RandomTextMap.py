import sys
from random import random, randrange
from collections import deque

            def print_map(self):
                for row in self.matrix:
                    string = ""
                    for cell in row:
                        string = string + str(cell)
                    print(string)

            def __add_water_neighbor_to_queue(self, h, w, deque):
                if h > 0 and self.matrix[h - 1][w] != '#':
                    deque.append((h - 1, w))
                if h < self.height - 1 and self.matrix[h + 1][w] != '#':
                    deque.append((h + 1, w))
                if w > 0 and self.matrix[h][w - 1] != '#':
                    deque.append((h, w - 1))
                if w < self.width - 1 and self.matrix[h][w + 1] != '#':
                    deque.append((h, w + 1))

            def __init__(self, width, height, water_chance, num_island_seeds, land_water_ratio):
                self.matrix = [['~' for x in range(width)] for y in range(height)]
                self.height = height
                self.width = width

                height_seeds = [randrange(0, height) for i in range(num_island_seeds)]
                width_seeds = [randrange(0, width) for i in range(num_island_seeds)]
                seeds = zip(height_seeds, width_seeds)

                coast = deque()
                for (h, w) in seeds:
                    self.matrix[h][w] = '#'
                    self.__add_water_neighbor_to_queue(h, w, coast)

                land = 8
                while coast:
                    (h, w) = coast.popleft()
                    if self.matrix[h][w] == '#':
                        continue

                    if (random() < water_chance):
                        self.matrix[h][w] = '#'
                        self.__add_water_neighbor_to_queue(h, w, coast)
                        land += 1
                        if (land / land_water_ratio >= self.height * self.width):
                            break
                    else:
                        coast.append((h, w))

            def output_map(self):
                return self.matrix


            def find_path(self, starting_path, end):
        # TODO: Install pathfinding algorithm
        # Starting_path is any part of the path that has been discovered.
        # Find neighboring cells to the last cell of starting_path
        # If one of the neighboring cells is end, add it to the path and return the whole path
        # Otherwise, add the cell to the path which is most likely to lead to end, and run find_path on that.
