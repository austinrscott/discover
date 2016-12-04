import pygame
from pygame.locals import *
from RandomTextMap import RandomTextMap


class Widget():
    def __init__(self, rect):
        self._rect = pygame.Rect(rect)

    def _init_surface(self):
        self._surface = pygame.Surface(self._rect.size).convert_alpha()

    def render(self):
        pass

    def event(self, e):
        pass

    def get_rect(self):
        return self._rect

    def get_surface(self):
        return self._surface

    def _event_get_new_pos(self, pos):
        new_pos = [pos[0] - self._rect.left, pos[1] - self._rect.top]
        return new_pos


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
        self._init_surface()
        for widget in self._widgets:
            widget.render()
            self._surface.blit(widget.get_surface(), widget.get_rect())


class MapWidget(ContainerWidget):
    def __init__(self, pos=(0, 0)):
        # Initialize map variables and the map model
        self._tile_size = 8
        self._grid_size = [70, 70]
        self._map_obj = RandomTextMap(width=self._grid_size[0],
                                      height=self._grid_size[1],
                                      water_chance=0.01,
                                      num_island_seeds=40,
                                      land_water_ratio=0.4)

        # Create MapWidget's Rect (via the superclass's constructor)
        super().__init__((pos, self._get_map_size()), MapEntity((15, 15), tile_size=self._tile_size))

    def event(self, e):
        if e.type == MOUSEBUTTONDOWN and e.button == 1 and self._rect.collidepoint(e.pos):
            e.pos = self._event_get_new_pos(e.pos)
            cell_clicked = self._find_cell(e.pos)
            print(cell_clicked)

    def _find_cell(self, pos):
        x, y = pos[0], pos[1]
        return [x // self._tile_size, y // self._tile_size]

    def _get_map_size(self):
        return self._grid_size[0] * self._tile_size, self._grid_size[1] * self._tile_size

    def _init_surface(self):
        super()._init_surface()
        matrix = self._map_obj.output_map()
        self._surface.fill((25, 25, 125))
        for y in range(self._grid_size[1]):
            for x in range(self._grid_size[0]):
                if matrix[y][x] == '#':
                    self._surface.fill((25, 125, 25),
                                       (x * self._tile_size, y * self._tile_size, self._tile_size, self._tile_size))


class MapEntity(Widget):
    """
    Something that exists on the map besides a tile. Ship, port, et cetera.
    """

    def __init__(self, map_pos, tile_size, color=(255, 255, 255)):
        self._tile_size = tile_size
        self._color = color
        self.render()
        super().__init__(self._surface.get_rect())
        self.move(map_pos)

    def move(self, to_pos):
        self._rect.move_ip(to_pos[0] * self._tile_size, to_pos[1] * self._tile_size)

    def render(self):
        self._surface = pygame.Surface((self._tile_size, self._tile_size)).convert_alpha()
        pygame.draw.circle(self._surface, self._color, self._surface.get_rect().center, self._tile_size // 2)
