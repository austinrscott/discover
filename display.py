#!/usr/bin/python

import pygame
from pygame.locals import *

# from RandomTextMap import RandomTextMap
# from random import randint
# from event import GAMEEVENT, GameEventType, TickEvent, MapGeneratedEvent
#
#
# class Widget():
#     def __init__(self, rect):
#         self._rect = pygame.Rect(rect)
#         self.dirty = True
#
#     def _init_surface(self):
#         self._surface = pygame.Surface(self._rect.size, SRCALPHA).convert_alpha()
#
#     def render(self):
#         pass
#
#     def event(self, e):
#         pass
#
#     def isdirty(self):
#         return self.dirty
#
#     def get_rect(self):
#         return self._rect
#
#     def get_surface(self):
#         return self._surface
#
#     def _event_get_new_pos(self, pos):
#         new_pos = [pos[0] - self._rect.left, pos[1] - self._rect.top]
#         return new_pos
#
#
# class ContainerWidget(Widget):
#     def __init__(self, rect, *widgets):
#         super().__init__(rect)
#         self._widgets = []
#         if widgets:
#             for widget in widgets:
#                 self.add(widget)
#         self.render()
#
#     def add(self, widget):
#         self._widgets.append(widget)
#         self.dirty = True
#
#     def event(self, e):
#         e.pos = self._event_get_new_pos(e.pos)
#         for widget in self._widgets:
#             widget.event(e)
#
#     def isdirty(self):
#         for widget in self._widgets:
#             if widget.isdirty():
#                 widget.render()
#                 self.dirty = True
#         return self.dirty
#
#     def render(self):
#         if self.isdirty():
#             self._init_surface()
#             for widget in self._widgets:
#                 self._surface.blit(widget.get_surface(), widget.get_rect())
#             self.dirty = False
#
#
# class MapWidget(ContainerWidget):
#     def __init__(self, pos=(0, 0)):
#         # Initialize map variables and the map model
#         self._tile_size = 4
#         self._grid_size = [140, 140]
#         self._map_obj = RandomTextMap(width=self._grid_size[0],
#                                       height=self._grid_size[1],
#                                       water_chance=0.01,
#                                       num_island_seeds=40,
#                                       land_water_ratio=0.4)
#
#         # Create MapWidget's Rect (via the superclass's constructor)
#         map_path = self._map_obj.water_route_to(0, 0, self._grid_size[1] - 1, self._grid_size[0] - 1)
#         while not map_path:
#             map_path = self._map_obj.water_route_to(randint(0, self._grid_size[1] - 1),
#                                                     randint(0, self._grid_size[0] - 1),
#                                                     randint(0, self._grid_size[1] - 1),
#                                                     randint(0, self._grid_size[0] - 1))
#         test_object = MapPath(map_path,
#                               self._tile_size)
#         super().__init__((pos, self._get_map_size()), test_object)
#
#     def event(self, e):
#         if e.type == MOUSEBUTTONDOWN and e.button == 1 and self._rect.collidepoint(e.pos):
#             e.pos = self._event_get_new_pos(e.pos)
#             cell_clicked = self._find_cell(e.pos)
#             for widget in self._widgets:
#                 widget.move(cell_clicked)
#
#     def _find_cell(self, pos):
#         x, y = pos[0], pos[1]
#         return [x // self._tile_size, y // self._tile_size]
#
#     def _get_map_size(self):
#         return self._grid_size[0] * self._tile_size, self._grid_size[1] * self._tile_size
#
#     def _init_surface(self):
#         print("Rendered map")
#         super()._init_surface()
#         matrix = self._map_obj.output_map()
#         self._surface.fill((25, 25, 125))
#         for y in range(self._grid_size[1]):
#             for x in range(self._grid_size[0]):
#                 if matrix[y][x] == '#':
#                     self._surface.fill((25, 125, 25),
#                                        (x * self._tile_size, y * self._tile_size, self._tile_size, self._tile_size))
#
#
# class MapEntity(Widget):
#     """
#     Something that exists on the map besides a tile. Ship, port, et cetera.
#     """
#
#     def __init__(self, map_pos, tile_size, color=(255, 255, 255)):
#         self._tile_size = tile_size
#         self._color = color
#         self._map_pos = map_pos
#         self.render()
#         super().__init__(self._surface.get_rect())
#         self.move(map_pos)
#
#     def move(self, to_pos):
#         self._rect.move_ip(to_pos[0] * self._tile_size - self._rect.left,
#                            to_pos[1] * self._tile_size - self._rect.top)
#         self.dirty = True
#
#     def render(self):
#         self._surface = pygame.Surface((self._tile_size, self._tile_size), SRCALPHA).convert_alpha()
#         pygame.draw.circle(self._surface, self._color, self._surface.get_rect().center, self._tile_size // 2)
#         self.dirty = False
#
#
# class MapPath(MapEntity):
#     """
#     A path between two cells on a map, given by an ordered list of coordinates (the 0th element being a tuple of
#     the coordinates in the path)
#     """
#
#     def __init__(self, path, tile_size, color=(255, 255, 255, 64)):
#         self._path = path
#         super().__init__((min(x for (y, x) in path), min(y for (y, x) in path)), tile_size, color)
#
#     def render(self):
#         width_in_tiles = abs(min(x for (y, x) in self._path) - max(x for (y, x) in self._path)) + 1
#         height_in_tiles = abs(min(y for (y, x) in self._path) - max(y for (y, x) in self._path)) + 1
#         self._surface = pygame.Surface((self._tile_size * width_in_tiles,
#                                         self._tile_size * height_in_tiles),
#                                        SRCALPHA).convert_alpha()
#         for (y, x) in self._path:
#             # For the purposes of rendering, the top left corner of this surface counts as (0, 0)
#             relative_x, relative_y = x - self._map_pos[0], y - self._map_pos[1]
#             pygame.draw.rect(self._surface,
#                              self._color,
#                              pygame.Rect(relative_x * self._tile_size,
#                                          relative_y * self._tile_size,
#                                          self._tile_size,
#                                          self._tile_size))
#         self.dirty = False
#
# class Button(Widget):
#     def __init__(self, pos, text="Button", onclick=None):
#         self.font = pygame.font.SysFont("Arial", 24)
#         self._rect = (pos, self.font.size(text))
#         self._text = text
#         if onclick:
#             self._onclick_func = onclick
#         super().__init__(self._rect)
#
#     def _onclick_func(self):
#         print("Button {} has been clicked.".format(self._text))
#
#     def _onclick(self):
#         self._onclick_func()
#
#     def _init_surface(self):
#         self._surface = self.font.render(self._text, True, (255,255,255))
#
#     def render(self):
#         self._init_surface()
#         pygame.draw.rect(self._surface, (255,255,255), self._surface.get_rect(), 2)
#         self.dirty = True
#
#     def event(self, e):
#         if self._rect.collidepoint(e.pos):
#             self._onclick()
from event import TickEvent, MapGeneratedEvent, MapZoomEvent


class Widget():
    def __init__(self, pos=(0, 0)):
        self.pos = pos
        self.dirty = True

    def _render(self):
        raise NotImplementedError("Function _render not implemented in class {}".format(self.__class__))

    def notify(self):
        raise NotImplementedError("Function notify not implemented in class {}".format(self.__class__))

    @property
    def surface(self):
        if self.dirty:
            self._render()
        return self._surface

    @property
    def size(self):
        if not self._size:
            self._size = self._surface.get_rect().size
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size
        self._needs_new_rect = True

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        self._pos = new_pos
        self._needs_new_rect = True

    @property
    def parent(self):
        # TODO: Maybe this doesn't need it?
        try:
            return self._parent
        except AttributeError:
            return None

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def rect(self):
        if self._needs_new_rect:
            self._rect = pygame.Rect(self.pos, self.size)
        return self._rect

    def move(self, x_offset, y_offset):
        self.pos = (self.pos[0] + x_offset, self.pos[1] + y_offset)

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, boolean):
        if boolean and self.parent:
            self._dirty = True
            self.parent.child_widget_dirty()
        else:
            self._dirty = boolean


class ContainerWidget(Widget):
    """ContainerWidget is a Widget which can combine the graphics of many sub-Widgets into one Surface."""

    def __init__(self, size, pos=(0, 0)):
        self.size = size
        self._widgets = []
        super().__init__(pos=pos)

    def _render(self):
        self._surface = pygame.Surface(self.size, SRCALPHA)
        for widget in self._widgets:
            self._surface.blit(widget.surface, widget.pos)
        self.dirty = False

    def add(self, *new_widgets):
        for new_widget in new_widgets:
            self._widgets.append(new_widget)
            new_widget.parent = self
        self.dirty = True

    def remove(self, widget):
        self._widgets.remove(widget)
        self.dirty = True

    def child_widget_dirty(self):
        self.dirty = True

    def notify(self, event):
        for widget in self._widgets:
            widget.notify(event=event)
            # TODO: Implement hierarchical mouse event detection in widgets


class MapTile(Widget):
    """A single MapTile knows how to draw the proper graphics for each type of landscape. It doesn't know its absolute
    position on the map but it does hold its position in the map grid as X, Y coordinates."""

    def __init__(self, tile_size, pos, type):
        self.tile_size = tile_size
        self._type = type
        super().__init__(pos=pos)

    def _render(self):
        self._surface = pygame.Surface((self.tile_size, self.tile_size), SRCALPHA)
        terrain_color = (255, 0, 255)
        if self._type == 'land':
            terrain_color = (32, 128, 32)
        elif self._type == 'water':
            terrain_color = (32, 32, 128)
        self._surface.fill(terrain_color)
        self.dirty = False

    @property
    def tile_size(self):
        return self._tile_size

    @tile_size.setter
    def tile_size(self, new_tile_size):
        self._tile_size = new_tile_size
        self.dirty = True


class MapWidget(ContainerWidget):
    """
    The MapWidget is responsible for holding all of the layers of the map: tiles, map entities (towns, boats, resources)
    and other overlays suh as fog-of-war.
    """

    # TODO: Make the MapWidget manage all of the tile widgets and render them to a single surface for the ViewportWidget.
    def __init__(self):
        super().__init__(size=(1, 1), pos=(0, 0))
        self._map = None

    def _render(self):
        """Render the master surface."""
        # TODO: Implement management of other layers besides just MapTiles on the map
        self._surface = pygame.Surface(self.size, SRCALPHA)
        for tile in self._widgets:
            x, y = tile.pos[0] * self.tile_size, tile.pos[1] * self.tile_size
            self._surface.blit(tile.surface, (x, y))
        self.dirty = False

    def _populate_map_tiles(self):
        # TODO: Add getters for the map so that this doesn't have to be derived from raw data
        map_width, map_height = len(self._map[0]), len(self._map)
        self.grid_size = (map_width, map_height)
        for y in range(map_height):
            for x in range(map_width):
                terrain = None
                if self._map[y][x] == '#':
                    terrain = 'land'
                elif self._map[y][x] == '~':
                    terrain = 'water'
                new_tile = MapTile(self._tile_size, (x, y), terrain)
                new_tile.parent = self
                self.add(new_tile)
        self._calculate_new_surface_size()

    def _calculate_new_surface_size(self):
        self.size = (self.grid_size[0] * self.tile_size, self.grid_size[1] * self.tile_size)

    def notify(self, event):
        if isinstance(event, MapGeneratedEvent):
            self._map = event.map
            self._populate_map_tiles()
            self.dirty = True

    @property
    def grid_size(self):
        return self._grid_size

    @grid_size.setter
    def grid_size(self, new_grid_size):
        self._grid_size = new_grid_size

    @property
    def tile_size(self):
        return self._tile_size

    @tile_size.setter
    def tile_size(self, new_tile_size):
        self._tile_size = new_tile_size
        # TODO: Find a better way to organize this... if it tries to calculate surface size before the map is initialized, it crashes because there's no grid size
        if self._map:
            self._calculate_new_surface_size()
        for tile in self._widgets:
            tile.tile_size = new_tile_size
        self.dirty = True


class ViewportWidget(ContainerWidget):
    """The ViewportWidget is responsible for viewing only a portion of the full MapWidget main surface, and for
    scrolling the view and initially taking care of zoom requests."""

    def __init__(self, size, pos=(0, 0), view_pos=(0, 0), tile_size=4):
        super().__init__(size=size, pos=pos)
        self.add(MapWidget())
        self.tile_size = tile_size
        self.view_pos = view_pos
        # TODO: Make the ViewportWidget initialize a MapWidget and display only a portion of it.

    def _render(self):
        self._surface = pygame.Surface(self.size, SRCALPHA)
        self._surface.fill((0, 0, 0))
        # Although the "viewport" has a position, it's actually the negative position which gets used for blitting
        actual_view_pos = (-self.view_pos[0], -self.view_pos[1])
        self._surface.blit(self._widgets[0].surface, actual_view_pos)
        self.dirty = False

    @property
    def tile_size(self):
        return self._tile_size

    @tile_size.setter
    def tile_size(self, new_tile_size):
        self._tile_size = new_tile_size
        # TODO: Think of a more elegant way to use the Viewport to do this rather than manually accessing the MapWidget
        self._widgets[0].tile_size = new_tile_size
        self.dirty = True

    @property
    def view_pos(self):
        return self._view_pos

    @view_pos.setter
    def view_pos(self, new_view_pos):
        self._view_pos = new_view_pos
        self.dirty = True

    def notify(self, event):
        if isinstance(event, MapZoomEvent):
            proposed_zoom_level = event.level + self.tile_size
            if proposed_zoom_level >= 1:
                self.tile_size = proposed_zoom_level
        super().notify(event)


class Display():
    def __init__(self, event_manager):
        # Register the Display to listen for events.
        self._event_manager = event_manager
        self._event_manager.register_listener(self)

        # Initialize the display window.
        self._window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Discover')
        self._window.fill((64, 64, 64))

        # Initialize the Widget tree
        self._root_widget = ContainerWidget(self._window.get_rect().size)
        viewport_size = self._window.get_rect().inflate(-25, -25).size
        self._root_widget.add(ViewportWidget(size=viewport_size, view_pos=(-25, -25), pos=(12.5, 12.5)))

        pygame.display.flip()

    def notify(self, event):
        self._root_widget.notify(event)
        if isinstance(event, TickEvent):
            # Refresh display
            self._window.fill((64, 64, 64))
            self._window.blit(self._root_widget.surface, (0, 0))
            pygame.display.flip()


"""
class PygameView:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)

        pygame.init()
        self.window = pygame.display.set_mode((424, 440))
        pygame.display.set_caption('Example Game')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text = "press space to start"
        textImg = font.render(text, 1, (255, 0, 0))
        self.background.blit(textImg, (0, 0))
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()

        # ----------------------------------------------------------------------

    def ShowMap(self, gameMap):
        # clear the screen first
        self.background.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        # use this squareRect as a cursor and go through the
        # columns and rows and assign the rect
        # positions of the SectorSprites
        squareRect = pygame.Rect((-128, 10, 128, 128))

        column = 0
        for sector in gameMap.sectors:
            if column < 3:
                squareRect = squareRect.move(138, 0)
            else:
                column = 0
                squareRect = squareRect.move(-(138 * 2), 138)
            column += 1
            newSprite = SectorSprite(sector, self.backSprites)
            newSprite.rect = squareRect
            newSprite = None

            # ----------------------------------------------------------------------

            # def ShowCharactor(self, charactor):
            #     sector = charactor.sector
            #     charactorSprite = CharactorSprite(self.frontSprites)
            #     sectorSprite = self.GetSectorSprite(sector)
            #     charactorSprite.rect.center = sectorSprite.rect.center

            # ----------------------------------------------------------------------

            # def MoveCharactor(self, charactor):
            #     charactorSprite = self.GetCharactorSprite(charactor)
            #
            #     sector = charactor.sector
            #     sectorSprite = self.GetSectorSprite(sector)
            #
            #     charactorSprite.moveTo = sectorSprite.rect.center

            # ----------------------------------------------------------------------

            # def GetCharactorSprite(self, charactor):
            #     # there will be only one
            #     for s in self.frontSprites:
            #         return s
            #     return None

            # ----------------------------------------------------------------------

            # def GetSectorSprite(self, sector):
            #     for s in self.backSprites:
            #         if hasattr(s, "sector") and s.sector == sector:
            #             return s

            # ----------------------------------------------------------------------

    def notify(self, event):
        if isinstance(event, TickEvent):
            # Draw Everything
            self.backSprites.clear(self.window, self.background)
            self.frontSprites.clear(self.window, self.background)

            self.backSprites.update()
            self.frontSprites.update()

            dirtyRects1 = self.backSprites.draw(self.window)
            dirtyRects2 = self.frontSprites.draw(self.window)

            dirtyRects = dirtyRects1 + dirtyRects2
            pygame.display.update(dirtyRects)


        elif isinstance(event, MapBuiltEvent):
            gameMap = event.map
            self.ShowMap(gameMap)

        elif isinstance(event, CharactorPlaceEvent):
            self.ShowCharactor(event.charactor)

        elif isinstance(event, CharactorMoveEvent):
            self.MoveCharactor(event.charactor)


class SectorSprite(pygame.sprite.Sprite):
    def __init__(self, sector, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((128, 128))
        self.image.fill((0, 255, 128))

        self.sector = sector


class CharactorSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        charactorSurf = pygame.Surface((64, 64))
        charactorSurf = charactorSurf.convert_alpha()
        charactorSurf.fill((0, 0, 0, 0))  # make transparent
        pygame.draw.circle(charactorSurf, (255, 0, 0), (32, 32), 32)
        self.image = charactorSurf
        self.rect = charactorSurf.get_rect()

        self.moveTo = None

        # ----------------------------------------------------------------------

    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
"""
