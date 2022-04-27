import math
import random
import pickle
from queue import PriorityQueue
import pygame

global clicked

clicked = False
pygame.init()
width = 1154
height = 804

half_width = width / 2
half_height = height / 2

# Sets up the colours to be used
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (50, 200, 255)
background = (62, 39, 35)
icon_1 = (14, 209, 69)
icon_2 = (218, 199, 63)
icon_3 = (128, 0, 255)
display = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

# sets up empty list used for map generation
map_list = [[], [], [], [], [], [], [], []]
map_tile_ID = [[], [], [], [], [], [], [], []]
# list which contains the file name of all the tiles to generate the map
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

# used to cover up the tiles to wait for the player to enter that area
global discovered_tile
discovered_tile = [[False for i in range(10)] for j in range(8)]

enemy_list = []
boss_list = []
# [enemy name, strength, endurance, intelligence, willpower, dexterity, [skills]]
skill_list = []
exclusion_list = []
player_skill_list = []
# [skill name, [acts upon,action,action type], multiplyer, target, MP cost, skill description]
item_list = []
item_name_list = []
equipment_list = []
equipment_name_list = []
# [Item Name, Item Type, [Affect], [Stats]]


Game = True

# loads from a text file the data needed in the correct format and saved into arrays
for line in open("enemy_list.txt", "r"):
    enemy_temp = line.split()
    enemy_temp[0] = enemy_temp[0].replace("_", " ")
    enemy_temp[6] = enemy_temp[6].split("@")
    for i in range(len(enemy_temp[6])):
        enemy_temp[6][i] = enemy_temp[6][i].replace("_", " ")
    enemy_list.append(enemy_temp)
# [enemy name, strength, endurance, intelligence, willpower, dexterity, [skills]]

for line in open("boss_list.txt", "r"):
    boss = line.split()
    boss[0] = boss[0].replace("_", " ")
    boss[6] = boss[6].split("@")
    for i in range(len(boss[6])):
        boss[6][i] = boss[6][i].replace("_", " ")
    boss_list.append(boss)
# [boss name, strength, endurance, intelligence, willpower, dexterity, [skills]]

for line in open("skill_list.txt", "r"):
    skills = line.split()
    skills[0] = skills[0].replace("_", " ")
    skills[1] = skills[1].split("_")
    skills[2] = float(skills[2])
    player_skill_list.append(skills[0])

    skills[4] = int(skills[4])
    skills[5] = skills[5].replace("_", " ")
    skill_list.append(skills)
# [skill name, [acts upon,action,action type], multiplyer, target, MP cost, skill description]

for line in open("exclusion list.txt", "r"):
    skill = line.replace("_", " ")
    skill = skill[:-1]
    exclusion_list.append(skill)
print(exclusion_list)

for line in open("item_list.txt", "r"):
    items = line.split()
    items[0] = items[0].replace("_", " ")
    items[2] = items[2].split("@")
    items[3] = items[3].split("@")
    items.append(0)
    for i in range(len(items[3])):
        items[3][i] = int(items[3][i])
    if items[1] in ["weapon", "helmet", "chest", "legs", "boots"]:
        for i in range(len(items[3])):
            items[4] += abs(items[3][i])
        equipment_list.append(items)
        equipment_name_list.append(items[0])
    elif items[1] == "temp":
        pass
    else:
        item_list.append(items)
        item_name_list.append(items[0])
# [Name, Type, [Affect], [Stats]]
##[North,East,South,West]
# a dictionary containing the direction for each tile the player can go through
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

global player_1
global player_icon
global enemy
global shop_list
global inventory

inventory = [["Health Potion", 3], ["Mana Potion", 3]]
floor_number = 1


# a class used for the rout finding
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

    # a function in the class which checks which tiles have a valid connection with each other
    def update_neighbours(self, map_tile_ID, grid):
        self.neighbours = []

        # checks all tiles except for the bottom tile in the down direction for valid connection
        if self.row != 7:
            if tile_value[self.tile_name][2] == tile_value[map_tile_ID[self.row + 1][self.col]][0]:
                if tile_value[self.tile_name][2] is True:
                    self.neighbours.append(grid[self.row + 1][self.col])

        # checks all tiles except the top tile in the up direction for valid connection
        if self.row != 0:
            if tile_value[self.tile_name][0] == tile_value[map_tile_ID[self.row - 1][self.col]][2]:
                if tile_value[self.tile_name][0] is True:
                    self.neighbours.append(grid[self.row - 1][self.col])
        # checks all tile except for the right most tile in the right direction for valid connection
        if self.col != 9:
            if tile_value[self.tile_name][1] == tile_value[map_tile_ID[self.row][self.col + 1]][3]:
                if tile_value[self.tile_name][1] is True:
                    self.neighbours.append(grid[self.row][self.col + 1])
        # checks all tile except for the left most tile in the left direction for valid connection
        if self.col != 0:
            if tile_value[self.tile_name][3] == tile_value[map_tile_ID[self.row][self.col - 1]][1]:
                if tile_value[self.tile_name][3] is True:
                    self.neighbours.append(grid[self.row][self.col - 1])


# a class for the player icon sprite which is used to navigate the map
class player_icons:
    def __init__(self, x, y, icon, goal_x=None, goal_y=None, respawn_x=None, respawn_y=None):
        self.icon_name = icon
        self.icon = pygame.image.load(r"player " + self.icon_name + ".png").convert_alpha()
        self.icon_mask = pygame.mask.from_surface(self.icon)
        self.x = x
        self.y = y
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.respawn_x = respawn_x
        self.respawn_y = respawn_y
        self.respawn = False

    # the function which allows the sprite to move on the map
    def move(self, direction):
        if direction == "Left":
            self.x -= 3
        elif direction == "Right":
            self.x += 3
        elif direction == "Up":
            self.y -= 3
        elif direction == "Down":
            self.y += 3
        #enemy_call()

    # the function which will draw the player sprite on the map
    def draw_player(self):
        display.blit(self.icon, (self.x, self.y))

    # the function which determines where to draw the player sprite when spawning them
    def player_spawn(self, map_tile_ID):
        tile_pos = [0, 0]
        for i in range(8):
            if "tile EN.png" in map_tile_ID[i]:
                tile_pos[0] = map_tile_ID[i].index("tile EN.png")
                tile_pos[1] = i

        self.x = 50 + (tile_pos[0] * 100)
        self.y = 50 + (tile_pos[1] * 100)
        self.draw_player()

    # function which determines the location of the goal the player is trying to reach
    def player_goal(self, map_tile_ID):
        tile_pos = [0, 0]
        for i in range(8):
            if "tile EX.png" in map_tile_ID[i]:
                tile_pos[0] = map_tile_ID[i].index("tile EX.png")
                tile_pos[1] = i

        self.goal_x = 50 + (tile_pos[0] * 100)
        self.goal_y = 50 + (tile_pos[1] * 100)

    def player_respawn(self, map_tile_ID):
        tile_pos = [0, 0]
        # locates the respawn tile
        for i in range(8):
            if "tile respawn-inactive.png" in map_tile_ID[i]:
                tile_pos[0] = map_tile_ID[i].index("tile respawn-inactive.png")
                tile_pos[1] = i

        self.respawn_x = 50 + (tile_pos[0] * 100)
        self.respawn_y = 50 + (tile_pos[1] * 100)
        self.respawn = False

    def get_respawn(self):
        return self.respawn


# the class that is used to generate an enemy when battling
class enemies:
    def __init__(self, strength, endurance,
                 intelligence, willpower, dexterity, name, skills=None):
        if skills is None:
            skills = []
        self.name = name
        self.strength = int(strength)
        self.endurance = int(endurance)
        self.HP = self.endurance * 10
        self.intelligence = int(intelligence)
        self.willpower = int(willpower)
        self.MP = self.willpower * 10
        self.dexterity = int(dexterity)
        self.skills = skills

        self.BattleStrength = self.strength
        self.BattleEndurance = self.endurance
        self.BattleHP = self.HP
        self.BattleIntelligence = self.intelligence
        self.BattleWillpower = self.willpower
        self.BattleMP = self.MP
        self.BattleDexterity = self.dexterity
        self.BaseCrit = round((self.BattleDexterity / (self.BattleStrength +
                                                       self.BattleEndurance +
                                                       self.BattleIntelligence +
                                                       self.BattleWillpower +
                                                       self.BattleDexterity)) * 100)
        self.Statuses = [[False, 0, 3], [False, 0], [False, 0, 3]]
        # Burn, Sleep, Poison

    def display_stats(self):
        print("Name:", self.name)
        print("Strength:", self.strength)
        print("Endurance:", self.endurance)
        print("HP:", self.HP)
        print("Intelligence:", self.intelligence)
        print("Willpower:", self.willpower)
        print("MP:", self.MP)
        print("Dexterity:", self.dexterity)
        print("skills:", self.skills)

    # the function which will determine the critical chance to be used
    def CritChance(self):
        self.Battle_stats_check()
        crit_chance = round((self.BattleDexterity / (self.BattleStrength +
                                                     self.BattleEndurance +
                                                     self.BattleIntelligence +
                                                     self.BattleWillpower +
                                                     self.BattleDexterity)) * 100)
        # if the generated critical chance is higher than the base critical chance
        # then the generated chance will be used
        # if not then the base chance will be used
        if self.BaseCrit < crit_chance:
            self.BaseCrit = crit_chance
            return crit_chance
        else:
            return self.BaseCrit

    # a function which prevents the temporary battle stats from going below zero
    def Battle_stats_check(self):
        if self.BattleStrength < 0:
            self.BattleStrength = 1
        if self.BattleEndurance < 0:
            self.BattleEndurance = 1
        if self.BattleIntelligence < 0:
            self.BattleIntelligence = 1
        if self.BattleWillpower < 0:
            self.BattleWillpower = 1
        if self.BattleDexterity < 0:
            self.BattleDexterity = 1

    def get_BattleStats(self):
        return [self.BattleStrength, self.BattleEndurance, self.BattleIntelligence,
                self.BattleWillpower, self.BattleDexterity]


# the class for which the player will be generated from and inherits all from the enemy class
class player(enemies):
    def __init__(self, strength, endurance,
                 intelligence, willpower, dexterity, skills=None,
                 name=None):
        super().__init__(strength, endurance, intelligence, willpower, dexterity, name)

        if skills is None:
            skills = ["Attack", "Meditate"]
        if name is None:
            name = [["None", "weapon", "None", "None"], ["None", "helmet", "None", "None"],
                    ["None", "chest", "None", "None"], ["None", "legs", "None", "None"],
                    ["None", "boots", "None", "None"]]
        self.equipment = name
        # [weapon,helmet,chest,legs,boots]
        self.skills = skills

        self.Stats_Point = 20

    def display_Battle_stats(self):
        print("Strength:", self.BattleStrength)
        print("Endurance:", self.BattleEndurance)
        print("HP:", self.BattleHP)
        print("Intelligence:", self.BattleIntelligence)
        print("Willpower:", self.BattleWillpower)
        print("MP:", self.BattleMP)
        print("Dexterity:", self.BattleDexterity)

    def display_equipment(self):
        print("Weapon:", self.equipment[0][0])
        print("Helmet:", self.equipment[1][0])
        print("Chest:", self.equipment[2][0])
        print("Legs:", self.equipment[3][0])
        print("Boots:", self.equipment[4][0])

    # a function to increase the base stats of the player
    def increase_stats(self, option):
        if option == "strength":
            self.strength += 1
        elif option == "endurance":
            self.endurance += 1
        elif option == "intelligence":
            self.intelligence += 1
        elif option == "willpower":
            self.willpower += 1
        elif option == "dexterity":
            self.dexterity += 1

        self.reset_stats()
        self.Stats_Point -= 1

    def change_equipment(self, equip):
        print(equip)
        # This changes the equipment based on what type of equipment it is
        if equip[1] == "weapon":
            current_equip = self.equipment[0]
            self.equipment[0] = equip
        elif equip[1] == "helmet":
            current_equip = self.equipment[1]
            self.equipment[1] = equip
        elif equip[1] == "chest":
            current_equip = self.equipment[2]
            self.equipment[2] = equip
        elif equip[1] == "legs":
            current_equip = self.equipment[3]
            self.equipment[3] = equip
        elif equip[1] == "boots":
            current_equip = self.equipment[4]
            self.equipment[4] = equip

        # that equipment is then removed from the inventory
        for i in range(len(inventory)):
            if inventory[i][0] == equip[0]:
                temp = i

        if inventory[temp][1] - 1 == 0:
            inventory.pop(temp)
        else:
            inventory[temp][1] -= 1

        # this part then adds into the inventory the piece of equipment that was unequipped
        try:
            for i in range(len(inventory)):
                if inventory[i][0] == current_equip[0]:
                    count = i
            inventory[count][1] += 1
        except:
            inventory.append([current_equip[0], 1])

        self.reset_stats()

    # this function updates the battle stats when a new equipment is equipped
    def update_equipment_stats(self, equip):
        if "strength" in equip[2]:
            self.BattleStrength += equip[3][equip[2].index("strength")]
        if "endurance" in equip[2]:
            self.BattleEndurance += equip[3][equip[2].index("endurance")]
        if "intelligence" in equip[2]:
            self.BattleIntelligence += equip[3][equip[2].index("intelligence")]
        if "willpower" in equip[2]:
            self.BattleWillpower += equip[3][equip[2].index("willpower")]
        if "dexterity" in equip[2]:
            self.BattleDexterity += equip[3][equip[2].index("dexterity")]

        self.Battle_stats_check()
        self.BaseCrit = round((self.BattleDexterity / (self.BattleStrength +
                                                       self.BattleEndurance +
                                                       self.BattleIntelligence +
                                                       self.BattleWillpower +
                                                       self.BattleDexterity)) * 100)

    # This function will reset the stats and statuses of the player
    def reset_stats(self):
        self.BattleStrength = self.strength
        self.BattleEndurance = self.endurance
        self.BattleIntelligence = self.intelligence
        self.BattleWillpower = self.willpower
        self.BattleDexterity = self.dexterity

        temp_HP = self.BattleHP / self.HP
        temp_MP = self.BattleMP / self.MP

        for i in range(5):
            if self.equipment[i][0] != "None":
                self.update_equipment_stats(self.equipment[i])

        self.HP = self.BattleEndurance * 10
        if self.HP < 1:
            self.HP = 10
        self.BattleHP = math.ceil(temp_HP * self.HP)

        self.MP = self.BattleWillpower * 10
        if self.MP < 1:
            self.MP = 10
        self.BattleMP = math.ceil(temp_MP * self.MP)

        self.BaseCrit = round((self.BattleDexterity / (self.BattleStrength +
                                                       self.BattleEndurance +
                                                       self.BattleIntelligence +
                                                       self.BattleWillpower +
                                                       self.BattleDexterity)) * 100)
        self.Statuses = [[False, 0, 3], [False, 0], [False, 0, 3]]
        # Burn, Sleep, Poison

    def get_base_stats(self):
        return [self.strength, self.endurance, self.intelligence, self.willpower, self.dexterity]

    def get_equipment(self):
        return self.equipment

    def get_skill(self):
        return self.skills


# This function is used to set up a new game
def initialise():
    # the first map is generated and verified
    map_list, map_tile_ID, map_mask = generate_map(tile_name_list)
    global player_1
    global player_icon
    global floor_number
    global discovered_tile
    global boss_number
    boss_number = 0
    floor_number = 1
    discovered_tile = [[False for i in range(10)] for j in range(8)]
    all_skill_list = []

    icon_list = ["icon 1", "icon 2", "icon 3"]

    # while loop to ensure the user selects a player avatar to use to navigate the map
    while True:
        display.fill(black)
        global clicked
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        button("Please select avatar", 0, 50, width, 50, 50, black, black, None, white)

        # this part allows the player to select what their avatar will look like
        selecting_icon = button("", 100, 400, 100, 100, 1, icon_1, white, selecting)
        if selecting_validation(selecting_icon):
            selecting_icon = icon_list[0]
            break

        selecting_icon = button("", 300, 400, 100, 100, 1, icon_2, white, selecting)
        if selecting_validation(selecting_icon):
            selecting_icon = icon_list[1]
            break

        selecting_icon = button("", 500, 400, 100, 100, 1, icon_3, white, selecting)
        if selecting_validation(selecting_icon):
            selecting_icon = icon_list[2]
            break

        exit_button = button("Back", 1005, 330, 146, 75, 30, white, red, exiting)
        if exit_button is True:
            menu()

        pygame.display.update()
        clock.tick(60)

    for i in range(len(skill_list)):
        all_skill_list.append(skill_list[i][0])

    # this part generates the base player and their icon on to the map
    player_1 = player(100, 100, 100, 100, 100, skills=all_skill_list)
    # player_1 = player(10, 10, 10, 10, 10)
    player_1.reset_stats()

    player_icon = player_icons(0, 0, selecting_icon)

    # generates the initial start, end and respawn points for the player
    player_icon.player_spawn(map_tile_ID)
    player_icon.player_goal(map_tile_ID)
    player_icon.player_respawn(map_tile_ID)

    return map_list, map_tile_ID, map_mask


# This function generates a random coordinate for the goal tile to be placed in
def goal_tile():
    returning_list = [0, 0]

    returning_list[0] = random.randint(0, 9)
    returning_list[1] = random.randint(0, 7)

    return returning_list


# The function which generated a map to be used
def generate_map(tile_name_list):
    global floor_number
    map_tile_ID = [["None" for i in range(10)] for j in range(8)]

    map_list = [["None" for i in range(10)] for j in range(8)]

    map_mask = [["None" for i in range(10)] for j in range(8)]

    # this part generates an initial random map to be used
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

    # this part loops three times to generate a map which has more connections
    # this ensures the map is more likely to be viable
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

    # This part places entry tile into the generated location and verifies there is at least one connection to it
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

    # This part places exit tile into the generated location
    # It also verifies the location is not in the same location as the entry tile
    while exit_tile_place == entry_tile_place:
        exit_tile_place = goal_tile()
        exit_x = exit_tile_place[0]
        exit_y = exit_tile_place[1]

    # This part generates the sprite for the map and saves it to an array
    exit_tile = pygame.image.load((r"tile list png" + chr(92) + tile_name_list[48]))

    respawn_tile_Place = goal_tile()
    respawn_x = respawn_tile_Place[0]
    respawn_y = respawn_tile_Place[1]

    # endures the respawn point is not on top of the end or start tile
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

    # loads in and blits to the surface the corresponding tile
    for y in range(8):
        for x in range(10):
            imagename = (r"tile list png" + chr(92) + map_tile_ID[y][x])
            image = pygame.image.load(imagename)
            map_list[y][x] = image

    map_surface = pygame.Surface((width, height))
    map_surface.fill(background)

    for y in range(8):
        for x in range(10):
            map_surface.blit(map_list[y][x], (2 + 100 * x, 2 + 100 * y))

    # This line generates a mask from the surface with the map sprites on to facilitate collision detection
    map_mask = pygame.mask.from_threshold(map_surface, (62, 39, 35), (50, 20, 25, 100))

    # This part is for the path finding function set up
    grid = [[], [], [], [], [], [], [], []]
    for i in range(8):
        for j in range(10):
            # sets up the tiles which will be used to identify connecting neighbours
            tile = tiles(i, j, map_tile_ID[i][j])
            grid[i].append(tile)

            # designates the tiles which are the goals and start for the path finding algorithm
            if tile.tile_name == "tile EN.png":
                start = tile
            if tile.tile_name == "tile EX.png":
                end = tile
            if tile.tile_name == "tile respawn-inactive.png":
                respawn = tile

    # this loop sets up the connecting neighbours
    for i in range(8):
        for j in range(10):
            grid[i][j].update_neighbours(map_tile_ID, grid)

    # If the path is found then the map is returned
    # If not then the function recursively calls itself until a map with a path is found to be returned
    if (floor_number + 1) % 5 == 0:
        # if the player has reached a boss floor then it generates a map which ensures the player can reach the
        # respawn tile and be able to reach the end tile from the respawn tile (may not be in this order)
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


# This function verifies if a tile has sufficient connections to other tiles
def tile_validation(tile_name, map_tile_list, y, x, connections):
    current_tile = tile_value[tile_name]
    value = 0

    # this section checks if the tile is on the edge of the map
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

    # If the tile that is being validated has a neighbour which also has a true value in that direction
    # then one is added to the value to show there is a connection in that direction
    if current_tile[0] == Up_tile[2] and current_tile[0] is True:
        value += 1
    if current_tile[1] == Right_tile[3] and current_tile[1] is True:
        value += 1
    if current_tile[2] == Down_tile[0] and current_tile[2] is True:
        value += 1
    if current_tile[3] == Left_tile[1] and current_tile[3] is True:
        value += 1

    # If the value is greater than or equal to the specified connection then false is returned to break the loop
    if value >= connections:
        return False
    else:
        return True


# This function checks if a tile has to be revealed to the player as they travel the map
def uncovering(discovered_tile):
    for y in range(8):
        for x in range(10):
            # If the player if within the bound of the tile then tile will gain a true value
            if ((x * 100) + 2) < player_icon.x + 2 < ((x * 100) + 102) and (
                    (y * 100) + 2) < player_icon.y + 2 < ((y * 100) + 102):
                discovered_tile[y][x] = True

            # if that tile has a false value then a rectangle will be drawn over the tile
            # else it is revealed to the player
            if discovered_tile[y][x] is False:
                pygame.draw.rect(display, black, (2 + (100 * x), 2 + (100 * y), 100, 100))


# This function estimates the distance from the current tile to the exit tile, used in the path finding algorithm
def estimate(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


# Function used to reconstruct the shortest path from the entry to the exit tile
def reconstruct(came_from, current):
    while current in came_from:
        current = came_from[current]
        print(current.row, current.col)


# This is the function for the A* path finding algorithm to ensure the map generated is viable
def path_finding(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    # sets the distance to be infinite to start the algorithm
    g_score = {tiles: float("inf") for row in grid for tiles in row}
    g_score[start] = 0
    f_score = {tiles: float("inf") for row in grid for tiles in row}
    f_score[start] = estimate(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    # while there are still nodes to consider in the queue run the loop
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # Remove the node being considered from the queue
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # If the current node being considered is the end point then the path has been found
        if current == end:
            return True

        # check for all neighbouring node of the current node being considered
        for neighbor in current.neighbours:
            temp_g_score = g_score[current] + 1
            # if the estimated distance is less than that of the current estimated distance
            # then add that node to the path
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + estimate(neighbor.get_pos(), end.get_pos())
                # if the current node is not in the queue, add it to the queue to
                # consider if it's neighbours are on the path
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
    # Only return False if no more nodes to consider and the end node has not been reached
    return False


# This function is called to detect if the player sprite has collided with the map sprite
def collision_detect(map_mask, temp_loc):
    offset = (temp_loc[0] + 2, temp_loc[1] + 2)
    result = map_mask.overlap(player_icon.icon_mask, offset)

    # if the result is true then a collision has occurred and the player should not be allowed in that direction
    if result:
        return True
    else:
        return False


# This function determines if the player encounters an enemy
# A random value is generated and if the value is 0 then the battle function will be called
def enemy_call(value=400):
    chance = random.randint(0, value)
    # chance = 0
    if chance == 0:
        print("enemies!")
        battle()


# This function is called when a battle occurs and an enemy is needed to be generated
def enemy_generator(lower, upper):
    global enemy
    enemy = list(enemy_list[random.randint(lower, upper)])
    temp_list = player_1.get_BattleStats()
    # increase the stats of the enemy to scale with the player strength
    average = sum(temp_list) // len(temp_list) // 5
    temp = (floor_number // 40) * 100
    if floor_number <= 3:
        temp = (floor_number * 2) - 6
    print(temp)
    enemy[1] = abs(int(enemy[1]) + average + temp)
    enemy[2] = abs(int(enemy[2]) + average + temp)
    enemy[3] = abs(int(enemy[3]) + average + temp)
    enemy[4] = abs(int(enemy[4]) + average + temp)
    enemy[5] = abs(int(enemy[5]) + average + temp)

    enemy = enemies(enemy[1], enemy[2], enemy[3], enemy[4], enemy[5], enemy[0], enemy[6])
    return enemy


# Function to ensure damage is not in the negatives
def damageCheck(damage):
    if damage <= 0:
        damage = 1
    return damage


# The function which checks if an action should be critical
def CriticalCalc(skill_multi, turn):
    number = random.randint(0, 100)
    # If the generated number is less than or equal to the critical chance of the player or enemy
    # Then the effect of the action is doubled
    if turn == 0:
        crit = player_1.CritChance()
        if number <= crit:
            print("critical")
            skill_multi = skill_multi * 2
    elif turn == 1:
        crit = enemy.CritChance()
        if number <= crit:
            print("critical")
            skill_multi = skill_multi * 2
    display.fill(black)
    battle_info_draw()
    button("Critical!", 150, 150, 400, 100, 20, white, white)
    pygame.display.update()
    pygame.time.wait(1500)
    return skill_multi


# This function checks if either the player or the enemy has ran out of HP
def DeathCheck(Game):
    global enemy
    if player_1.BattleHP <= 0:
        print("player dead")
        Game = False
        game_over()
    elif enemy.BattleHP <= 0:
        print("Enemy dead")

        Game = False
        player_1.reset_stats()
        player_1.BattleHP += enemy.HP / 10
        if player_1.BattleHP > player_1.HP:
            player_1.BattleHP = player_1.HP

        # if the enemy ran out of HP then the player regains some HP as a reward
        button("player regained " + str(enemy.HP / 10) + " HP", 150, 150, 400, 100, 20, white, white)
        battle_info_draw()
        pygame.display.update()
        pygame.time.wait(1000)

    return Game


# def Respawn():
#     pass


# This function ensures the action the player wants to take has enough MP to be used
def player_MPcheck(skill):
    temp = player_1.BattleMP
    cost = skill[4]
    if (temp - cost) < 0:
        return False
    else:
        player_1.BattleMP -= cost
        return True


# This function ensures the action the enemy wants to take has enough MP to be used
def enemy_MPcheck(skill):
    temp = enemy.BattleMP
    cost = skill[4]
    if (temp - cost) < 0:
        return False
    else:
        enemy.BattleMP -= cost
        return True


# This function is used in the battle function to calculate the effect of the action taken
def calculation(picked_skill, multiplyer, turn):
    temp_list = ["burn", "sleep", "poison"]
    action = picked_skill[1][0]
    effect = picked_skill[1][1]
    form = picked_skill[1][2]
    cost = picked_skill[4]
    Target = picked_skill[3]
    if Target == "self":
        if action == "HP":
            if turn % 2 == 0:
                if effect == "+":
                    print("player", player_1.BattleHP)
                    if form == "mag":
                        damage = (player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (player_1.BattleStrength * multiplyer)
                    player_1.BattleHP = player_1.BattleHP + damageCheck(damage)
                    if player_1.BattleHP > player_1.HP:
                        player_1.BattleHP = player_1.HP
                        print("Overflow HP removed")
                else:
                    print("player_1", player_1.BattleHP)
                    if form == "mag":
                        damage = (player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (player_1.BattleStrength * multiplyer)
                    player_1.BattleHP = player_1.BattleHP - damageCheck(damage)
                battle_calc_info(turn, picked_skill, damage)
                print("player HP is", player_1.BattleHP)
            else:
                if effect == "+":
                    if form == "mag":
                        damage = (enemy.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (enemy.BattleStrength * multiplyer)
                    enemy.BattleHP = enemy.BattleHP + damageCheck(damage)
                    if enemy.BattleHP > enemy.HP:
                        enemy.BattleHP = enemy.HP
                        print("Overflow HP removed")
                else:
                    if form == "mag":
                        damage = (enemy.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (enemy.BattleStrength * multiplyer)
                    enemy.BattleHP = enemy.BattleHP - damageCheck(damage)
                battle_calc_info(turn, picked_skill, damage)
                print("enemy HP is", enemy.BattleHP)

        elif action == "MP":
            if turn % 2 == 0:
                if effect == "+":
                    if form == "mag":
                        damage = (player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (player_1.BattleStrength * multiplyer)
                        temp = player_1.HP * (cost / 100)
                        print(temp, damage, cost)
                        if player_1.BattleHP - temp < 0:
                            damage = 0
                        else:
                            player_1.BattleHP -= temp
                    player_1.BattleMP = player_1.BattleMP + damageCheck(damage)
                    if player_1.BattleMP > player_1.MP:
                        player_1.BattleMP = player_1.MP
                        print("overflow MP released")
                else:
                    if form == "mag":
                        damage = (player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (player_1.BattleStrength * multiplyer)
                        temp = abs(damage * (cost / 100))
                        if player_1.BattleHP - temp < 0:
                            damage = 0
                        else:
                            player_1.BattleHP -= temp
                    player_1.BattleMP = player_1.BattleMP - damage
                    if player_1.BattleMP < 0:
                        player_1.BattleMP = 20
                battle_calc_info(turn, picked_skill, damage)
                print("player MP is", player_1.BattleMP)
            else:
                if effect == "+":
                    if form == "mag":
                        damage = (enemy.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (enemy.BattleStrength * multiplyer)
                        temp = abs(damage * (cost / 100))
                        if enemy.BattleHP - temp < 0:
                            damage = 0
                        else:
                            enemy.BattleHP -= temp
                    enemy.BattleMP = enemy.BattleMP + damageCheck(damage)
                    if enemy.BattleMP > enemy.MP:
                        enemy.BattleMP = enemy.MP
                        print("overflow MP released")
                else:
                    if form == "mag":
                        damage = (enemy.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (enemy.BattleStrength * multiplyer)
                        temp = abs(damage * (cost / 100))
                        if enemy.BattleHP - temp < 0:
                            damage = 0
                        else:
                            enemy.BattleHP -= temp
                    enemy.BattleMP = enemy.BattleMP - damage
                    if player_1.BattleMP < 0:
                        player_1.BattleMP = 20
                battle_calc_info(turn, picked_skill, damage)
                print("enemy MP is", enemy.BattleMP)

        elif action == "Attack":
            if turn % 2 == 0:
                if effect == "+":
                    player_1.BattleStrength = player_1.BattleStrength + (player_1.strength * multiplyer)
                else:
                    player_1.BattleStrength = player_1.BattleStrength - (player_1.strength * multiplyer)
                    player_1.Battle_stats_check()
                print("player Strength is", player_1.BattleStrength)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    enemy.BattleStrength = enemy.BattleStrength + (enemy.strength * multiplyer)
                    battle_calc_info(turn, picked_skill)
                else:
                    enemy.BattleStrength = enemy.BattleStrength - (enemy.strength * multiplyer)
                    enemy.Battle_stats_check()
                print("enemy Strength is", enemy.BattleStrength)
                battle_calc_info(turn, picked_skill)

        elif action == "Defence":
            if turn % 2 == 0:
                if effect == "+":
                    player_1.BattleEndurance = player_1.BattleEndurance + (player_1.endurance * multiplyer)
                else:
                    player_1.BattleEndurance = player_1.BattleEndurance - (player_1.endurance * multiplyer)
                    player_1.Battle_stats_check()
                print("player Endurance is", player_1.BattleEndurance)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    enemy.BattleEndurance = enemy.BattleEndurance + (enemy.endurance * multiplyer)

                else:
                    enemy.BattleEndurance = enemy.BattleEndurance - (enemy.endurance * multiplyer)
                    enemy.Battle_stats_check()
                print("enemy Endurance is", enemy.BattleEndurance)
                battle_calc_info(turn, picked_skill)

        elif action == "Intelligence":
            if turn % 2 == 0:
                if effect == "+":
                    player_1.BattleIntelligence = player_1.BattleIntelligence + (player_1.intelligence * multiplyer)
                else:
                    player_1.BattleIntelligence = player_1.BattleIntelligence - (player_1.intelligence * multiplyer)
                    player_1.Battle_stats_check()
                print("player Intelligence is", player_1.BattleIntelligence)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    enemy.BattleIntelligence = enemy.BattleIntelligence + (enemy.intelligence * multiplyer)
                else:
                    enemy.BattleIntelligence = enemy.BattleIntelligence - (enemy.intelligence * multiplyer)
                    enemy.Battle_stats_check()
                print("enemy Intelligence is", enemy.BattleIntelligence)
                battle_calc_info(turn, picked_skill)

        elif action == "Willpower":
            if turn % 2 == 0:
                if effect == "+":
                    player_1.BattleWillpower = player_1.BattleWillpower + (player_1.willpower * multiplyer)
                else:
                    player_1.BattleWillpower = player_1.BattleWillpower - (player_1.willpower * multiplyer)
                    player_1.Battle_stats_check()
                print("player Willpower is", player_1.BattleWillpower)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    enemy.BattleWillpower = enemy.BattleWillpower + (enemy.willpower * multiplyer)
                else:
                    enemy.BattleWillpower = enemy.BattleWillpower - (enemy.willpower * multiplyer)
                    enemy.Battle_stats_check()
                print("enemy Willpower is", enemy.BattleWillpower)
                battle_calc_info(turn, picked_skill)

        elif action == "Dexterity":
            if turn % 2 == 0:
                if effect == "+":
                    player_1.BattleDexterity = player_1.BattleDexterity + (player_1.dexterity * multiplyer)
                else:
                    player_1.BattleDexterity = player_1.BattleDexterity - (player_1.dexterity * multiplyer)
                    player_1.Battle_stats_check()
                print("player Dexterity is", player_1.BattleDexterity)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    enemy.BattleDexterity = enemy.BattleDexterity + (enemy.dexterity * multiplyer)
                else:
                    enemy.BattleDexterity = enemy.BattleDexterity - (enemy.dexterity * multiplyer)
                    enemy.Battle_stats_check()
                print("enemy Dexterity is", enemy.BattleDexterity)
                battle_calc_info(turn, picked_skill)

        elif action == "All":
            if turn % 2 == 0:
                if effect == "+":
                    player_1.BattleStrength += (player_1.strength * multiplyer)
                    player_1.BattleEndurance += (player_1.endurance * multiplyer)
                    player_1.BattleIntelligence += (player_1.intelligence * multiplyer)
                    player_1.BattleWillpower += (player_1.willpower * multiplyer)
                    player_1.BattleDexterity += (player_1.dexterity * multiplyer)
                else:
                    player_1.BattleStrength -= (player_1.strength * multiplyer)
                    player_1.BattleEndurance -= (player_1.endurance * multiplyer)
                    player_1.BattleIntelligence -= (player_1.intelligence * multiplyer)
                    player_1.BattleWillpower -= (player_1.willpower * multiplyer)
                    player_1.BattleDexterity -= (player_1.dexterity * multiplyer)
                    player_1.Battle_stats_check()
            else:
                if effect == "+":
                    enemy.BattleStrength += (enemy.strength * multiplyer)
                    enemy.BattleEndurance += (enemy.endurance * multiplyer)
                    enemy.BattleIntelligence += (enemy.intelligence * multiplyer)
                    enemy.BattleWillpower += (enemy.willpower * multiplyer)
                    enemy.BattleDexterity += (enemy.dexterity * multiplyer)

                else:
                    enemy.BattleStrength -= (enemy.strength * multiplyer)
                    enemy.BattleEndurance -= (enemy.endurance * multiplyer)
                    enemy.BattleIntelligence -= (enemy.intelligence * multiplyer)
                    enemy.BattleWillpower -= (enemy.willpower * multiplyer)
                    enemy.BattleDexterity -= (enemy.dexterity * multiplyer)
                    enemy.Battle_stats_check()
            battle_calc_info(turn, picked_skill)

        elif action == "Status":
            print("status")

    elif Target == "enemy":

        if action == "HP":
            if turn % 2 == 0:
                if effect == "+":
                    if form == "mag":
                        damage = (player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (player_1.BattleStrength * multiplyer)
                    enemy.BattleHP = enemy.BattleHP + damageCheck(damage)
                    if enemy.BattleHP > enemy.HP:
                        enemy.BattleHP = enemy.HP
                        print("Overflow HP removed")
                    print("enemy HP is", enemy.BattleHP)
                else:
                    if picked_skill[0] in ["Back Stab", "Assassinate"]:
                        damage = ((player_1.BattleStrength + player_1.BattleDexterity) * multiplyer) - (
                                enemy.BattleEndurance / 2)
                    elif form == "mag":
                        damage = (player_1.BattleIntelligence * multiplyer) - (enemy.BattleWillpower / 2)
                    elif form == "phy":
                        damage = (player_1.BattleStrength * multiplyer) - (enemy.BattleEndurance / 2)
                    elif form in temp_list:
                        damage = 0
                        for i in temp_list:
                            if i == form and enemy.Statuses[temp_list.index(form)][0]:
                                damage = enemy.HP * multiplyer
                        if damage == 0:
                            damage = 10

                    enemy.BattleHP = enemy.BattleHP - damageCheck(damage)
                    print("enemy HP is", enemy.BattleHP)
                battle_calc_info(turn, picked_skill, damage)
            else:
                if effect == "+":
                    if form == "mag":
                        damage = (enemy.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (enemy.BattleStrength * multiplyer)
                    player_1.BattleHP = player_1.BattleHP + (enemy.BattleStrength * multiplyer)
                    if player_1.BattleHP > player_1.HP:
                        player_1.BattleHP = player_1.HP
                        print("Overflow HP removed")
                    print("player HP is", player_1.BattleHP)
                else:
                    if picked_skill[0] in ["Back Stab", "Assassinate"]:
                        damage = ((enemy.BattleStrength + enemy.BattleDexterity) * multiplyer) - (
                                player_1.BattleEndurance / 2)
                    elif form == "mag":
                        damage = (enemy.BattleIntelligence * multiplyer) - (player_1.BattleWillpower / 2)
                    elif form == "phy":
                        damage = (enemy.BattleStrength * multiplyer) - (player_1.BattleEndurance / 2)
                    elif form in temp_list:
                        damage = 0
                        for i in temp_list:
                            if i == form and player_1.Statuses[temp_list.index(form)][0]:
                                damage = player_1.HP * multiplyer
                        if damage == 0:
                            damage = 10

                    player_1.BattleHP = player_1.BattleHP - damageCheck(damage)
                    print("player HP is", player_1.BattleHP)
                battle_calc_info(turn, picked_skill, damage)

        elif action == "MP":
            if turn % 2 == 0:
                if effect == "+":
                    enemy.BattleMP = enemy.BattleMP + (enemy.intelligence * multiplyer)
                    if enemy.BattleMP > enemy.MP:
                        enemy.BattleMP = enemy.MP
                        print("overflow MP released")
                else:
                    enemy.BattleMP = enemy.BattleMP - (enemy.intelligence * multiplyer)
                print("enemy MP is", enemy.BattleMP)
                battle_calc_info(turn, picked_skill, (enemy.intelligence * multiplyer))
            else:
                if effect == "+":
                    player_1.BattleMP = player_1.BattleMP + (player_1.intelligence * multiplyer)
                    if player_1.BattleMP > player_1.MP:
                        player_1.BattleMP = player_1.MP
                        print("overflow MP released")
                else:
                    player_1.BattleMP = player_1.BattleMP - (player_1.intelligence * multiplyer)
                print("player_1 MP is", player_1.BattleMP)
                battle_calc_info(turn, picked_skill, (player_1.intelligence * multiplyer))

        elif action == "Attack":
            if turn % 2 == 0:
                if effect == "+":
                    enemy.BattleStrength = enemy.BattleStrength + (player_1.strength * multiplyer)
                    print("enemy Strength is", enemy.BattleStrength)
                else:
                    enemy.BattleStrength = enemy.BattleStrength - (player_1.strength * multiplyer)
                    enemy.Battle_stats_check()
                    print("enemy Strength is", enemy.BattleStrength)
            else:
                if effect == "+":
                    player_1.BattleStrength = player_1.BattleStrength + (enemy.strength * multiplyer)
                    print("player Strength is", player_1.BattleStrength)
                else:
                    player_1.BattleStrength = player_1.BattleStrength - (enemy.strength * multiplyer)
                    player_1.Battle_stats_check()
                    print("player Strength is", player_1.BattleStrength)
            battle_calc_info(turn, picked_skill)

        elif action == "Defence":
            if turn % 2 == 0:
                if effect == "+":
                    enemy.BattleEndurance = enemy.BattleEndurance + (player_1.endurance * multiplyer)
                    print("enemy Endurance is", enemy.BattleEndurance)
                else:
                    enemy.BattleEndurance = enemy.BattleEndurance - (player_1.endurance * multiplyer)
                    enemy.Battle_stats_check()
                    print("enemy Endurance is", enemy.BattleEndurance)
            else:
                if effect == "+":
                    player_1.BattleEndurance = player_1.BattleEndurance + (enemy.endurance * multiplyer)
                    print("player Endurance is", player_1.BattleEndurance)
                else:
                    player_1.BattleEndurance = player_1.BattleEndurance - (enemy.endurance * multiplyer)
                    player_1.Battle_stats_check()
                    print("player Endurance is", player_1.BattleEndurance)
            battle_calc_info(turn, picked_skill)

        elif action == "Intelligence":
            if turn % 2 == 0:
                if effect == "+":
                    enemy.BattleIntelligence = enemy.BattleIntelligence + (player_1.intelligence * multiplyer)
                else:
                    enemy.BattleIntelligence = enemy.BattleIntelligence - (player_1.intelligence * multiplyer)
                    enemy.Battle_stats_check()
                print("enemy Intelligence is", enemy.BattleIntelligence)
            else:
                if effect == "+":
                    player_1.BattleIntelligence = player_1.BattleIntelligence + (enemy.intelligence * multiplyer)
                else:
                    player_1.BattleIntelligence = player_1.BattleIntelligence - (enemy.intelligence * multiplyer)
                    player_1.Battle_stats_check()
                print("player Intelligence is", player_1.BattleIntelligence)
            battle_calc_info(turn, picked_skill)

        elif action == "Willpower":
            if turn % 2 == 0:
                if effect == "+":
                    enemy.BattleWillpower = enemy.BattleWillpower + (player_1.willpower * multiplyer)
                else:
                    enemy.BattleWillpower = enemy.BattleWillpower - (player_1.willpower * multiplyer)
                    enemy.Battle_stats_check()
                print("enemy Willpower is", enemy.BattleWillpower)
            else:
                if effect == "+":
                    player_1.BattleWillpower = player_1.BattleWillpower + (enemy.willpower * multiplyer)
                else:
                    player_1.BattleWillpower = player_1.BattleWillpower - (enemy.willpower * multiplyer)
                    player_1.Battle_stats_check()
                print("player Willpower is", player_1.BattleWillpower)
            battle_calc_info(turn, picked_skill)

        elif action == "Dexterity":
            if turn % 2 == 0:
                if effect == "+":
                    enemy.BattleDexterity = enemy.BattleDexterity + (player_1.dexterity * multiplyer)
                else:
                    enemy.BattleDexterity = enemy.BattleDexterity - (player_1.dexterity * multiplyer)
                    enemy.Battle_stats_check()
                print("enemy Dexterity is", enemy.BattleDexterity)
            else:
                if effect == "+":
                    player_1.BattleDexterity = player_1.BattleDexterity + (enemy.dexterity * multiplyer)
                else:
                    player_1.BattleDexterity = player_1.BattleDexterity - (enemy.dexterity * multiplyer)
                    player_1.Battle_stats_check()
                print("player Dexterity is", player_1.BattleDexterity)
            battle_calc_info(turn, picked_skill)

        elif action == "All":
            if turn % 2 == 0:
                if effect == "+":
                    enemy.BattleStrength += (player_1.strength * multiplyer)
                    enemy.BattleEndurance += (player_1.endurance * multiplyer)
                    enemy.BattleIntelligence += (player_1.intelligence * multiplyer)
                    enemy.BattleWillpower += (player_1.willpower * multiplyer)
                    enemy.BattleDexterity += (player_1.dexterity * multiplyer)
                else:
                    enemy.BattleStrength -= (player_1.strength * multiplyer)
                    enemy.BattleEndurance -= (player_1.endurance * multiplyer)
                    enemy.BattleIntelligence -= (player_1.intelligence * multiplyer)
                    enemy.BattleWillpower -= (player_1.willpower * multiplyer)
                    enemy.BattleDexterity -= (player_1.dexterity * multiplyer)
                    enemy.Battle_stats_check()
            else:
                if effect == "+":
                    player_1.BattleStrength += (enemy.strength * multiplyer)
                    player_1.BattleEndurance += (enemy.endurance * multiplyer)
                    player_1.BattleIntelligence += (enemy.intelligence * multiplyer)
                    player_1.BattleWillpower += (enemy.willpower * multiplyer)
                    player_1.BattleDexterity += (enemy.dexterity * multiplyer)

                else:
                    player_1.BattleStrength -= (enemy.strength * multiplyer)
                    player_1.BattleEndurance -= (enemy.endurance * multiplyer)
                    player_1.BattleIntelligence -= (enemy.intelligence * multiplyer)
                    player_1.BattleWillpower -= (enemy.willpower * multiplyer)
                    player_1.BattleDexterity -= (enemy.dexterity * multiplyer)
                    player_1.Battle_stats_check()
            battle_calc_info(turn, picked_skill)

        # This section checks if the action should inflict the corresponding status effect
        elif action == "Status":
            chance = random.randint(0, 100)
            if effect == "Burn":
                if chance <= multiplyer:
                    if turn % 2 == 0:
                        enemy.Statuses[0][0] = True
                        enemy.Statuses[0][1] += 1
                        if enemy.Statuses[0][1] == 4:
                            enemy.Statuses[0][1] = 3
                        else:
                            enemy.BattleEndurance = enemy.BattleEndurance - (enemy.endurance * 0.1)
                        enemy.Statuses[0][2] = 3
                        print("Burn stage", enemy.Statuses[0][1], "was applied")
                    else:
                        player_1.Statuses[0][0] = True
                        player_1.Statuses[0][1] += 1
                        if player_1.Statuses[0][1] == 4:
                            player_1.Statuses[0][1] = 3
                        player_1.BattleEndurance = player_1.BattleEndurance - (player_1.endurance * 0.1)
                        player_1.Statuses[0][2] = 3
                        print("Burn stage", player_1.Statuses[0][1], "was applied")
                    battle_calc_info(turn, picked_skill, 0, 1)

                else:
                    print("Burn was ineffective")
                    battle_calc_info(turn, picked_skill, 0, -1)

            elif effect == "Sleep":
                if chance <= multiplyer:
                    if turn % 2 == 0:
                        enemy.Statuses[1][0] = True
                        enemy.Statuses[1][1] += 1
                        if enemy.Statuses[1][1] == 4:
                            enemy.Statuses[1][1] = 3
                        print("Sleep stage", enemy.Statuses[1][1], "was applied")
                    else:
                        player_1.Statuses[1][0] = True
                        player_1.Statuses[1][1] += 1
                        if player_1.Statuses[1][1] == 4:
                            player_1.Statuses[1][1] = 3
                        print("Sleep stage", player_1.Statuses[1][1], "was applied")
                    battle_calc_info(turn, picked_skill, 0, 1)
                else:
                    print("Sleep was ineffective")
                    battle_calc_info(turn, picked_skill, 0, 0)

            elif effect == "Poison":
                if chance <= multiplyer:
                    if turn % 2 == 0:
                        enemy.Statuses[2][0] = True
                        enemy.Statuses[2][1] += 1
                        if enemy.Statuses[2][1] == 4:
                            enemy.Statuses[2][1] = 3
                        else:
                            enemy.BattleDexterity = enemy.BattleDexterity - (enemy.dexterity * 0.1)
                        enemy.Statuses[2][2] = 3
                        print("Poison stage", enemy.Statuses[2][1], "was applied")
                    else:
                        player_1.Statuses[2][0] = True
                        player_1.Statuses[2][1] += 1
                        if player_1.Statuses[2][1] == 4:
                            player_1.Statuses[2][1] = 3
                        player_1.BattleDexterity = player_1.BattleDexterity - (player_1.dexterity * 0.1)
                        player_1.Statuses[2][2] = 3
                        print("Poison stage", player_1.Statuses[2][1], "was applied")
                    battle_calc_info(turn, picked_skill, 0, 1)
                else:
                    print("Poison was ineffective")
                    battle_calc_info(turn, picked_skill, 0, -1)


# This function is called at the start of every turn so active status effects can take place
def status_check(turn):
    sleep = False
    player_checklist = []
    enemy_checklist = []
    # This part allows for the check if the player or enemy has any status effects active
    for i in range(3):
        player_checklist.append(player_1.Statuses[i][0])
    for i in range(3):
        enemy_checklist.append(enemy.Statuses[i][0])

    if turn == 0:
        if True in player_checklist:
            # this checks if the burn status on the player is active
            if player_1.Statuses[0][0]:
                print("Activate player Burn")
                # this line deals the corresponding damage due to the burn to the player
                player_1.BattleHP = player_1.BattleHP - (player_1.endurance * 0.1 * player_1.Statuses[0][1])
                player_1.Statuses[0][2] -= 1
                # The duration of the burn is then decreased by one
                if player_1.Statuses[0][2] == 0:
                    # If the duration reaches zero then the player is given back their endurance
                    # and other values are reset and the status is removed
                    player_1.Statuses[0][0] = False
                    for i in range(player_1.Statuses[0][1]):
                        player_1.BattleEndurance = player_1.BattleEndurance + (player_1.endurance * 0.1)
                    player_1.Statuses[0][1] = 0
                    player_1.Statuses[0][2] = 3
                    print("Burn removed")

            if player_1.Statuses[1][0]:
                print("Activate player Sleep")
                chance = random.randint(0, 100)
                if player_1.Statuses[1][1] == 1:
                    if chance <= 50:
                        player_1.Statuses[1][0] = False
                        print("sleep deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in sleep")
                elif player_1.Statuses[1][1] == 2:
                    if chance <= 30:
                        player_1.Statuses[1][0] = False
                        print(" deep sleep deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in deep sleep")
                elif player_1.Statuses[1][1] == 3:
                    if chance <= 25:
                        player_1.Statuses[1][0] = False
                        print("coma deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in a coma")

            if player_1.Statuses[2][0]:
                player_1.BattleHP = player_1.BattleHP - (player_1.HP * 0.01 * player_1.Statuses[2][1])
                player_1.Statuses[2][2] -= 1
                if player_1.Statuses[2][2] == 0:
                    player_1.Statuses[2][0] = False
                    for i in range(player_1.Statuses[2][1]):
                        player_1.BattleDexterity = player_1.BattleDexterity + (player_1.dexterity * 0.1)
                    player_1.Statuses[2][1] = 0
                    player_1.Statuses[2][2] = 3
                    print("Poison removed")

                print("Activate player poison")
        return sleep

    elif turn == 1:
        if True in enemy_checklist:
            if enemy.Statuses[0][0]:
                print("Activate enemy Burn")
                enemy.BattleHP = enemy.BattleHP - (enemy.endurance * 0.1 * enemy.Statuses[0][1])
                enemy.Statuses[0][2] -= 1
                if enemy.Statuses[0][2] == 0:
                    enemy.Statuses[0][0] = False
                    for i in range(enemy.Statuses[0][1]):
                        enemy.BattleEndurance = enemy.BattleEndurance + (enemy.endurance * 0.1)
                    enemy.Statuses[0][1] = 0
                    enemy.Statuses[0][2] = 3

            if enemy.Statuses[1][0]:
                print("Activate enemy Sleep")
                chance = random.randint(0, 100)
                if enemy.Statuses[1][1] == 1:
                    if chance <= 50:
                        enemy.Statuses[1][0] = False
                        enemy.Statuses[1][1] = 0
                        print("sleep deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in sleep")
                elif enemy.Statuses[1][1] == 2:
                    if chance <= 30:
                        enemy.Statuses[1][0] = False
                        enemy.Statuses[1][1] = 0
                        print(" deep sleep deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in deep sleep")
                elif enemy.Statuses[1][1] == 3:
                    if chance <= 25:
                        enemy.Statuses[1][0] = False
                        enemy.Statuses[1][1] = 0
                        print("coma deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in a coma")

            if enemy.Statuses[2][0]:
                print(enemy.BattleHP)
                enemy.BattleHP = enemy.BattleHP - (enemy.HP * 0.01 * enemy.Statuses[2][1])
                print(enemy.BattleHP)
                enemy.Statuses[2][2] -= 1
                if enemy.Statuses[2][2] == 0:
                    enemy.Statuses[2][0] = False
                    for i in range(enemy.Statuses[2][1]):
                        enemy.BattleDexterity = enemy.BattleDexterity + (enemy.dexterity * 0.1)
                    enemy.Statuses[2][1] = 0
                    enemy.Statuses[2][2] = 3

                print("Activate enemy poison")
        return sleep


# This is the function that is called when a battle is needed
def battle(boss=False):
    global enemy
    global boss_number
    # global floor_number
    battle = True
    Run = False

    # This ""if" loop checks if the enemy to be spawned is a regular enemy or a boss enemy
    if not boss:
        # If not the boss enemy then which group of normal enemy to spawn
        if boss_number == 0:
            enemy = enemy_generator(0, 5)
        elif boss_number == 1:
            enemy = enemy_generator(3, 8)
        elif boss_number == 2:
            enemy = enemy_generator(9, 11)
        elif boss_number == 3:
            enemy = enemy_generator(12, 17)
        elif boss_number == 4:
            enemy = enemy_generator(18, 20)
        elif boss_number == 5:
            enemy = enemy_generator(21, 23)
        elif boss_number == 6:
            enemy = enemy_generator(24, 25)
        elif boss_number == 7:
            enemy = enemy_generator(26, 30)

    else:
        # Each time a player defeats a boss it cycles through to the next boss
        # it will start again when all bosses are cycled through
        try:
            enemy = boss_list[boss_number]
        except:
            boss_number = 0
            enemy = list(boss_list[boss_number])

        # This section scales up the enemy stats so the stronger the player is the stronger the enemy is
        temp_list = player_1.get_BattleStats()

        average = sum(temp_list) // len(temp_list) // 5

        count = (floor_number // 5) - (boss_number + 1)

        enemy[1] = int(enemy[1]) + average + count
        enemy[2] = int(enemy[2]) + average + count
        enemy[3] = int(enemy[3]) + average + count
        enemy[4] = int(enemy[4]) + average + count
        enemy[5] = int(enemy[5]) + average + count
        print("generated")

        enemy = enemies(enemy[1], enemy[2], enemy[3], enemy[4], enemy[5], enemy[0], enemy[6])

    print(enemy.display_stats())

    # This section decides who gets the first move
    if player_1.BattleDexterity > enemy.BattleDexterity:
        turn = 0
    else:
        turn = 1

    # main move for the battle
    while DeathCheck(battle):
        display.fill(black)
        battle_info_draw()
        global clicked
        clicked = False
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    enemy.BattleHP = 0
                if event.key == pygame.K_9:
                    player_1.BattleHP = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        # This checks if the player or enemy has the sleep status and if they do the turn is skipped
        if status_check(turn % 2):
            turn += 1
        InvalidMove = True

        # This is the player turn
        if turn % 2 == 0:

            while InvalidMove:
                display.fill(black)
                battle_info_draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            clicked = True

                if keys[pygame.K_0]:
                    enemy.BattleHP = 0
                player_action = button("Fight", 750, 600, 200, 100, 50, white, red, fight)
                if player_action is not None:
                    break

                # Opens the screen for the skill selection
                player_action = button("Skills", 950, 600, 200, 100, 50, white, red, skill_selection)
                if player_action is not None:
                    if player_MPcheck(skill_list[player_skill_list.index(player_action)]):
                        InvalidMove = False
                    else:
                        print("Invalid move, lack MP")
                        display.fill(black)

                # opens the screen for the item selection
                Item = button("Items", 750, 700, 200, 100, 50, white, red, item_selection)
                if Item:
                    InvalidMove = False
                    player_picked_skill = ["None", "None", "None", "None"]

                Run = button("Run", 950, 700, 200, 100, 50, white, red, run)
                if Run is True:
                    InvalidMove = False
                    player_picked_skill = ["None", "None", "None", "None"]

                pygame.display.update()
                clock.tick(60)

            # Makes sure the action selected is valid
            try:
                player_picked_skill = player_skill_list.index(player_action)
                player_picked_skill = skill_list[player_picked_skill]
                print(player_picked_skill)

            except ValueError:
                pass

            # This checks for special action and carry them out
            try:
                try:
                    if enemy_picked_skill[0] in ["Block", "Magic Shield"]:
                        if enemy_picked_skill[0] == "Block":
                            if player_picked_skill[1][0] == "HP" and player_picked_skill[1][1] == "-" and \
                                    player_picked_skill[1][
                                        2] == "phy":
                                print("Action had no effect")
                            else:
                                calculation(player_picked_skill, CriticalCalc(player_picked_skill[2], (turn % 2)), turn)

                        elif enemy_picked_skill[0] == "Magic Shield":
                            if player_picked_skill[1][0] == "HP" and player_picked_skill[1][1] == "-" and \
                                    player_picked_skill[1][
                                        2] == "mag":
                                print("Action had no effect")
                            else:
                                calculation(player_picked_skill, CriticalCalc(player_picked_skill[2], (turn % 2)), turn)
                    else:
                        try:
                            calculation(player_picked_skill, CriticalCalc(player_picked_skill[2], (turn % 2)), turn)
                        except TypeError:
                            pass
                except UnboundLocalError:
                    try:
                        calculation(player_picked_skill, CriticalCalc(player_picked_skill[2], (turn % 2)), turn)
                    except TypeError:
                        pass
            except UnboundLocalError:
                pass

            turn += 1

            if Run is True:
                if not boss:
                    chance = random.randint(0, 100)
                    if chance < 30:
                        battle = False
                        break
                    else:
                        button("Failed To Run", 150, 150, 400, 100, 20, white, white)
                        pygame.display.update()
                        pygame.time.wait(1500)
                else:
                    button("Failed To Run", 150, 150, 400, 100, 20, white, white)
                    pygame.display.update()
                    pygame.time.wait(1500)

        # This is the enemy turn
        else:
            print("enemy action")
            # The AI that decides what action the enemy should use
            enemy_picked_skill = AI_decide()
            print("--", enemy_picked_skill)

            try:
                if player_picked_skill[0] in ["Block", "Magic Shield"]:
                    if player_picked_skill[0] == "Block":
                        if enemy_picked_skill[1][0] == "HP" and enemy_picked_skill[1][1] == "-" and \
                                enemy_picked_skill[1][
                                    2] == "phy":
                            print("Action had no effect")
                        else:
                            calculation(enemy_picked_skill, CriticalCalc(enemy_picked_skill[2], (turn % 2)), turn)

                    elif player_picked_skill[0] == "Magic Shield":
                        if enemy_picked_skill[1][0] == "HP" and enemy_picked_skill[1][1] == "-" and \
                                enemy_picked_skill[1][
                                    2] == "mag":
                            print("Action had no effect")
                        else:
                            calculation(enemy_picked_skill, CriticalCalc(enemy_picked_skill[2], (turn % 2)), turn)
                else:
                    calculation(enemy_picked_skill, CriticalCalc(enemy_picked_skill[2], (turn % 2)), turn)
            except (UnboundLocalError, TypeError):
                calculation(enemy_picked_skill, CriticalCalc(enemy_picked_skill[2], (turn % 2)), turn)

            print(enemy_picked_skill)

            turn += 1
        pygame.display.update()
        clock.tick(60)


# This function uses a bubble sort to sort the enemy skills based on the effect ascending or descending
def skill_sorting(unsorted_list, orderType):
    for i in range(len(unsorted_list) - 1):
        for j in range(len(unsorted_list) - i - 1):
            if orderType:
                # sorts descending
                if unsorted_list[j][2] < unsorted_list[j + 1][2]:
                    unsorted_list[j], unsorted_list[j + 1] = unsorted_list[j + 1], unsorted_list[j]
            else:
                # sorts ascending
                if unsorted_list[j][2] > unsorted_list[j + 1][2]:
                    unsorted_list[j], unsorted_list[j + 1] = unsorted_list[j + 1], unsorted_list[j]


# The AI which decides on what action the enemy should take based on the current situations
def AI_decide():
    attack_list = []
    high_attack_list = []
    buff_list = []
    debuff_list = []
    defence_list = []
    heal_list = []
    rest_list = []
    status_list = []
    status_damage_list = []

    total_skill_list = []

    player_Health = round(player_1.BattleHP / player_1.HP) * 100
    player_Mana = round(player_1.BattleMP / player_1.MP) * 100
    enemy_Health = round(enemy.BattleHP / enemy.HP) * 100
    enemy_Mana = round(enemy.BattleMP / enemy.MP) * 100

    for i in range(len(enemy.skills)):
        for j in range(len(skill_list)):
            if enemy.skills[i] == skill_list[j][0]:
                enemy_picked_skill = skill_list[j]
        affecting = enemy_picked_skill[1]
        effect = enemy_picked_skill[2]

        if enemy_Health > 90 and all(x in affecting for x in ["HP", "+"]):
            continue

        if enemy_Mana > 90 and all(x in affecting for x in ["MP", "+"]):
            continue

        for x in player_1.Statuses:
            if True in x:
                break
        else:
            if any(x in affecting for x in ["sleep", "burn", "poison"]):
                continue

        total_skill_list.append(enemy_picked_skill)

        if enemy_picked_skill[0] in ["Block", "Magic Shield"] or (
                affecting[0] in ["Defence", "Willpower"] and affecting[1] == "+"):
            defence_list.append(enemy_picked_skill)

        if affecting[0] == "Status":
            status_list.append(enemy_picked_skill)

        if affecting[0] in ["HP", "MP"] and affecting[1] == "-":
            if affecting[2] in ["mag", "phy"]:
                attack_list.append(enemy_picked_skill)
            elif affecting[2] in ["burn", "sleep", "poison"]:
                status_damage_list.append(enemy_picked_skill)

        if affecting[0] == "HP" and affecting[1] == "+":
            heal_list.append(enemy_picked_skill)

        if affecting[0] == "MP" and affecting[1] == "+":
            rest_list.append(enemy_picked_skill)

        if affecting[0] in ["Attack", "Defence", "Intelligence", "Willpower", "Dexterity",
                            "All"] and affecting[1] == "+":
            buff_list.append(enemy_picked_skill)

        if affecting[0] in ["Attack", "Defence", "Intelligence", "Willpower", "Dexterity",
                            "All"] and affecting[1] == "-":
            debuff_list.append(enemy_picked_skill)

    skill_sorting(attack_list, True)
    for i in range(math.ceil(len(attack_list) / 4)):
        high_attack_list.append(attack_list[i])
    random.shuffle(attack_list)

    skill_sorting(heal_list, True)

    print("all", total_skill_list)
    print("Attack", attack_list)
    print("high attack", high_attack_list)
    print("Defence", defence_list)
    print("Buff", buff_list)
    print("debuff", debuff_list)
    print("heal", heal_list)
    print("rest", rest_list)
    print("status", status_list)
    print("Status damage", status_damage_list)

    if enemy_Health < 30 and player_Health < 30:
        print("last stand")
        for i in range(len(high_attack_list)):
            if enemy_MPcheck(high_attack_list[i]):
                return high_attack_list[i]

    if enemy_Health < 30:
        print("heal")
        for i in range(len(heal_list)):
            if enemy_MPcheck(heal_list[i]):
                return heal_list[i]

    if enemy_Mana < 30:
        print("restore mana")
        for i in range(len(rest_list)):
            if enemy_MPcheck(rest_list[i]):
                return rest_list[i]

    if player_Mana < 20 and enemy_Health < 50:
        print("Heal")
        for i in range(len(heal_list)):
            if enemy_MPcheck(heal_list[i]):
                return heal_list[i]

    if player_Health < 30:
        print("High attack")
        if random.randint(0, 1) == 1:
            for i in range(len(high_attack_list)):
                if enemy_MPcheck(high_attack_list[i]):
                    return high_attack_list[i]

    if True not in player_1.Statuses:
        if status_list:
            print("status")
            if random.randint(0, 5) == 0:
                for i in range(len(status_list)):
                    if enemy_MPcheck(status_list[i]):
                        return status_list[i]

    if True in player_1.Statuses:
        print("Status Action")
        if random.randint(0, 1) == 0:
            for i in range(len(status_list)):
                if enemy_MPcheck(status_list[i]):
                    return status_list[i]
        else:
            if status_damage_list:
                for i in range(len(status_damage_list)):
                    if enemy_MPcheck(status_damage_list[i]):
                        return status_damage_list[i]

    if player_Health > 50 and enemy_Health > 50:
        print("buff")
        if random.randint(0, 5) == 0:
            for i in range(len(buff_list)):
                if enemy_MPcheck(buff_list[i]):
                    return buff_list[i]

    if player_Health < 50:
        print("moderate attack")
        if random.randint(0, 1) == 1:
            for i in range(len(attack_list)):
                if enemy_MPcheck(attack_list[i]):
                    return attack_list[i]

    if player_Health > 80:
        print("debuff")
        if random.randint(0, 5) == 0:
            for i in range(len(debuff_list)):
                if enemy_MPcheck(debuff_list[i]):
                    return debuff_list[i]

    if player_Health < 80:
        print("general attack")
        for i in range(len(attack_list)):
            if enemy_MPcheck(attack_list[i]):
                return attack_list[i]

    print("basic attack")
    temp_skill = total_skill_list[random.randint(0, len(total_skill_list) - 1)]
    if random.randint(0, 1) == 1:
        if enemy_MPcheck(temp_skill):
            return temp_skill
    else:
        return ['Attack', ['HP', '-', 'phy'], 1.0, 'enemy', 0, 'Basic_Attack']


# draws the health bars and the sprites for the player and enemy
# and indicate if they are suffering from any status effects
def battle_info_draw():
    Text_font = pygame.font.Font("freesansbold.ttf", 20)
    sleep = pygame.image.load(r"sleep.png")
    poison = pygame.image.load(r"poison.png")
    burn = pygame.image.load(r"burn.png")

    player_sprite = pygame.image.load(r"player sprite.png")
    enemy_sprite = pygame.image.load(r"enemy sprites" + chr(92) + str(enemy.name) + ".png")

    # enemy info
    display.blit(enemy_sprite, (600, 125))
    pygame.draw.rect(display, white, (795, 75, 330, 75))
    pygame.draw.rect(display, background, (790, 70, 340, 85))
    button(enemy.name, 795, 75, 330, 35, 20, white, white)
    button("", 825, 110, 300, 40, 1, red, red)
    button("HP", 795, 110, 30, 20, 20, white, white)
    button("MP", 795, 130, 30, 20, 20, white, white)

    # indicate what statuses are affecting the enemy
    if enemy.Statuses[0][0]:
        display.blit(burn, (800, 50))
    if enemy.Statuses[1][0]:
        display.blit(sleep, (825, 50))
    if enemy.Statuses[2][0]:
        display.blit(poison, (850, 50))

    # the health and mana bars
    if enemy.BattleHP > 0:
        button("", 825, 110, ((enemy.BattleHP / enemy.HP) * 300), 20, 20, green, green)
    text_surf, text_rect = text_objects((str(int(enemy.BattleHP)) + "/" + str(enemy.HP)), Text_font)
    text_rect.center = (975, 120)
    display.blit(text_surf, text_rect)

    if enemy.BattleMP > 0:
        button("", 825, 130, ((enemy.BattleMP / enemy.MP) * 300), 20, 20, blue, blue)
    text_surf, text_rect = text_objects((str(int(enemy.BattleMP)) + "/" + str(enemy.MP)), Text_font)
    text_rect.center = (975, 140)
    display.blit(text_surf, text_rect)

    # player info
    display.blit(player_sprite, (50, 350))
    pygame.draw.rect(display, white, (25, 675, 330, 75))
    pygame.draw.rect(display, background, (20, 670, 340, 85))
    button("Player", 25, 675, 330, 35, 20, white, white)
    button("", 55, 710, 300, 40, 1, red, red)
    button("HP", 25, 710, 30, 20, 20, white, white)
    button("MP", 25, 730, 30, 20, 20, white, white)

    if player_1.Statuses[0][0]:
        display.blit(burn, (25, 650))
    if player_1.Statuses[1][0]:
        display.blit(sleep, (50, 650))
    if player_1.Statuses[2][0]:
        display.blit(poison, (75, 650))

    if player_1.BattleHP > 0:
        button("", 55, 710, ((player_1.BattleHP / player_1.HP) * 300), 20, 20, green, green)
    text_surf, text_rect = text_objects((str(int(player_1.BattleHP)) + "/" + str(player_1.HP)), Text_font)
    text_rect.center = (205, 720)
    display.blit(text_surf, text_rect)

    if player_1.BattleMP > 0:
        button("", 55, 730, ((player_1.BattleMP / player_1.MP) * 300), 20, 20, blue, blue)
    text_surf, text_rect = text_objects((str(int(player_1.BattleMP)) + "/" + str(player_1.MP)), Text_font)
    text_rect.center = (205, 740)
    display.blit(text_surf, text_rect)


# draws the results of the action taken by the player or enemy
def battle_calc_info(turn, skill, damage=0, successful=0):
    display.fill(black)
    battle_info_draw()
    message = ""
    message2 = ""
    if turn % 2 == 0:
        message2 += "Player "
        if skill[3] == "self":
            message += "Player "
            if skill[1][0] in ["HP", "MP", "Attack", "Defence", "Intelligence", "Willpower", "Dexterity", "All"]:
                message += skill[1][0] + " Stat"
            elif skill[1][0] == "Status":
                message += "Inflicted " + skill[1][1] + " Skill"

            if skill[1][1] == "-":
                message += " Decreased "
            elif skill[1][1] == "+":
                message += " Increased "
            if skill[1][0] in ["HP", "MP"]:
                message += "by " + str(damageCheck(damage))
        else:
            message += "Enemy "
            if skill[1][0] in ["HP", "MP", "Attack", "Defence", "Intelligence", "Willpower", "Dexterity", "All"]:
                message += skill[1][0]
            elif skill[1][0] == "Status":
                message += "Inflicted " + skill[1][1]

            if skill[1][1] == "-":
                message += " Decreased "
            elif skill[1][1] == "+":
                message += " Increased "
            if skill[1][0] in ["HP", "MP"]:
                message += "by " + str(damageCheck(damage))
    else:
        message2 += "Enemy "
        if skill[3] == "self":
            message += "Enemy "
            if skill[1][0] in ["HP", "MP", "Attack", "Defence", "Intelligence", "Willpower", "Dexterity"]:
                message += skill[1][0]
            elif skill[1][0] == "Status":
                message += "Inflicted " + skill[1][1]

            if skill[1][1] == "-":
                message += " Decreased "
            elif skill[1][1] == "+":
                message += " Increased "
            if skill[1][0] in ["HP", "MP"]:
                message += "by " + str(damageCheck(damage))
        else:
            message += "Player "
            if skill[1][0] in ["HP", "MP", "Attack", "Defence", "Intelligence", "Willpower", "Dexterity"]:
                message += skill[1][0]
            elif skill[1][0] == "Status":
                message += "Inflicted " + skill[1][1]

            if skill[1][1] == "-":
                message += " Decreased "
            elif skill[1][1] == "+":
                message += " Increased "
            if skill[1][0] in ["HP", "MP"]:
                message += "by " + str(damageCheck(damage))

    # the action that was used is displayed and then the effects are displayed
    message2 += "used " + skill[0]
    button(message2, 150, 150, 400, 100, 20, white, white)
    pygame.display.update()
    pygame.time.wait(1500)

    button(message, 150, 150, 400, 100, 20, white, white)
    pygame.display.update()
    pygame.time.wait(1500)

    # this section displays if a status inducting move was used and shows if it was successful or not
    if successful == 1:
        display.fill(black)
        battle_info_draw()
        button((skill[1][1] + " was successfully applied"), 150, 150, 400, 100, 20, white, white)
        pygame.display.update()
        pygame.time.wait(1500)
    elif successful == -1:
        display.fill(black)
        battle_info_draw()
        button((skill[1][1] + " was unsuccessfully"), 150, 150, 400, 100, 20, white, white)
        pygame.display.update()
        pygame.time.wait(1500)
    print(message)


def fight():
    print("action fight")


# this function allows the player to select a skill they own
def skill_selection():
    total_skills = len(player_1.skills)
    skill_number = 0
    split_skill = int(math.ceil(total_skills / 5))
    split_skill_list = []
    selected_skill = None
    page = 0
    try:
        player_1.skills.remove("Attack")
    except ValueError:
        pass

    # this for loop splits the skills owned by the player into a 2d array so they are on different pages
    for i in range(split_skill):
        split_skill_list.append([])
        for j in range(5):
            try:
                split_skill_list[i].append(str(player_1.skills[skill_number]))
            except:
                split_skill_list[i].append("None")
            skill_number += 1

    while selected_skill is None:

        display.fill(black)
        battle_info_draw()
        global clicked
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        try:
            # this displays one page of skills
            for i in range(5):
                if split_skill_list[page][i] != "None":
                    selected_skill = button(split_skill_list[page][i], 25, 25 + (i * 50), 240, 50, 18, white, red,
                                            selecting)
                    if 25 < mx < 275 and 25 + (i * 50) < my < 75 + (i * 50):
                        # if the mouse is within the bounds the skill information and skill cost will be displayed
                        skill_display = []
                        skill_info = skill_list[player_skill_list.index(split_skill_list[page][i])]
                        skill_info_split = skill_info[5].split()
                        temp = skill_info_split[0]

                        skill_info_split.pop(0)
                        if skill_info_split:
                            empty = True
                        while empty:

                            if len(temp) <= 24:
                                temp = temp + " " + skill_info_split[0]
                                skill_info_split.pop(0)
                            else:
                                skill_display.append(temp)
                                temp = skill_info_split[0]
                                skill_info_split.pop(0)
                            if not skill_info_split:
                                skill_display.append(temp)
                                break

                        for j in range(len(skill_display)):
                            button(str(skill_display[j]), 300, 100 + (j * 50), 350, 50, 18, white, white)
                        button(str("Skill Cost: " + str(skill_info[4]) + " MP"), 300, 100 + ((j + 1) * 50), 350, 50, 18,
                               white, white)
                else:
                    button(split_skill_list[page][i], 25, 25 + (i * 50), 240, 50, 20, white, white)
                if selecting_validation(selected_skill):
                    break

        except IndexError:
            page -= 1

        # This section allows the player to change the page of skills they are selecting
        try:
            page += button("Next", 145, 275, 120, 50, 20, white, red, page_change)
        except TypeError:
            page = page

        try:
            page -= button("Back", 25, 275, 120, 50, 20, white, red, page_change)
        except TypeError:
            page = page

        if button("Exit", 270, 25, 100, 50, 25, white, red, exiting):
            break

        if page < 0:
            page = 0

        pygame.display.update()
        clock.tick(60)

    return selected_skill


# This function is similar to the skill selection function but for items instead of skills
def item_selection():
    item_number = 0
    split_item_list = []
    consumable_list = []
    selected_item = None
    page = 0

    for i in range(len(inventory)):
        try:
            temp = inventory[i]

            for j in range(len(item_list)):
                if temp[0] == item_list[j][0]:
                    temp2 = list(item_list[j])
                    temp2.append(temp[1])
                    consumable_list.append(temp2)
        except:
            pass

    split_item = int(math.ceil(len(consumable_list) / 5))

    for i in range(split_item):
        split_item_list.append([])
        for j in range(5):
            try:
                split_item_list[i].append(consumable_list[item_number])
            except:
                split_item_list[i].append(["None", "None", "None", "None", "None", "None"])
            item_number += 1

    while selected_item is None:
        display.fill(black)
        battle_info_draw()
        global clicked
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        try:
            for i in range(5):
                if split_item_list[page][i][0] != "None":
                    selected_item = button(split_item_list[page][i][0], 25, 25 + (i * 50), 240, 50, 20, white, red,
                                           selecting)
                    if 25 < mx < 245 and 25 + (i * 50) < my < 75 + (i * 50):
                        button("Increases", 300, 150, 200, 50, 20, white, white)
                        for j in range(len(split_item_list[page][i][2])):
                            button((str(split_item_list[page][i][2][j]) + " by " + str(split_item_list[page][i][3][j])),
                                   300, 205 + (j * 55), 200, 50, 15, white, white)
                else:
                    button(split_item_list[page][i][0], 25, 25 + (i * 50), 240, 50, 20, white, white)
                if selecting_validation(selected_item):
                    item_effect(split_item_list[page][i][0], split_item_list[page][i][2], split_item_list[page][i][3])
                    split_item_list[page][i][5] -= 1
                    for j in inventory:
                        if j[0] == split_item_list[page][i][0]:
                            j[1] -= 1
                            if j[1] == 0:
                                inventory.pop(inventory.index(j))
                    if split_item_list[page][i][5] == 0:
                        split_item_list[page][i][0] = "None"
                    break

        except IndexError:
            page -= 1

        try:
            page += button("Next", 145, 275, 120, 50, 20, white, red, page_change)
        except TypeError:
            page = page

        try:
            page -= button("Back", 25, 275, 120, 50, 20, white, red, page_change)
        except TypeError:
            page = page

        if button("Exit", 270, 25, 100, 50, 25, white, red, exiting):
            return False

        if page < 0:
            page = 0

        pygame.display.update()
        clock.tick(60)
    print(selected_item)
    return True


# This function is called when an item is selected and apply their effects
def item_effect(name, affects, value):
    for i in range(len(affects)):
        if affects[i] == "HP":
            player_1.BattleHP += value[i]
            if player_1.BattleHP > player_1.HP:
                player_1.BattleHP = player_1.HP
        elif affects[i] == "MP":
            player_1.BattleMP += value[i]
            if player_1.BattleMP > player_1.MP:
                player_1.BattleMP = player_1.MP
        elif affects[i] == "Attack":
            player_1.BattleStrength += value[i]
        elif affects[i] == "Endurance":
            player_1.BattleEndurance += value[i]
        elif affects[i] == "Intelligence":
            player_1.BattleIntelligence += value[i]
        elif affects[i] == "Willpower":
            player_1.BattleWillpower += value[i]
        elif affects[i] == "Dexterity":
            player_1.BattleDexterity += value[i]
        battle_calc_info(0, [name, [affects[i], "+", ""], 0, "self", 0, ""], value[i])


def run():
    print("running")
    return True


# the function is used to allow a skill or item to be selected
def selecting():
    pass


# the function is used to allow a skill or item to be selected
def selecting_validation(selected):
    if selected is None:
        pass
    else:
        return True


# The function to allow the page for selecting to change
def page_change():
    return 1


# function to allow the user to exit menus
def exiting():
    return True


# The function to turn a string message into a text object to be blitted onto the screen
def text_objects(text, font, colour=black):
    text_surface = font.render(text, True, colour)
    return text_surface, text_surface.get_rect()


# This function is called when the player reaches zero HP
def game_over():
    display.fill(black)

    button("Game Over", 0, 100, width, 50, 100, black, black, colour=red)
    pygame.display.update()
    pygame.time.wait(2000)
    # checks if  the player has reached visited the respawn point
    if player_icon.get_respawn():
        display.fill(black)
        button("Resurrecting", 0, 100, width, 50, 100, black, black, colour=red)

        pygame.display.update()
        pygame.time.wait(2000)
        # if the player has visited the respawn point the game loads to the state the player was in when they visited it
        load_game("respawn save file.txt")


# The function which give functionality to all the buttons
def button(message, x, y, width, height, font_size, colour1, colour2, action=None, colour=black):
    global clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # clicked = False

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(display, colour2, (x, y, width, height))
        if clicked:
            clicked = False
            if click[0] == 1 and action is not None:
                if action == main:
                    map_list, map_tile_ID, map_mask = initialise()
                    main(map_list, map_tile_ID, map_mask, refresh_shop())

                elif action == load_game:
                    if message == "Load Game":
                        return load_game()
                    elif message == "Resurrect":
                        return load_game("respawn save file.txt")

                elif action == fight:
                    return "Attack"

                # if the button is pressed it will call the function which is in action
                elif action == skill_selection:
                    return skill_selection()

                elif action == item_selection:
                    return item_selection()

                elif action == run:
                    return run()

                elif action == page_change:
                    return page_change()

                elif action == exiting:
                    return exiting()

                elif action == selecting:
                    return message

                else:
                    action()
    else:
        # draws the button when it is not highlighted by the mouse
        pygame.draw.rect(display, colour1, (x, y, width, height))

    Text_font = pygame.font.Font("freesansbold.ttf", font_size)
    text_surf, text_rect = text_objects(message, Text_font, colour)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    display.blit(text_surf, text_rect)


# Functions to change the equipment of the player that is selected from the change_equipment function
def replace_equip(selected):
    for i in range(len(equipment_name_list)):
        if equipment_name_list[i] == selected:
            player_1.change_equipment(equipment_list[i])
            break


# A function that allows the player to select what equipment they want to change
# This function is called from the status screen function
def change_equipment(type_of_equip):
    page = 0
    while True:
        global clicked
        clicked = False
        display.fill(background)
        pygame.draw.rect(display, black, (0, 0, 1004, 804))
        number = 0

        selecting_item = None
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        # the corresponding equipment type is extracted from the player inventory and saved to an array
        # this array is split into pages
        # the selected page of the array will display each equipment as a button and when the mouse is within the bounds
        # the information regarding the equipment will be displayed
        if type_of_equip == "head":
            if player_1.equipment[1][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(player_1.equipment[1][0], 650, 110, 250, 100, 15, white, white)

            helmet_list = []
            selecting_list = []
            for i in range(len(inventory)):
                temp = inventory[i]
                try:
                    temp = equipment_list[equipment_name_list.index(temp[0])]
                except:
                    pass
                if temp[1] == "helmet":
                    helmet_list.append(temp)
            for i in range(int(math.ceil(len(helmet_list) / 5)) + 1):
                selecting_list.append([])
                for j in range(5):
                    try:
                        selecting_list[i].append(helmet_list[number])
                    except:
                        selecting_list[i].append(["None", "None", "None", "none"])
                    number += 1

            try:
                for i in range(5):
                    if selecting_list[page][i][0] != "None":
                        selecting_item = button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15,
                                                white, red, selecting)
                        if 50 < mx < 250 and 50 + (i * 100) < my < 150 + (i * 100):
                            draw_stat_name(300, 100, 150, 50, 20)
                            if "strength" not in selecting_list[page][i][2]:
                                button("0", 450, 100, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("strength")]),
                                       450, 100, 50, 50, 20, white, white)

                            if "endurance" not in selecting_list[page][i][2]:
                                button("0", 450, 150, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("endurance")]),
                                       450, 150, 50, 50, 20, white, white)

                            if "intelligence" not in selecting_list[page][i][2]:
                                button("0", 450, 200, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[
                                    page][i][2].index("intelligence")]), 450, 200, 50, 50, 20, white, white)

                            if "willpower" not in selecting_list[page][i][2]:
                                button("0", 450, 250, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("willpower")]),
                                       450, 250, 50, 50, 20, white, white)

                            if "dexterity" not in selecting_list[page][i][2]:
                                button("0", 450, 300, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("dexterity")]),
                                       450, 300, 50, 50, 20, white, white)

                    else:
                        button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15, white, white)
                    if selecting_validation(selecting_item):
                        replace_equip(selecting_item)
                        break

            except IndexError:
                pass

        if type_of_equip == "chest":
            if player_1.equipment[2][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(player_1.equipment[2][0], 650, 110, 250, 100, 15, white, white)

            chest_list = []
            selecting_list = []
            for i in range(len(inventory)):
                temp = inventory[i]
                try:
                    temp = equipment_list[equipment_name_list.index(temp[0])]
                except:
                    pass
                if temp[1] == "chest":
                    chest_list.append(temp)
            for i in range(int(math.ceil(len(chest_list) / 5)) + 1):
                selecting_list.append([])
                for j in range(5):
                    try:
                        selecting_list[i].append(chest_list[number])
                    except:
                        selecting_list[i].append(["None", "None", "None", "none"])
                    number += 1

            try:
                for i in range(5):
                    if selecting_list[page][i][0] != "None":
                        selecting_item = button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15,
                                                white, red, selecting)
                        if 50 < mx < 250 and 50 + (i * 100) < my < 150 + (i * 100):
                            draw_stat_name(300, 100, 150, 50, 20)
                            if "strength" not in selecting_list[page][i][2]:
                                button("0", 450, 100, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("strength")]),
                                       450, 100, 50, 50, 20, white, white)

                            if "endurance" not in selecting_list[page][i][2]:
                                button("0", 450, 150, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("endurance")]),
                                       450, 150, 50, 50, 20, white, white)

                            if "intelligence" not in selecting_list[page][i][2]:
                                button("0", 450, 200, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[
                                    page][i][2].index("intelligence")]), 450, 200, 50, 50, 20, white, white)

                            if "willpower" not in selecting_list[page][i][2]:
                                button("0", 450, 250, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("willpower")]),
                                       450, 250, 50, 50, 20, white, white)

                            if "dexterity" not in selecting_list[page][i][2]:
                                button("0", 450, 300, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("dexterity")]),
                                       450, 300, 50, 50, 20, white, white)

                    else:
                        button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15, white, white)
                    if selecting_validation(selecting_item):
                        replace_equip(selecting_item)
                        break

            except IndexError:
                pass

        if type_of_equip == "legs":
            if player_1.equipment[3][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(player_1.equipment[3][0], 650, 110, 250, 100, 15, white, white)

            legs_list = []
            selecting_list = []
            for i in range(len(inventory)):
                temp = inventory[i]
                try:
                    temp = equipment_list[equipment_name_list.index(temp[0])]
                except:
                    pass
                if temp[1] == "legs":
                    legs_list.append(temp)
            for i in range(int(math.ceil(len(legs_list) / 5)) + 1):
                selecting_list.append([])
                for j in range(5):
                    try:
                        selecting_list[i].append(legs_list[number])
                    except:
                        selecting_list[i].append(["None", "None", "None", "none"])
                    number += 1

            try:
                for i in range(5):
                    if selecting_list[page][i][0] != "None":
                        selecting_item = button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15,
                                                white, red, selecting)
                        if 50 < mx < 250 and 50 + (i * 100) < my < 150 + (i * 100):
                            draw_stat_name(300, 100, 150, 50, 20)
                            if "strength" not in selecting_list[page][i][2]:
                                button("0", 450, 100, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("strength")]),
                                       450, 100, 50, 50, 20, white, white)

                            if "endurance" not in selecting_list[page][i][2]:
                                button("0", 450, 150, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("endurance")]),
                                       450, 150, 50, 50, 20, white, white)

                            if "intelligence" not in selecting_list[page][i][2]:
                                button("0", 450, 200, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[
                                    page][i][2].index("intelligence")]), 450, 200, 50, 50, 20, white, white)

                            if "willpower" not in selecting_list[page][i][2]:
                                button("0", 450, 250, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("willpower")]),
                                       450, 250, 50, 50, 20, white, white)

                            if "dexterity" not in selecting_list[page][i][2]:
                                button("0", 450, 300, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("dexterity")]),
                                       450, 300, 50, 50, 20, white, white)

                    else:
                        button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15, white, white)
                    if selecting_validation(selecting_item):
                        replace_equip(selecting_item)
                        break

            except IndexError:
                pass

        if type_of_equip == "boots":
            if player_1.equipment[4][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(player_1.equipment[4][0], 650, 110, 250, 100, 15, white, white)

            boots_list = []
            selecting_list = []
            for i in range(len(inventory)):
                temp = inventory[i]
                try:
                    temp = equipment_list[equipment_name_list.index(temp[0])]
                except:
                    pass
                if temp[1] == "boots":
                    boots_list.append(temp)
            for i in range(int(math.ceil(len(boots_list) / 5)) + 1):
                selecting_list.append([])
                for j in range(5):
                    try:
                        selecting_list[i].append(boots_list[number])
                    except:
                        selecting_list[i].append(["None", "None", "None", "none"])
                    number += 1

            try:
                for i in range(5):
                    if selecting_list[page][i][0] != "None":
                        selecting_item = button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15,
                                                white, red, selecting)
                        if 50 < mx < 250 and 50 + (i * 100) < my < 150 + (i * 100):
                            draw_stat_name(300, 100, 150, 50, 20)
                            if "strength" not in selecting_list[page][i][2]:
                                button("0", 450, 100, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("strength")]),
                                       450, 100, 50, 50, 20, white, white)

                            if "endurance" not in selecting_list[page][i][2]:
                                button("0", 450, 150, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("endurance")]),
                                       450, 150, 50, 50, 20, white, white)

                            if "intelligence" not in selecting_list[page][i][2]:
                                button("0", 450, 200, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[
                                    page][i][2].index("intelligence")]), 450, 200, 50, 50, 20, white, white)

                            if "willpower" not in selecting_list[page][i][2]:
                                button("0", 450, 250, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("willpower")]),
                                       450, 250, 50, 50, 20, white, white)

                            if "dexterity" not in selecting_list[page][i][2]:
                                button("0", 450, 300, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("dexterity")]),
                                       450, 300, 50, 50, 20, white, white)

                    else:
                        button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15, white, white)
                    if selecting_validation(selecting_item):
                        replace_equip(selecting_item)
                        break

            except IndexError:
                pass

        if type_of_equip == "weapon":
            if player_1.equipment[0][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(player_1.equipment[0][0], 650, 110, 250, 100, 15, white, white)

            weapon_list = []
            selecting_list = []
            for i in range(len(inventory)):
                temp = inventory[i]
                try:
                    temp = equipment_list[equipment_name_list.index(temp[0])]
                except:
                    pass
                if temp[1] == "weapon":
                    weapon_list.append(temp)
            for i in range(int(math.ceil(len(weapon_list) / 5)) + 1):
                selecting_list.append([])
                for j in range(5):
                    try:
                        selecting_list[i].append(weapon_list[number])
                    except:
                        selecting_list[i].append(["None", "None", "None", "none"])
                    number += 1

            try:
                for i in range(5):
                    if selecting_list[page][i][0] != "None":
                        selecting_item = button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15,
                                                white, red, selecting)
                        if 50 < mx < 250 and 50 + (i * 100) < my < 150 + (i * 100):
                            draw_stat_name(300, 100, 150, 50, 20)
                            if "strength" not in selecting_list[page][i][2]:
                                button("0", 450, 100, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("strength")]),
                                       450, 100, 50, 50, 20, white, white)

                            if "endurance" not in selecting_list[page][i][2]:
                                button("0", 450, 150, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("endurance")]),
                                       450, 150, 50, 50, 20, white, white)

                            if "intelligence" not in selecting_list[page][i][2]:
                                button("0", 450, 200, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[
                                    page][i][2].index("intelligence")]), 450, 200, 50, 50, 20, white, white)

                            if "willpower" not in selecting_list[page][i][2]:
                                button("0", 450, 250, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("willpower")]),
                                       450, 250, 50, 50, 20, white, white)

                            if "dexterity" not in selecting_list[page][i][2]:
                                button("0", 450, 300, 50, 50, 20, white, white)
                            else:
                                button(str(selecting_list[page][i][3][selecting_list[page][i][2].index("dexterity")]),
                                       450, 300, 50, 50, 20, white, white)

                    else:
                        button(str(selecting_list[page][i][0]), 50, 50 + (i * 100), 200, 100, 15, white, white)
                    if selecting_validation(selecting_item):
                        replace_equip(selecting_item)
                        break

            except IndexError:
                pass

        try:
            page += button("Next", 150, 550, 100, 50, 20, white, red, page_change)
        except TypeError:
            page = page

        try:
            page -= button("Back", 50, 550, 100, 50, 20, white, red, page_change)
        except TypeError:
            page = page

        if page < 0:
            page = 0

        if page > len(selecting_list) - 1:
            page = len(selecting_list) - 1

        exit_button = button("Back", 1005, 330, 146, 75, 30, white, red, exiting)

        if exit_button is True:
            break

        pygame.display.update()
        clock.tick(60)


# Function to randomise the shop lists
def refresh_shop():
    global shop_list
    shop_list = [[], [], []]
    # generates 5 random items for the equipment shop
    for i in range(5):
        count = random.randint(0, len(equipment_list) - 1)
        shop_list[0].append(list(equipment_list[count]))
        # randomises the price up
        shop_list[0][i][4] = math.ceil(equipment_list[count][4] * random.uniform(1, 2))
    # generates 5 random skills the player can purchase
    for i in range(5):
        count = random.randint(2, len(skill_list) - 1)
        # while loops excludes skills the player is not supposed to posses
        while skill_list[count][0] in exclusion_list:
            count = random.randint(2, len(skill_list) - 1)
        # scales up the price of the skills
        shop_list[1].append([list(skill_list[count])[0],
                             math.ceil(skill_list[count][2] + skill_list[count][4] * random.uniform(5, 10))])

    # generates 5 random consumable items for the player to purchase
    for i in range(5):
        count = random.randint(0, len(item_list) - 1)
        shop_list[2].append(list(item_list[count]))
        # gives fluctuate the price of each item
        shop_list[2][i][4] = math.ceil(sum(shop_list[2][i][3]) * random.uniform(0.5, 1.25))

    return shop_list


# this function group together items in the player inventory
def compile_inventory(inventory):
    temp_list = [inventory[0]]
    # checks for duplicate items and group together
    for i in range(1, len(inventory)):
        inventory_added = False
        temp = inventory[i]
        for j in range(len(temp_list)):
            if temp[0] in temp_list[j]:
                temp_list[j][1] += 1
                inventory_added = True
                break
        if not inventory_added:
            temp_list.append(temp)

    return list(temp_list)


# Allows the user to sort their inventory to show strongest item/equipment/skills first (temporary)
def sort_inventory(inventory):
    list_of_equipment = []
    list_of_item = []
    list_of_skill = list(player_1.skills)

    split_list_of_equipment = []
    split_list_of_item = []
    split_list_of_skill = []

    for i in range(len(inventory)):
        temp = inventory[i]
        try:
            temp = equipment_list[equipment_name_list.index(temp[0])]
            list_of_equipment.append(temp)
        except:
            pass
        try:
            temp = list(item_list[item_name_list.index(temp[0])])
            temp[4] = inventory[i][1]
            list_of_item.append(temp)
        except:
            pass

    for i in range(len(list_of_skill)):
        for j in range(len(skill_list)):
            if list_of_skill[i] == skill_list[j][0]:
                list_of_skill[i] = skill_list[j]

    # sorting
    # sort equipment
    number = 0
    sort_items(list_of_equipment)
    for i in range(int(math.ceil(len(list_of_equipment) / 5)) + 1):
        split_list_of_equipment.append([])
        for j in range(5):
            try:
                split_list_of_equipment[i].append(list_of_equipment[number])
            except:
                split_list_of_equipment[i].append(["None", "None", "None", "None"])
            number += 1

    # sort items
    number = 0
    sort_items(list_of_item)
    for i in range(int(math.ceil(len(list_of_item) / 5))):
        split_list_of_item.append([])
        for j in range(5):
            try:
                split_list_of_item[i].append(list_of_item[number])
            except:
                split_list_of_item[i].append(["None", "None", "None", "None", "None"])
            number += 1

    # sort skills
    skill_sorting(list_of_skill, True)
    number = 0
    for i in range(int(math.ceil(len(list_of_skill) / 5))):
        split_list_of_skill.append([])
        for j in range(5):
            try:
                split_list_of_skill[i].append(list_of_skill[number])
            except:
                split_list_of_skill[i].append(["None", "None", "None", "None", "None"])
            number += 1

    return split_list_of_equipment, split_list_of_item, split_list_of_skill


# Performs a bubble sort by the sum value item stats changes
def sort_items(unsorted_list):
    # how many total passes the sort needs
    for i in range(len(unsorted_list) - 1):
        # performs one complete pass and compares the values
        for j in range(len(unsorted_list) - i - 1):
            # if a swap is needed the swap will be performed so the list is sorted descending
            if sum(unsorted_list[j][3]) < sum(unsorted_list[j + 1][3]):
                unsorted_list[j], unsorted_list[j + 1] = unsorted_list[j + 1], unsorted_list[j]


# the main menu of the program when first ran
def menu():
    while True:
        global clicked
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        display.fill(black)
        button("The Tower", 0, 50, width, 50, 100, black, black, None, red)
        button("New Game", 100, 200, 250, 100, 25, white, red, main)
        button("Load Game", 100, 400, 250, 100, 25, white, red, load_game)
        button("Resurrect", 400, 400, 250, 100, 25, white, red, load_game)
        button("How To Play", 100, 600, 250, 100, 25, white, red, info)

        pygame.display.update()
        clock.tick(60)


# function to display information about how to play this game
def info():
    while True:
        help_list = []
        global clicked
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
        display.fill(black)

        # the text is read from a text file saved to an array
        info_file = open("help info.txt", "r")
        for line in info_file:
            help_list.append(line[:-1])

        # the array is looped through to print the text onto the screen
        for i in range(len(help_list)):
            button(help_list[i], 0, 100 + (i * 55), width, 50, 20, black, black, None, white)

        exit_button = button("back", 470, 500, 200, 50, 20, white, red, exiting)
        if exit_button is True:
            break

        pygame.display.update()
        clock.tick(60)


# function to draw the names of the stats in the desired location
def draw_stat_name(x, y, width, height, size):
    button("Strength", x, y, width, height, size, white, white)
    button("Endurance", x, y + height, width, height, size, white, white)
    button("Intelligence", x, y + 2 * height, width, height, size, white, white)
    button("Willpower", x, y + 3 * height, width, height, size, white, white)
    button("Dexterity", x, y + 4 * height, width, height, size, white, white)


# the function which shows the status screen which shows the player stats and their equipped equipment
def status_screen():
    player_1.reset_stats()
    while True:
        global clicked
        clicked = False
        display.fill(background)
        pygame.draw.rect(display, black, (0, 0, 1004, 804))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        button("Player Status", (width / 2 - 150), (height / 100), 200, 50, 50, black, black, colour=red)

        button("Free Status Points", 50, 100, 305, 50, 30, white, white)
        button(str(player_1.Stats_Point), 360, 100, 55, 50, 30, white, white)

        button("Strength", 50, 155, 200, 50, 30, white, white)

        # allows the player to use their points to increase their base stats of choice
        button(str(player_1.BattleStrength), 255, 155, 100, 50, 30, white, white)
        if player_1.Stats_Point > 0:
            pressing = button("+", 360, 155, 55, 50, 30, white, red, exiting)
            if pressing is True:
                player_1.increase_stats("strength")

        button("Endurance", 50, 210, 200, 50, 30, white, white)
        button(str(player_1.BattleEndurance), 255, 210, 100, 50, 30, white, white)

        if player_1.Stats_Point > 0:
            pressing = button("+", 360, 210, 55, 50, 30, white, red, exiting)
            if pressing is True:
                player_1.increase_stats("endurance")

        button("Intelligence", 50, 265, 200, 50, 30, white, white)
        button(str(player_1.BattleIntelligence), 255, 265, 100, 50, 30, white, white)

        if player_1.Stats_Point > 0:
            pressing = button("+", 360, 265, 55, 50, 30, white, red, exiting)
            if pressing is True:
                player_1.increase_stats("intelligence")

        button("Willpower", 50, 320, 200, 50, 30, white, white)
        button(str(player_1.BattleWillpower), 255, 320, 100, 50, 30, white, white)

        if player_1.Stats_Point > 0:
            pressing = button("+", 360, 320, 55, 50, 30, white, red, exiting)
            if pressing is True:
                player_1.increase_stats("willpower")

        button("Dexterity", 50, 375, 200, 50, 30, white, white)
        button(str(player_1.BattleDexterity), 255, 375, 100, 50, 30, white, white)

        if player_1.Stats_Point > 0:
            pressing = button("+", 360, 375, 55, 50, 30, white, red, exiting)
            if pressing is True:
                player_1.increase_stats("dexterity")

        pygame.draw.rect(display, background, (640, 100, 270, 560))

        # displays the currently equipped items on the player and when this button is pressed allows the player to
        # change their equipment
        equipment_types = ["weapon", "head", "chest", "legs", "boots"]
        for i in range(5):
            if player_1.equipment[i][0] == "None":
                equipping = button("None", 650, 110 + (i * 110), 250, 100, 15, white, red, exiting)
                if equipping:
                    change_equipment(equipment_types[i])
            else:
                equipping = button(player_1.equipment[i][0], 650, 110 + (i * 110), 250, 100, 15, white, red, exiting)
                if equipping:
                    change_equipment(equipment_types[i])

        exit_button = button("Back", 1005, 330, 146, 75, 30, white, red, exiting)

        if exit_button is True:
            break

        pygame.display.update()
        clock.tick(60)


# the function which shows all item, skills and equipment the player owns
def inventory_screen():
    equipment_page = 0
    item_page = 0
    skill_page = 0

    # print(equipment_list)
    # print(item_list)
    # print(player_1.skills)

    list_of_equipment = []
    list_of_item = []
    list_of_skill = list(player_1.skills)

    split_list_of_equipment = []
    split_list_of_item = []
    split_list_of_skill = []

    for i in range(len(inventory)):
        temp = inventory[i]
        try:
            temp = equipment_list[equipment_name_list.index(temp[0])]
            list_of_equipment.append(temp)
        except:
            pass
        try:
            temp = list(item_list[item_name_list.index(temp[0])])
            temp[4] = inventory[i][1]
            list_of_item.append(temp)
        except:
            pass

    for i in range(len(list_of_skill)):
        for j in range(len(skill_list)):
            if list_of_skill[i] == skill_list[j][0]:
                list_of_skill[i] = skill_list[j]

    # print(list_of_equipment)
    # print(list_of_item)
    # print(list_of_skill)

    number = 0
    # distributes items and equipment and skills into three arrays in groups of 5
    for i in range(int(math.ceil(len(list_of_equipment) / 5)) + 1):
        split_list_of_equipment.append([])
        for j in range(5):
            try:
                split_list_of_equipment[i].append(list_of_equipment[number])
            except:
                split_list_of_equipment[i].append(["None", "None", "None", "None"])
            number += 1

    number = 0
    for i in range(int(math.ceil(len(list_of_item) / 5))):
        split_list_of_item.append([])
        for j in range(5):
            try:
                split_list_of_item[i].append(list_of_item[number])
            except:
                split_list_of_item[i].append(["None", "None", "None", "None", "None"])
            number += 1

    number = 0
    for i in range(int(math.ceil(len(list_of_skill) / 5))):
        split_list_of_skill.append([])
        for j in range(5):
            try:
                split_list_of_skill[i].append(list_of_skill[number])
            except:
                split_list_of_skill[i].append(["None", "None", "None", "None", "None"])
            number += 1

    while True:
        global clicked
        clicked = False
        display.fill(background)
        pygame.draw.rect(display, black, (0, 0, 1004, 804))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
        button("Equipment", 50, 50, 200, 50, 15, white, white)

        # Displays the equipment in groups of 5
        for i in range(5):
            if split_list_of_equipment[equipment_page][i][0] != "None":
                # if the mouse is within the bound, will display the stats for the equipment
                button(split_list_of_equipment[equipment_page][i][0], 50, 100 + (i * 50), 200, 50, 15, white, red)
                if 50 < mx < 250 and 100 + (i * 50) < my < 150 + (i * 50):
                    draw_stat_name(50, 450, 150, 50, 20)
                    button(str(split_list_of_equipment[equipment_page][i][1]), 300, 450, 100, 50, 20, white, white)
                    if "strength" not in split_list_of_equipment[equipment_page][i][2]:
                        button("0", 200, 450, 50, 50, 20, white, white)
                    else:
                        button(str(split_list_of_equipment[equipment_page][i][3][split_list_of_equipment[
                            equipment_page][i][2].index("strength")]), 200, 450, 50, 50, 20, white, white)

                    if "endurance" not in split_list_of_equipment[equipment_page][i][2]:
                        button("0", 200, 500, 50, 50, 20, white, white)
                    else:
                        button(str(split_list_of_equipment[equipment_page][i][3][split_list_of_equipment[
                            equipment_page][i][2].index("endurance")]), 200, 500, 50, 50, 20, white, white)

                    if "intelligence" not in split_list_of_equipment[equipment_page][i][2]:
                        button("0", 200, 550, 50, 50, 20, white, white)
                    else:
                        button(str(split_list_of_equipment[equipment_page][i][3][split_list_of_equipment[
                            equipment_page][i][2].index("intelligence")]), 200, 550, 50, 50, 20, white, white)

                    if "willpower" not in split_list_of_equipment[equipment_page][i][2]:
                        button("0", 200, 600, 50, 50, 20, white, white)
                    else:
                        button(str(split_list_of_equipment[equipment_page][i][3][split_list_of_equipment[
                            equipment_page][i][2].index("willpower")]), 200, 600, 50, 50, 20, white, white)

                    if "dexterity" not in split_list_of_equipment[equipment_page][i][2]:
                        button("0", 200, 650, 50, 50, 20, white, white)
                    else:
                        button(str(split_list_of_equipment[equipment_page][i][3][split_list_of_equipment[
                            equipment_page][i][2].index("dexterity")]), 200, 650, 50, 50, 20, white, white)
            else:
                button(split_list_of_equipment[equipment_page][i][0], 50, 100 + (i * 50), 200, 50, 15, white, white)

        button("Items", 300, 50, 200, 50, 15, white, white)
        for i in range(5):
            if split_list_of_item[item_page][i][0] != "None":
                button(split_list_of_item[item_page][i][0], 300, 100 + (i * 50), 200, 50, 15, white, red)
                if 300 < mx < 500 and 100 + (i * 50) < my < 150 + (i * 50):
                    button("Increases", 50, 450, 200, 50, 20, white, white)
                    if len(split_list_of_item[item_page][i][2]) <= 4:
                        for j in range(len(split_list_of_item[item_page][i][2])):
                            button((str(split_list_of_item[item_page][i][2][j]) + " by " +
                                    str(split_list_of_item[item_page][i][3][j])), 50,
                                   505 + (j * 55), 200, 50, 20, white, white)
                    else:
                        for j in range(4):
                            button((str(split_list_of_item[item_page][i][2][j]) + " by " +
                                    str(split_list_of_item[item_page][i][3][j])), 50,
                                   505 + (j * 55), 200, 50, 20, white, white)
                        for j in range(4, 7):
                            button((str(split_list_of_item[item_page][i][2][j]) + " by " +
                                    str(split_list_of_item[item_page][i][3][j])),
                                   255, 505 + ((j - 4) * 55), 200, 50, 20, white, white)
                    button("Held: " + str(split_list_of_item[item_page][i][4]), 255, 450, 200, 50, 20, white, white)

            else:
                button(split_list_of_item[item_page][i][0], 300, 100 + (i * 50), 200, 50, 15, white, white)

        button("Skills", 550, 50, 200, 50, 15, white, white)
        for i in range(5):
            if split_list_of_skill[skill_page][i][0] != "None":
                button(split_list_of_skill[skill_page][i][0], 550, 100 + (i * 50), 200, 50, 15, white, red)
                if 550 < mx < 750 and 100 + (i * 50) < my < 150 + (i * 50):
                    skill_display = []
                    skill_info = skill_list[player_skill_list.index(split_list_of_skill[skill_page][i][0])]
                    skill_info_split = skill_info[5].split()
                    temp = skill_info_split[0]

                    skill_info_split.pop(0)
                    if skill_info_split:
                        empty = True
                    while empty:

                        if len(temp) <= 24:
                            temp = temp + " " + skill_info_split[0]
                            skill_info_split.pop(0)
                        else:
                            skill_display.append(temp)
                            temp = skill_info_split[0]
                            skill_info_split.pop(0)
                        if not skill_info_split:
                            skill_display.append(temp)
                            break

                    for j in range(len(skill_display)):
                        button(str(skill_display[j]), 50, 450 + (j * 50), 350, 50, 20, white, white)
                    button(str("Skill Cost: " + str(skill_info[4]) + " MP"), 500, 450, 350, 50, 20,
                           white, white)
            else:
                button(split_list_of_skill[skill_page][i][0], 550, 100 + (i * 50), 200, 50, 15, white, white)

        # will allow all three types to change pages and see different groups of item/equipment/skills
        try:
            equipment_page += button("Next", 150, 350, 100, 50, 20, white, red, page_change)
        except TypeError:
            equipment_page = equipment_page
        try:
            item_page += button("Next", 400, 350, 100, 50, 20, white, red, page_change)
        except TypeError:
            item_page = item_page
        try:
            skill_page += button("Next", 650, 350, 100, 50, 20, white, red, page_change)
        except TypeError:
            skill_page = skill_page

        try:
            equipment_page -= button("Back", 50, 350, 100, 50, 20, white, red, page_change)
        except TypeError:
            equipment_page = equipment_page
        try:
            item_page -= button("Back", 300, 350, 100, 50, 20, white, red, page_change)
        except TypeError:
            item_page = item_page
        try:
            skill_page -= button("Back", 550, 350, 100, 50, 20, white, red, page_change)
        except TypeError:
            skill_page = skill_page

        # Ensures the page does not go out of range and cause errors
        if equipment_page < 0:
            equipment_page = 0
        if item_page < 0:
            item_page = 0
        if skill_page < 0:
            skill_page = 0

        if equipment_page > len(split_list_of_equipment) - 1:
            equipment_page = len(split_list_of_equipment) - 1
        if item_page > len(split_list_of_item) - 1:
            item_page = len(split_list_of_item) - 1
        if skill_page > len(split_list_of_skill) - 1:
            skill_page = len(split_list_of_skill) - 1

        sorting = button("Inventory sort", 780, 50, 200, 50, 20, white, red, selecting)
        if sorting:
            split_list_of_equipment, split_list_of_item, split_list_of_skill = sort_inventory(inventory)

        exit_button = button("Back", 1005, 330, 146, 75, 30, white, red, exiting)

        if exit_button is True:
            break
        pygame.display.update()
        clock.tick(60)


# the screen that allows the player to make purchases to increase their power
def shop_screen():
    global inventory

    Text_font = pygame.font.Font("freesansbold.ttf", 20)
    while True:
        global shop_list
        global clicked
        clicked = False
        skill_display = []
        display.fill(background)
        pygame.draw.rect(display, black, (0, 0, 1004, 804))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        button("", 55, 710, 300, 20, 1, red, red)
        button("HP", 25, 710, 30, 20, 20, white, white)

        button("", 55, 710, ((player_1.BattleHP / player_1.HP) * 300), 20, 20, green, green)
        text_surf, text_rect = text_objects((str(int(player_1.BattleHP)) + "/" + str(player_1.HP)), Text_font)
        text_rect.center = (205, 720)
        display.blit(text_surf, text_rect)

        # Equipment shop
        pygame.draw.rect(display, background, (45, 45, 365, 335))

        button("Equipment", 50, 50, 250, 50, 20, white, white)
        button("cost", 305, 50, 100, 50, 20, white, white)
        try:
            for i in range(5):
                if shop_list[0][i][0] != "None":
                    selecting_item = button(str(shop_list[0][i][0]), 50, 105 + (i * 55), 250, 50, 15, white,
                                            red, selecting)
                    button(str(shop_list[0][i][4]), 305, 105 + (i * 55), 100, 50, 20, white, white)
                    if 50 < mx < 300 and 105 + (i * 55) < my < 155 + (i * 55):
                        draw_stat_name(50, 400, 150, 50, 20)
                        if "strength" not in shop_list[0][i][2]:
                            button("0", 200, 400, 50, 50, 20, white, white)
                        else:
                            button(str(shop_list[0][i][3][shop_list[0][i][2].index("strength")]),
                                   200, 400, 50, 50, 20, white, white)

                        if "endurance" not in shop_list[0][i][2]:
                            button("0", 200, 450, 50, 50, 20, white, white)
                        else:
                            button(str(shop_list[0][i][3][shop_list[0][i][2].index("endurance")]),
                                   200, 450, 50, 50, 20, white, white)

                        if "intelligence" not in shop_list[0][i][2]:
                            button("0", 200, 500, 50, 50, 20, white, white)
                        else:
                            button(str(shop_list[0][i][3][shop_list[0][i][2].index("intelligence")]),
                                   200, 500, 50, 50, 20, white, white)

                        if "willpower" not in shop_list[0][i][2]:
                            button("0", 200, 550, 50, 50, 20, white, white)
                        else:
                            button(str(shop_list[0][i][3][shop_list[0][i][2].index("willpower")]),
                                   200, 550, 50, 50, 20, white, white)

                        if "dexterity" not in shop_list[0][i][2]:
                            button("0", 200, 600, 50, 50, 20, white, white)
                        else:
                            button(str(shop_list[0][i][3][shop_list[0][i][2].index("dexterity")]),
                                   200, 600, 50, 50, 20, white, white)

                if selecting_validation(selecting_item):
                    cost = shop_list[0][i][4]
                    if player_1.BattleHP - cost >= 1:
                        player_1.BattleHP -= cost
                        inventory.append([shop_list[0][i][0], 1])
                        inventory = compile_inventory(inventory)
                        shop_list[0][i][0] = "None"

        except (IndexError, UnboundLocalError):
            pass

        # Skill shop
        pygame.draw.rect(display, background, (545, 45, 365, 335))
        button("Skill", 550, 50, 250, 50, 20, white, white)
        button("cost", 805, 50, 100, 50, 20, white, white)
        try:
            for i in range(5):
                if shop_list[1][i][0] != "None":
                    selecting_item = button(shop_list[1][i][0], 550, 105 + (i * 55), 250, 50, 15, white, red, selecting)
                    button(str(shop_list[1][i][1]), 805, 105 + (i * 55), 100, 50, 20, white, white)

                    if 550 < mx < 800 and 105 + (i * 55) < my < 155 + (i * 55):
                        skill_info = skill_list[player_skill_list.index(shop_list[1][i][0])]
                        skill_info_split = skill_info[5].split()
                        temp = skill_info_split[0]

                        skill_info_split.pop(0)
                        if skill_info_split:
                            empty = True
                        while empty:

                            if len(temp) <= 24:
                                temp = temp + " " + skill_info_split[0]
                                skill_info_split.pop(0)
                            else:
                                skill_display.append(temp)
                                temp = skill_info_split[0]
                                skill_info_split.pop(0)
                            if not skill_info_split:
                                skill_display.append(temp)
                                break

                        for j in range(len(skill_display)):
                            button(str(skill_display[j]), 50, 400 + (j * 50), 350, 50, 20, white, white)
                        button(str("Skill Cost: " + str(skill_info[4]) + " MP"), 50, 400 + ((j + 1) * 50), 350, 50, 20,
                               white, white)

                    if selecting_validation(selecting_item):
                        cost = shop_list[1][i][1]
                        if player_1.BattleHP - cost >= 1:
                            if shop_list[1][i][0] not in player_1.skills:
                                player_1.BattleHP -= cost
                                player_1.skills.append(shop_list[1][i][0])
                                shop_list[1][i][0] = "None"

        except IndexError:
            pass

        # Consumable shop
        pygame.draw.rect(display, background, (545, 395, 365, 335))
        button("Consumable", 550, 400, 250, 50, 20, white, white)
        button("cost", 805, 400, 100, 50, 20, white, white)
        try:
            for i in range(5):
                if shop_list[2][i][0] != "None":
                    selecting_item = button(shop_list[2][i][0], 550, 455 + (i * 55), 250, 50, 20, white, red, selecting)
                    button(str(shop_list[2][i][4]), 805, 455 + (i * 55), 100, 50, 20, white, white)

                    if 550 < mx < 800 and 455 + (i * 55) < my < 505 + (i * 55):
                        button("Increases", 50, 400, 200, 50, 20, white, white)

                        if len(shop_list[2][i][2]) <= 4:
                            for j in range(len(shop_list[2][i][2])):
                                button((str(shop_list[2][i][2][j]) + " by " + str(shop_list[2][i][3][j])), 50,
                                       455 + (j * 55), 200, 50, 20, white, white)
                        else:
                            for j in range(4):
                                button((str(shop_list[2][i][2][j]) + " by " + str(shop_list[2][i][3][j])), 50,
                                       455 + (j * 55), 200, 50, 20, white, white)
                            for j in range(4, 7):
                                button((str(shop_list[2][i][2][j]) + " by " + str(shop_list[2][i][3][j])),
                                       255, 455 + ((j - 4) * 55), 200, 50, 20, white, white)

                    if selecting_validation(selecting_item):
                        cost = shop_list[2][i][4]
                        if player_1.BattleHP - cost >= 1:
                            player_1.BattleHP -= cost
                            inventory.append([shop_list[2][i][0], 1])
                            inventory = compile_inventory(inventory)
                            shop_list[2][i][0] = "None"

        except IndexError:
            pass

        # this section allows the player to refresh the shop of all items and skills and equipment
        refresh = button("Refresh Shop - 10% HP Cost", 50, 750, 300, 25, 20, white, red, selecting)
        if selecting_validation(refresh):
            temp = player_1.BattleHP
            cost = math.ceil(player_1.HP / 10)
            # this prevents the player from player from using all their HP when refreshing
            if temp - cost >= 1:
                player_1.BattleHP -= math.ceil(player_1.HP / 10)
                shop_list = refresh_shop()

        exit_button = button("Back", 1005, 330, 146, 75, 30, white, red, exiting)

        if exit_button is True:
            break

        pygame.display.update()
        clock.tick(60)
    return shop_list


# This function allows the player to save their progress
def save(discovered_tile, map_tile_ID, map_mask, save_file_name="player save file.txt"):
    global shop_list
    global boss_number
    # information to be saved is first saved to an array
    respawn_info = [player_icon.respawn_x, player_icon.respawn_y, player_icon.respawn]
    saving_list = [player_1.get_base_stats(), player_1.get_skill(), player_1.get_equipment(), inventory,
                   discovered_tile, map_tile_ID, shop_list, floor_number, player_1.BattleHP, player_1.BattleMP,
                   player_icon.icon_name, boss_number, respawn_info]

    # this list is then saved to a text file using pickle
    save_file = open(save_file_name, "wb")
    pickle.dump(saving_list, save_file)
    save_file.close()


# This function allows the player to load their previous progress
def load_game(load_file="player save file.txt"):
    global discovered_tile
    global player_1
    global inventory
    global floor_number
    global shop_list
    global player_icon
    global boss_number
    map_list = [["None" for i in range(10)] for j in range(8)]

    map_mask = [["None" for i in range(10)] for j in range(8)]

    # the file is unpickled and the data is retrieved
    save_file = open(load_file, "rb")
    load_list = pickle.load(save_file)
    stats = load_list[0]
    player_skill = load_list[1]
    player_equipment = load_list[2]
    inventory = load_list[3]
    discovered_tile = load_list[4]
    map_tile_ID = load_list[5]
    shop_list = load_list[6]
    floor_number = load_list[7]
    boss_number = load_list[11]

    player_1 = player(stats[0], stats[1], stats[2], stats[3], stats[4], player_skill, player_equipment)
    player_1.reset_stats()

    player_1.BattleHP = load_list[8]
    player_1.BattleMP = load_list[9]

    icon_name = load_list[10]

    player_icon = player_icons(0, 0, icon_name)

    player_icon.respawn_x, player_icon.respawn_y, player_icon.respawn = load_list[12]

    for y in range(8):
        for x in range(10):
            imagename = (r"tile list png" + chr(92) + map_tile_ID[y][x])
            image = pygame.image.load(imagename)
            map_list[y][x] = image

    map_surface = pygame.Surface((width, height))
    map_surface.fill(background)

    for y in range(8):
        for x in range(10):
            map_surface.blit(map_list[y][x], (2 + 100 * x, 2 + 100 * y))

    map_mask = pygame.mask.from_threshold(map_surface, (62, 39, 35), (50, 20, 25, 100))

    # if the player had reached the respawn point then the player is spawned at the respawn point instead of the start
    player_icon.player_spawn(map_tile_ID)
    player_icon.player_goal(map_tile_ID)
    if player_icon.get_respawn():
        player_icon.x = player_icon.respawn_x
        player_icon.y = player_icon.respawn_y

    return main(map_list, map_tile_ID, map_mask, shop_list)


# prevents a Type error that occurs occasionally when the generate map functions return a None
def recursive_exception_map():
    try:
        map_list, map_tile_ID, map_mask = generate_map(tile_name_list)
        return map_list, map_tile_ID, map_mask
    except TypeError:
        # If there was an error the function calls itself until there isn't an error
        return recursive_exception_map()


# This function is the main game loop while running
def main(map_list, map_tile_ID, map_mask, shop_list):
    global discovered_tile
    global floor_number
    global boss_number

    # as long as the player has health points the game will continue
    while player_1.BattleHP > 0:
        display.fill(background)
        # Tracks for keyboard input
        keys = pygame.key.get_pressed()
        global clicked
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # checks if the mouse has been pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        if keys[pygame.K_ESCAPE]:
            break

        # if space is pressed the floor increments by one and a new map if generated
        if keys[pygame.K_SPACE]:
            map_list, map_tile_ID, map_mask = recursive_exception_map()
            player_icon.player_spawn(map_tile_ID)
            player_icon.player_goal(map_tile_ID)
            player_icon.player_respawn(map_tile_ID)
            discovered_tile = [[False for i in range(10)] for j in range(8)]
            floor_number += 1
            player_1.Stats_Point += random.randint(1, 5)
            shop_list = refresh_shop()

        if keys[pygame.K_r]:
            discovered_tile = [[True for i in range(10)] for j in range(8)]

        if keys[pygame.K_i]:
            print(inventory)

        if keys[pygame.K_c]:
            enemy_call(0)

        # keys to allow movement on the map
        if keys[pygame.K_LEFT]:
            temp_loc = (player_icon.x - 3, player_icon.y)
            if collision_detect(map_mask, temp_loc):
                pass
            else:
                player_icon.move("Left")

        if keys[pygame.K_RIGHT]:
            temp_loc = (player_icon.x + 3, player_icon.y)
            if collision_detect(map_mask, temp_loc):
                pass
            else:
                player_icon.move("Right")

        if keys[pygame.K_UP]:
            temp_loc = (player_icon.x, player_icon.y - 3)
            if collision_detect(map_mask, temp_loc):
                pass
            else:
                player_icon.move("Up")

        if keys[pygame.K_DOWN]:
            temp_loc = (player_icon.x, player_icon.y + 3)
            if collision_detect(map_mask, temp_loc):
                pass
            else:
                player_icon.move("Down")

        # blits the map onto the screen
        for y in range(8):
            for x in range(10):
                display.blit(map_list[y][x], (2 + 100 * x, 2 + 100 * y))

        button("Status", 1005, 10, 146, 75, 30, white, red, status_screen)
        button("Inventory", 1005, 90, 146, 75, 30, white, red, inventory_screen)

        button("Floor", 1005, 330, 146, 50, 50, background, background, colour=white)

        shop_selecting = button("Shop", 1005, 170, 146, 75, 30, white, red, selecting)
        if selecting_validation(shop_selecting):
            shop_screen()

        # saves the current state of the game to a text file
        save_selecting = button("Save", 1005, 250, 146, 75, 30, white, red, selecting)
        if selecting_validation(save_selecting):
            save(discovered_tile, map_tile_ID, map_mask)
            display.fill(background)
            # gives the player a prompt that a successful save has happened
            button("Saved", 0, 200, width, 50, 100, background, background, None, red)
            pygame.display.update()
            pygame.time.wait(1000)

        # if the player is on a boss floor then the floor number is displayed as red
        if (floor_number % 5) == 0:
            button(str(floor_number), 1005, 380, 146, 146, 75, background, background, colour=red)
        else:
            button(str(floor_number), 1005, 380, 146, 146, 75, background, background, colour=white)

        player_icon.draw_player()
        uncovering(discovered_tile)
        # if the player icon's x and y coordinate is within the bounds of the goal then
        # a new map is generated and the player is rewarded one status point
        # if the map floor number was a multiple of 5 then a boss enemy will be spawned to battle the player
        if (player_icon.goal_x - 15) < player_icon.x < (player_icon.goal_x + 15) and (
                player_icon.goal_y - 15) < player_icon.y < (player_icon.goal_y + 15):
            if (floor_number % 5) == 0:
                battle(True)
                player_1.BattleHP += player_1.HP // 10
                player_1.BattleMP += player_1.MP // 10
                if player_1.BattleHP > player_1.HP:
                    player_1.BattleHP = player_1.HP
                if player_1.BattleMP > player_1.MP:
                    player_1.BattleMP = player_1.MP
                boss_number += 1
                if boss_number >= len(boss_list):
                    boss_number = 0
            floor_number += 1
            player_1.Stats_Point += random.randint(1, 5)
            shop_list = refresh_shop()
            map_list, map_tile_ID, map_mask = recursive_exception_map()
            # updates the goal and spawn and respawn point for the player on the new map
            player_icon.player_spawn(map_tile_ID)
            player_icon.player_goal(map_tile_ID)
            player_icon.player_respawn(map_tile_ID)
            # recovers the map so the player can explore again
            discovered_tile = [[False for i in range(10)] for j in range(8)]

        # checks if the player has reached the respawn point
        if (player_icon.respawn_x - 15) < player_icon.x < (player_icon.respawn_x + 15) and (
                player_icon.respawn_y - 15) < player_icon.y < (player_icon.respawn_y + 15):
            # if the player had not yet reached this point for that floor then a respawn save is created
            if not player_icon.respawn:
                player_icon.respawn = True
                tile_pos = [0, 0]
                # changes the tile on the map to show the respawn point is active
                for i in range(8):
                    if "tile respawn-inactive.png" in map_tile_ID[i]:
                        tile_pos[0] = map_tile_ID[i].index("tile respawn-inactive.png")
                        tile_pos[1] = i

                map_tile_ID[tile_pos[1]][tile_pos[0]] = "tile respawn-active.png"
                map_list[tile_pos[1]][tile_pos[0]] = pygame.image.load((r"tile list png" +
                                                                        chr(92) + tile_name_list[46]))
                # the save for the current map situation is created
                save(discovered_tile, map_tile_ID, map_mask, "respawn save file.txt")

        pygame.display.update()
        clock.tick(60)


# enemy = enemy_generator(7, 7)
# enemy.display_stats()
menu()
