#!/usr/bin/python

import pygame
from pygame.locals import *
from event import TickEvent, MapGeneratedEvent, MapZoomEvent, MouseDragEvent, MouseDraggingEvent, MouseClickEvent


class Widget():
    def __init__(self, pos=(0, 0)):
        self.pos = pos
        self.dirty = True

    def _render(self):
        raise NotImplementedError("Function _render not implemented in class {}".format(self.__class__))

    def clicked(self, button):
        # Not implemented in base class
        pass

    def notify(self, event):
        if isinstance(event, MouseClickEvent) and self.rect.collidepoint(*event.pos):
            self.clicked(event.button)

    @property
    def surface(self):
        if self.dirty:
            self._render()
        return self._surface

    @property
    def size(self):
        if not hasattr(self, '_size'):
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
        # TODO: Maybe this is too much?
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
        super().notify(event)
        # TODO: Find a more elegant way to do this?
        if isinstance(event, MouseClickEvent):
            translated_event = self._translate_click_event_to_surface_pos(event)
        else:
            translated_event = event
        for widget in self._widgets:
            widget.notify(event=translated_event)

    def _translate_click_event_to_surface_pos(self, event):
        new_pos = (event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])
        return MouseClickEvent(event.button, new_pos)


class MapTile(Widget):
    """A single MapTile knows how to draw the proper graphics for each type of landscape. It doesn't know its absolute
    position on the map but it does hold its position in the map grid as X, Y coordinates."""

    # TODO: MapTiles need to hold both their grid position and need to know their absolute position on the map now.
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

    def clicked(self, button):
        print("DEBUG: Map clicked")

    def notify(self, event):
        if isinstance(event, MapGeneratedEvent):
            self._map = event.map
            self._populate_map_tiles()
            self.dirty = True
        super().notify(event)

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
        self._widgets[0].pos = (-new_view_pos[0], -new_view_pos[1])
        self.dirty = True

    def move_view(self, relative_x, relative_y):
        self.view_pos = (self.view_pos[0] - relative_x, self.view_pos[1] - relative_y)

    def notify(self, event):
        if isinstance(event, MapZoomEvent):
            proposed_zoom_level = event.level + self.tile_size
            if proposed_zoom_level >= 1:
                self.tile_size = proposed_zoom_level
        elif isinstance(event, MouseDraggingEvent):
            self.move_view(*event.rel)
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
            # Update FPS
            pygame.display.set_caption('Discover — FPS: {:0.2f}'.format(event.fps))

            # Refresh display
            self._window.fill((64, 64, 64))
            self._window.blit(self._root_widget.surface, (0, 0))
            pygame.display.flip()
