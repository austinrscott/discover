#!/usr/bin/python

# Import Python libraries
import random

# Import pygame
import pygame
from pygame.locals import *


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Discover')

    # Render full map
    map_data = create_map_data()
    map = render_map(map_data)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()

        screen.blit(map, (0, 0))
        pygame.display.flip()


def create_map_data():
    return None


def render_map(data):
    tile_size = 5
    grid_size = 100
    water_tile = pygame.Surface((tile_size, tile_size))
    water_tile.fill((25,25,125))
    land_tile = pygame.Surface((tile_size, tile_size))
    land_tile.fill((25,125,25))
    surface = pygame.Surface((grid_size * tile_size, grid_size * tile_size)).convert()
    for y in range(grid_size):
        for x in range(grid_size):
            blitsource = None
            if random.randint(0, 1):
                blitsource = water_tile
            else:
                blitsource = land_tile
            surface.blit(blitsource, (x * tile_size, y * tile_size))
    return surface


if __name__ == '__main__':
    main()
