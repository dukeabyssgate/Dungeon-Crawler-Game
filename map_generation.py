
import random
from queue import PriorityQueue

import pygame

import global_file

width = 1154
height = 804

half_width = width / 2
half_height = height / 2


map_list = [[], [], [], [], [], [], [], []]
map_tile_ID = [[], [], [], [], [], [], [], []]

tile_name_list = ["tile 1.png", "tile 1_C.png", "tile 2.png", "tile 3_H.png",
                  "tile 3_V.png", "tile 4_E.png", "tile 4_N.png", "tile 4_S.png",
                  "tile 4_W.png", "tile 5_E.png", "tile 5_N.png", "tile 5_S.png",
                  "tile 5_W.png", "tile 6_E.png", "tile 6_N.png", "tile 6_S.png",
                  "tile 6_W.png", "tile 7_E.png", "tile 7_N.png", "tile 7_S.png",
                  "tile 7_W.png", "tile 8_E.png", "tile 8_N.png", "tile 8_S.png",
                  "tile 8_W.png", "tile 8_C_E.png", "tile 8_C_N.png", "tile 8_C_S.png",
                  "tile 8_C_W.png", "tile 9_E.png", "tile 9_N.png", "tile 9_S.png",
                  "tile 9_W.png", "tile 9_C_E.png", "tile 9_C_N.png", "tile 9_C_S.png",
                  "tile 9_C_W.png", "tile 10_E.png", "tile 10_N.png", "tile 10_S.png",
                  "tile 10_W.png", "tile 10_C_E.png", "tile 10_C_N.png", "tile 10_C_S.png",
                  "tile 10_C_W.png",
                  "tile respawn-inactive.png", "tile respawn-active.png",
                  "tile EN.png", "tile EX.png"]

global discovered_tile
discovered_tile = [[False for i in range(10)] for j in range(8)]

# [Name, Type, [Affect], [Stats]]
##[North,East,South,West]
tile_value = {"None": [False, False, False, False], "tile 1.png": [True, True, True, True],
              "tile 1_C.png": [True, True, True, True], "tile 2.png": [True, True, True, True],
              "tile 3_H.png": [False, True, False, True], "tile 3_V.png": [True, False, True, False],
              "tile 4_E.png": [False, False, False, True], "tile 4_N.png": [False, False, True, False],
              "tile 4_S.png": [True, False, False, False], "tile 4_W.png": [False, True, False, False],
              "tile 5_E.png": [False, False, False, True], "tile 5_N.png": [False, False, True, False],
              "tile 5_S.png": [True, False, False, False], "tile 5_W.png": [False, True, False, False],
              "tile 6_E.png": [False, False, True, True], "tile 6_N.png": [False, True, True, False],
              "tile 6_S.png": [True, False, False, True], "tile 6_W.png": [True, True, False, False],
              "tile 7_E.png": [True, False, True, True], "tile 7_N.png": [False, True, True, True],
              "tile 7_S.png": [True, True, False, True], 'tile 7_W.png': [True, True, True, False],
              "tile 8_E.png": [True, False, True, True], "tile 8_N.png": [False, True, True, True],
              "tile 8_S.png": [True, True, False, True], 'tile 8_W.png': [True, True, True, False],
              "tile 8_C_E.png": [True, False, True, True], "tile 8_C_N.png": [False, True, True, True],
              "tile 8_C_S.png": [True, True, False, True], "tile 8_C_W.png": [True, True, True, False],
              "tile 9_E.png": [False, False, True, True], "tile 9_N.png": [False, True, True, False],
              "tile 9_S.png": [True, False, False, True], "tile 9_W.png": [True, True, False, False],
              "tile 9_C_E.png": [False, False, True, True], "tile 9_C_N.png": [False, True, True, False],
              "tile 9_C_S.png": [True, False, False, True], "tile 9_C_W.png": [True, True, False, False],
              "tile 10_E.png": [False, False, False, True], "tile 10_N.png": [False, False, True, False],
              "tile 10_S.png": [True, False, False, False], "tile 10_W.png": [False, True, False, False],
              "tile 10_C_E.png": [False, False, False, True], "tile 10_C_N.png": [False, False, True, False],
              "tile 10_C_S.png": [True, False, False, False], "tile 10_C_W.png": [False, True, False, False],
              "tile respawn-inactive.png": [True, True, True, True],
              "tile respawn-active.png": [True, True, True, True],
              "tile EN.png": [True, True, True, True], "tile EX.png": [True, True, True, True]
              }


class tiles:
    def __init__(self, row, col, tile_name):
        self.row = row
        self.col = col
        self.tile_name = tile_name
        self.neighbours = []

    def get_pos(self):
        return self.row, self.col

    def get_name(self):
        return self.tile_name

    def update_neighbours(self, map_tile_ID, grid):
        self.neighbours = []

        if self.row != 7:
            if tile_value[self.tile_name][2] == tile_value[map_tile_ID[self.row + 1][self.col]][0]:
                if tile_value[self.tile_name][2] is True:
                    self.neighbours.append(grid[self.row + 1][self.col])

        if self.row != 0:
            if tile_value[self.tile_name][0] == tile_value[map_tile_ID[self.row - 1][self.col]][2]:
                if tile_value[self.tile_name][0] is True:
                    self.neighbours.append(grid[self.row - 1][self.col])
        if self.col != 9:
            if tile_value[self.tile_name][1] == tile_value[map_tile_ID[self.row][self.col + 1]][3]:
                if tile_value[self.tile_name][1] is True:
                    self.neighbours.append(grid[self.row][self.col + 1])
        if self.col != 0:
            if tile_value[self.tile_name][3] == tile_value[map_tile_ID[self.row][self.col - 1]][1]:
                if tile_value[self.tile_name][3] is True:
                    self.neighbours.append(grid[self.row][self.col - 1])


def goal_tile():
    returning_list = [0, 0]

    returning_list[0] = random.randint(0, 9)
    returning_list[1] = random.randint(0, 7)

    return returning_list


def generate_map(tile_name_list):
    global floor_number

    map_tile_ID = [["None" for i in range(10)] for j in range(8)]

    map_list = [["None" for i in range(10)] for j in range(8)]

    map_mask = [["None" for i in range(10)] for j in range(8)]

    for y in range(8):
        for x in range(10):
            random_num = random.randint(0, 44)
            number = 0
            Validated = True
            while Validated:
                random_num = random.randint(0, 44)
                Validated = tile_validation(tile_name_list[random_num], map_tile_ID, y, x, 1)

                number += 1
                if number > 50:
                    Validated = False

            map_tile_ID[y][x] = tile_name_list[random_num]

    for i in range(3):
        for y in range(8):
            for x in range(10):
                number = 0
                Validated = True
                while Validated:
                    if tile_validation(map_tile_ID[y][x], map_tile_ID, y, x, 2) is True:
                        random_num = random.randint(0, 44)
                        map_tile_ID[y][x] = tile_name_list[random_num]
                    else:
                        Validated = False

                    number += 1
                    if number > 10:
                        Validated = False

    Validated = True
    while Validated:
        entry_tile_place = goal_tile()
        entry_x = entry_tile_place[0]
        entry_y = entry_tile_place[1]
        Validated = tile_validation(tile_name_list[47], map_tile_ID, entry_y, entry_x, 1)

    entry_tile = pygame.image.load((r"tile list png" + chr(92) + tile_name_list[47]))

    exit_tile_place = goal_tile()
    exit_x = exit_tile_place[0]
    exit_y = exit_tile_place[1]

    while exit_tile_place == entry_tile_place:
        exit_tile_place = goal_tile()
        exit_x = exit_tile_place[0]
        exit_y = exit_tile_place[1]

    exit_tile = pygame.image.load((r"tile list png" + chr(92) + tile_name_list[48]))

    respawn_tile_Place = goal_tile()
    respawn_x = respawn_tile_Place[0]
    respawn_y = respawn_tile_Place[1]

    while exit_tile_place == respawn_tile_Place or entry_tile_place == respawn_tile_Place:
        respawn_tile_Place = goal_tile()
        respawn_x = respawn_tile_Place[0]
        respawn_y = respawn_tile_Place[1]

    respawn_tile = pygame.image.load((r"tile list png" + chr(92) + tile_name_list[45]))

    map_list[respawn_y][respawn_x] = respawn_tile
    map_tile_ID[respawn_y][respawn_x] = tile_name_list[45]

    map_list[entry_y][entry_x] = entry_tile
    map_tile_ID[entry_y][entry_x] = tile_name_list[47]

    map_list[exit_y][exit_x] = exit_tile
    map_tile_ID[exit_y][exit_x] = tile_name_list[48]

    for y in range(8):
        for x in range(10):
            imagename = (r"tile list png" + chr(92) + map_tile_ID[y][x])
            image = pygame.image.load(imagename)
            map_list[y][x] = image

    map_surface = pygame.Surface((width, height))
    map_surface.fill(global_file.background)

    for y in range(8):
        for x in range(10):
            map_surface.blit(map_list[y][x], (2 + 100 * x, 2 + 100 * y))

    map_mask = pygame.mask.from_threshold(map_surface, (62, 39, 35), (50, 20, 25, 100))

    grid = [[], [], [], [], [], [], [], []]
    for i in range(8):
        for j in range(10):
            tile = tiles(i, j, map_tile_ID[i][j])
            grid[i].append(tile)

            if tile.tile_name == "tile EN.png":
                start = tile
            if tile.tile_name == "tile EX.png":
                end = tile
            if tile.tile_name == "tile respawn-inactive.png":
                respawn = tile

    for i in range(8):
        for j in range(10):
            grid[i][j].update_neighbours(map_tile_ID, grid)

    if (global_file.floor_number + 1) % 5 == 0:
        if path_finding(grid, start, respawn):
            if path_finding(grid, respawn, end):
                return map_list, map_tile_ID, map_mask
        else:
            return generate_map(tile_name_list)
    else:
        if path_finding(grid, start, end):
            return map_list, map_tile_ID, map_mask
        else:
            return generate_map(tile_name_list)


def tile_validation(tile_name, map_tile_list, y, x, connections):
    current_tile = tile_value[tile_name]
    value = 0

    if x == 0:
        Left_x = "None"
        Right_x = x + 1
    elif x == 9:
        Left_x = x - 1
        Right_x = "None"
    else:
        Left_x = x - 1
        Right_x = x + 1

    if y == 0:
        Up_y = "None"
        Down_y = y + 1
    elif y == 7:
        Up_y = y - 1
        Down_y = "None"
    else:
        Up_y = y - 1
        Down_y = y + 1

    if Left_x == "None":
        Left_tile = tile_value["None"]
    else:
        Left_tile = tile_value[map_tile_list[y][Left_x]]

    if Right_x == "None":
        Right_tile = tile_value["None"]
    else:
        Right_tile = tile_value[map_tile_list[y][Right_x]]

    if Up_y == "None":
        Up_tile = tile_value["None"]
    else:
        Up_tile = tile_value[map_tile_list[Up_y][x]]

    if Down_y == "None":
        Down_tile = tile_value["None"]
    else:
        Down_tile = tile_value[map_tile_list[Down_y][x]]

    if current_tile[0] == Up_tile[2] and current_tile[0] is True:
        value += 1
    if current_tile[1] == Right_tile[3] and current_tile[1] is True:
        value += 1
    if current_tile[2] == Down_tile[0] and current_tile[2] is True:
        value += 1
    if current_tile[3] == Left_tile[1] and current_tile[3] is True:
        value += 1

    if value >= connections:
        return False
    else:
        return True


def estimate(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct(came_from, current):
    while current in came_from:
        current = came_from[current]
        print(current.row, current.col)


def path_finding(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {tiles: float("inf") for row in grid for tiles in row}
    g_score[start] = 0
    f_score = {tiles: float("inf") for row in grid for tiles in row}
    f_score[start] = estimate(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            return True

        for neighbor in current.neighbours:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + estimate(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
    return False
