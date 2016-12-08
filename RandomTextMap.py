import sys
from random import random, randrange
from collections import deque


class RandomTextMap:
    def print_map(self):
        for row in self.matrix:
            string = ""
            for cell in row:
                string = string + str(cell)
            print(string)

    def __neighbors_of_cell(self, h, w):
        if h > 0 and self.matrix[h - 1][w] != '#':
            yield (h - 1, w)
        if h < self.height - 1 and self.matrix[h + 1][w] != '#':
            yield (h + 1, w)
        if w > 0 and self.matrix[h][w - 1] != '#':
            yield (h, w - 1)
        if w < self.width - 1 and self.matrix[h][w + 1] != '#':
            yield (h, w + 1)

    # from y1,x1 to y2,x2
    def water_route_to(self, y1, x1, y2, x2):
        search_queue = deque()

        if self.matrix[y1][x1] != '~':
            return None

        search_queue.append((y1, x1))
        visited = [[None for y in range(len(self.matrix))] for x in range(len(self.matrix[0]))]
        visited[y1][x1] = (-1, -1)

        while search_queue:
            (y, x) = search_queue.popleft()
            if (y, x) == (y2, x2):
                break

            for (n_y, n_x) in self.__neighbors_of_cell(y, x):
                if self.matrix[n_y][n_x] == '~':
                    if not visited[n_y][n_x]:
                        visited[n_y][n_x] = (y, x)
                        search_queue.append((n_y, n_x))

        if visited[y2][x2] is None:
            return None

        path = deque()
        (cur_y, cur_x) = (y2, x2)
        path.appendleft((y2, x2))

        while (cur_y, cur_x) != (-1, -1):
            path.appendleft(visited[cur_y][cur_x])
            (cur_y, cur_x) = visited[cur_y][cur_x]

        return list(path)[1:]

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

        # self.print_map()
        # print
        # print
        land = num_island_seeds
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

#
# _map_obj = RandomTextMap(width=100,
#                               height=100,
#                               water_chance=0.01,
#                               num_island_seeds=40,
#                               land_water_ratio=0.4)
#
# _map_obj.print_map()
#
# print(_map_obj.water_route_to(0,0,5,80))
# print("hello")
