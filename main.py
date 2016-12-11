#!/usr/bin/python

# Import pygame
import pygame

from display import Display
from event import EventManager, ClockController
from game import GameModel
from input import InputController


def main():
    # Initialize pygame
    pygame.init()

    # Initialize event manager
    event_manager = EventManager()

    # Initialize display, input, and game data
    display_manager = Display(event_manager)
    input_manager = InputController(event_manager)
    game_model = GameModel(event_manager)
    clock = ClockController(event_manager)

    # Run game
    clock.run()


if __name__ == '__main__':
    main()
