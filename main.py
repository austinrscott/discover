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

    # Initialize root widget
    root = ContainerWidget(screen.get_rect())

    # Initialize map
    root.add(Map())

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit()
        root.render()
        screen.blit(root.get_surface(), (0, 0))
        pygame.display.flip()


class Widget():
    def __init__(self, rect):
        self._rect = pygame.Rect(rect)
        self._surface = None

    def event(self, e):
        pass

    def get_rect(self):
        return self._rect

    def get_surface(self):
        return self._surface

    def render(self):
        pass


class ContainerWidget(Widget):
    def __init__(self, rect, *widgets):
        super().__init__(rect)
        self._widgets = []
        if widgets:
            for widget in widgets:
                self.add(widget)
        self.render()

    def add(self, widget):
        self._widgets.append(widget)

    def event(self, e):
        pass

    def render(self):
        self._surface = pygame.Surface((self._rect.width, self._rect.height))
        for widget in self._widgets:
            widget.render()
            self._surface.blit(widget.get_surface(), widget.get_rect())

class Map(Widget):
    def __init__(self, rect=None):
        self._map_obj = RandomTextMap(width=145,
                                      height=145,
                                      water_chance=0.01,
                                      num_island_seeds=40,
                                      land_water_ratio=0.4)
        self.render()
        super().__init__(self._surface.get_rect())

    def render(self):
        matrix = self._map_obj.output_map()
        grid_x, grid_y = len(matrix), len(matrix[0])
        tile_size = 4
        new_surface = pygame.Surface((grid_x * tile_size, grid_y * tile_size))
        new_surface.fill((25, 25, 125))
        for y in range(grid_y):
            for x in range(grid_x):
                if matrix[y][x] == '#':
                    new_surface.fill((25, 125, 25), (x * tile_size, y * tile_size, tile_size, tile_size))
        self._surface = new_surface


if __name__ == '__main__':
    main()
