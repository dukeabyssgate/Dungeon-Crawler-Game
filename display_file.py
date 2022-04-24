import pygame
import global_file


white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (50, 200, 255)

width = global_file.width
height = global_file.height
display = pygame.display.set_mode((width, height))

def uncovering(discovered_tile, x, y):
    for i in range(8):
        for j in range(10):
            # If the player if within the bound of the tile then tile will gain a true value
            if ((j * 100) + 2) < x + 2 < (j * 100) + 102 and (i * 100) + 2 < y + 2 < (i * 100) + 102:
                discovered_tile[i][j] = True

            # if that tile has a false value then a rectangle will be drawn over the tile
            # else it is revealed to the player
            if discovered_tile[i][j] is False:
                pygame.draw.rect(display, black, (2 + (100 * x), 2 + (100 * y), 100, 100))