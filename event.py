#!/usr/bin/python

'''
Much of this code is derived from Shandy Brown's "Writing Games Tutorial". http://ezide.com/games/writing-games.html
Accessed 12/9/16: https://github.com/sjbrown/writing_games_tutorial/blob/example1/code_examples/example.py
tutorial@ezide.com
'''

from weakref import WeakKeyDictionary

from pygame.time import Clock


def debug(msg):
    print(msg)


class Event:
    """this is a superclass for any events that might be generated by an
    object and sent to the EventManager"""

    def __init__(self):
        raise NotImplementedError("Class Event is an abstract base class and not intended for instantiation.")


class TickEvent(Event):
    def __init__(self, time_elapsed, fps):
        self.name = "Event — Tick"
        self.time_elapsed = time_elapsed
        self.fps = fps


class QuitEvent(Event):
    def __init__(self):
        self.name = "Event — Program Quit"


class MapGeneratedEvent(Event):
    def __init__(self, game_map):
        """
        :param game_map:
        """
        self.name = "Event — Map Finished Generating"
        self.map = game_map


class MapZoomEvent(Event):
    def __init__(self, zoom_level):
        """
        :param zoom_level: How much the map has been zoomed in/out, measured in pixels per tile.
        """
        self.name = "Event — Map Zoomed By {}px Per Tile".format(zoom_level)
        self.level = zoom_level


class MouseClickEvent(Event):
    def __init__(self, button, pos):
        """
        :param button: 1 for left click, 3 for right click.
        :param pos: (x, y) location of the click.
        """
        self.name = "Event — Mouse Clicked (Button {} @ {}, {})".format(button, pos[0], pos[1])
        self.button = button
        self.pos = pos


class MouseDragEvent(Event):
    def __init__(self, button, start_pos, end_pos):
        """
        An event in which the mouse was clicked, dragged and a button was released.

        :param button: 1 for left click, 3 for right click.
        :param start_pos: The starting (x, y) of the drag.
        :param end_pos: The ending (x, y) of the drag.
        """
        self.name = "Event — Mouse Dragged (Button {} from {}, {} to {}, {}".format(button, *start_pos, *end_pos)
        self.button = button
        self.start_pos = start_pos
        self.end_pos = end_pos


class MouseDraggingEvent(Event):
    def __init__(self, pos, relative_motion):
        """
        An event in which a mouse button is currently held down and the mouse was moved.

        :param button: 1 for left click, 3 for right click.
        :param relative_motion: The relative (x, y) motion of the drag (since the last mouse position).
        """
        self.name = "Event — Mouse Dragging (From {}, {} to {}, {}".format(*pos, *relative_motion)
        self.pos = pos
        self.rel = relative_motion


class GameStartedEvent(Event):
    def __init__(self, game):
        """
        :param game: The GameModel instance
        """
        self.name = "Event — Game Started"
        self.game = game


class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        self.listeners = WeakKeyDictionary()
        self.event_queue = []

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        if listener in self.listeners:
            del self.listeners[listener]

    def post(self, event):
        if not isinstance(event, TickEvent) and not isinstance(event, MouseDraggingEvent):
            debug("     Message: " + event.name)
        for listener in self.listeners:
            listener.notify(event)


class ClockController:
    """..."""

    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self._clock = Clock()
        self.application_active = True

    def run(self):
        while self.application_active:
            event = TickEvent(self._clock.tick(), self._clock.get_fps())
            self.event_manager.post(event)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            # this will stop the while loop from running
            self.application_active = False
