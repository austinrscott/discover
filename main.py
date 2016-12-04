#!/usr/bin/python

# Import pygame
import pygame
from pygame.locals import *

# Import map class
from RandomTextMap import RandomTextMap


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Discover')

    # Initialize map
    map_obj = RandomTextMap(height=100, width=100, water_chance=.3, num_island_seeds=50, land_water_ratio=.3)
    map_obj.print_map()

    # Render map
    map_surface = render_map(map_obj)

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit()
        screen.blit(map_surface, (0, 0))
        pygame.display.flip()


class Widget():
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)

    def onclick(self):
        pass

    def event(self, e):
        pass

    def render(self):
        pass


class Container(Widget):
    def __init__(self, rect, *widgets):
        super().__init__(rect)
        self._widgets = []
        if widgets:
            for widget in widgets:
                self.add(widget)
        self.render()

    def add(self, widget):
        self._widgets.append(widget)


def render_map(map_object):
    matrix = map_object.output_map()
    grid_x, grid_y = len(matrix), len(matrix[0])
    tile_size = 3
    new_surface = pygame.Surface((grid_x * tile_size, grid_y * tile_size))
    new_surface.fill((25, 25, 125))
    for y in range(grid_y):
        for x in range(grid_x):
            if matrix[y][x] == '#':
                new_surface.fill((25, 125, 25), (x * tile_size, y * tile_size, tile_size, tile_size))
    return new_surface


if __name__ == '__main__':
    main()
