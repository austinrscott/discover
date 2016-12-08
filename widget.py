import pygame
from pygame.locals import *
from RandomTextMap import RandomTextMap
from random import randint


class Widget():
    def __init__(self, rect):
        self._rect = pygame.Rect(rect)
        self._dirty = True

    def _init_surface(self):
        self._surface = pygame.Surface(self._rect.size, SRCALPHA).convert_alpha()

    def render(self):
        pass

    def event(self, e):
        pass

    def is_dirty(self):
        return self._dirty

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
        self._dirty = True

    def event(self, e):
        e.pos = self._event_get_new_pos(e.pos)
        for widget in self._widgets:
            widget.event(e)

    def is_dirty(self):
        for widget in self._widgets:
            if widget.is_dirty():
                widget.render()
                self._dirty = True
        return self._dirty

    def render(self):
        if self.is_dirty():
            self._init_surface()
            for widget in self._widgets:
                self._surface.blit(widget.get_surface(), widget.get_rect())
            self._dirty = False


class MapWidget(ContainerWidget):
    def __init__(self, pos=(0, 0)):
        # Initialize map variables and the map model
        self._tile_size = 4
        self._grid_size = [140, 140]
        self._map_obj = RandomTextMap(width=self._grid_size[0],
                                      height=self._grid_size[1],
                                      water_chance=0.01,
                                      num_island_seeds=40,
                                      land_water_ratio=0.4)

        # Create MapWidget's Rect (via the superclass's constructor)
        map_path = self._map_obj.water_route_to(0, 0, self._grid_size[1] - 1, self._grid_size[0] - 1)
        while not map_path:
            map_path = self._map_obj.water_route_to(randint(0, self._grid_size[1] - 1),
                                                    randint(0, self._grid_size[0] - 1),
                                                    randint(0, self._grid_size[1] - 1),
                                                    randint(0, self._grid_size[0] - 1))
        test_object = MapPath(map_path,
                              self._tile_size)
        super().__init__((pos, self._get_map_size()), test_object)

    def event(self, e):
        if e.type == MOUSEBUTTONDOWN and e.button == 1 and self._rect.collidepoint(e.pos):
            e.pos = self._event_get_new_pos(e.pos)
            cell_clicked = self._find_cell(e.pos)
            for widget in self._widgets:
                widget.move(cell_clicked)

    def _find_cell(self, pos):
        x, y = pos[0], pos[1]
        return [x // self._tile_size, y // self._tile_size]

    def _get_map_size(self):
        return self._grid_size[0] * self._tile_size, self._grid_size[1] * self._tile_size

    def _init_surface(self):
        print("Rendered map")
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
        self._map_pos = map_pos
        self.render()
        super().__init__(self._surface.get_rect())
        self.move(map_pos)

    def move(self, to_pos):
        self._rect.move_ip(to_pos[0] * self._tile_size - self._rect.left,
                           to_pos[1] * self._tile_size - self._rect.top)
        self._dirty = True

    def render(self):
        self._surface = pygame.Surface((self._tile_size, self._tile_size), SRCALPHA).convert_alpha()
        pygame.draw.circle(self._surface, self._color, self._surface.get_rect().center, self._tile_size // 2)
        self._dirty = False


class MapPath(MapEntity):
    """
    A path between two cells on a map, given by an ordered list of coordinates (the 0th element being a tuple of
    the coordinates in the path)
    """

    def __init__(self, path, tile_size, color=(255, 255, 255, 64)):
        self._path = path
        super().__init__((min(x for (y, x) in path), min(y for (y, x) in path)), tile_size, color)

    def render(self):
        width_in_tiles = abs(min(x for (y, x) in self._path) - max(x for (y, x) in self._path)) + 1
        height_in_tiles = abs(min(y for (y, x) in self._path) - max(y for (y, x) in self._path)) + 1
        self._surface = pygame.Surface((self._tile_size * width_in_tiles,
                                        self._tile_size * height_in_tiles),
                                       SRCALPHA).convert_alpha()
        for (y, x) in self._path:
            # For the purposes of rendering, the top left corner of this surface counts as (0, 0)
            relative_x, relative_y = x - self._map_pos[0], y - self._map_pos[1]
            pygame.draw.rect(self._surface,
                             self._color,
                             pygame.Rect(relative_x * self._tile_size,
                                         relative_y * self._tile_size,
                                         self._tile_size,
                                         self._tile_size))
        self._dirty = False

class Button(Widget):
    # TODO: Add some formatting to button (space between text and border)
    # TODO: Add more complex functionality with button (left, right click)
    # TODO: Add responsiveness to button (change color upon click)
    def __init__(self, pos, text="Button", onclick=None):
        self.font = pygame.font.SysFont("Arial", 24)
        self._rect = (pos, self.font.size(text))
        self._text = text
        if onclick:
            self._onclick_func = onclick
        super().__init__(self._rect)

    def _onclick_func(self):
        print("Button {} has been clicked.".format(self._text))

    def _onclick(self):
        self._onclick_func()

    def _init_surface(self):
        self._surface = self.font.render(self._text, True, (255,255,255))

    def render(self):
        self._init_surface()
        pygame.draw.rect(self._surface, (255,255,255), self._surface.get_rect(), 2)

    def event(self, e):
        if self._rect.collidepoint(e.pos):
            self._onclick()

