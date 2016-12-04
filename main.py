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
    root.add(Map(pos=[25, 25]))

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                root.event(event)
        root.render()
        screen.blit(root.get_surface(), (0, 0))
        pygame.display.flip()


class Widget():
    def __init__(self, rect):
        self._rect = pygame.Rect(rect)

    def event(self, e):
        pass

    def get_rect(self):
        return self._rect

    def get_surface(self):
        return self._surface

    def _event_get_new_pos(self, pos):
        new_pos = [pos[0] - self._rect.left, pos[1] - self._rect.top]
        return new_pos

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
        e.pos = self._event_get_new_pos(e.pos)
        for widget in self._widgets:
            widget.event(e)

    def render(self):
        self._surface = pygame.Surface((self._rect.width, self._rect.height))
        for widget in self._widgets:
            widget.render()
            self._surface.blit(widget.get_surface(), widget.get_rect())


class Map(Widget):
    def __init__(self, rect=None, pos=None):
        self._tile_size = 8
        self._grid_size = [70, 70]
        self._map_obj = RandomTextMap(width=self._grid_size[0],
                                      height=self._grid_size[1],
                                      water_chance=0.01,
                                      num_island_seeds=40,
                                      land_water_ratio=0.4)
        self._create_map_surface()
        new_rect = self._surface.get_rect()
        if pos:
            new_rect.move_ip(pos[0], pos[1])
        super().__init__(new_rect)
        self.render()


    def event(self, e):
        if e.type == MOUSEBUTTONDOWN and e.button == 1 and self._rect.collidepoint(e.pos):
            e.pos = self._event_get_new_pos(e.pos)
            cell_clicked = self._find_cell(e.pos)
            print(cell_clicked)

    def _find_cell(self, pos):
        x, y = pos[0], pos[1]
        return [x // self._tile_size, y // self._tile_size]

    def _create_map_surface(self):
        self._surface = pygame.Surface((self._grid_size[0] * self._tile_size, self._grid_size[1] * self._tile_size))

    def render(self):
        matrix = self._map_obj.output_map()
        self._surface.fill((25, 25, 125))
        for y in range(self._grid_size[1]):
            for x in range(self._grid_size[0]):
                if matrix[y][x] == '#':
                    self._surface.fill((25, 125, 25),
                                     (x * self._tile_size, y * self._tile_size, self._tile_size, self._tile_size))


if __name__ == '__main__':
    main()
