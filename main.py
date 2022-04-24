from map_generation import generate_map, tile_name_list
import math
import global_file
from battle_logic import calculation, status_check, battle_calc_info, battle_info_draw
import random
import display_file
import pickle
import pygame


global clicked

clicked = False
pygame.init()

white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (50, 200, 255)

width = global_file.width
height = global_file.height
half_width = width / 2
half_height = height / 2
icon_1 = (14, 209, 69)
icon_2 = (218, 199, 63)
icon_3 = (128, 0, 255)


display = display_file.display

clock = pygame.time.Clock()
Game = True

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





def collision_detect(map_mask, temp_loc):
    offset = (temp_loc[0] + 2, temp_loc[1] + 2)
    result = map_mask.overlap(player_icon.icon_mask, offset)

    # if the result is true then a collision has occurred and the player should not be allowed in that direction
    if result:
        return True
    else:
        return False


global player_icon
global enemy
global shop_list
global inventory

inventory = [["Health Potion", 3], ["Mana Potion", 3]]


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
        enemy_call()

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
        self.Statuses = [[False, 0, 5], [False, 0], [False, 0, 5]]
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

        self.status_point = 5

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
        self.status_point -= 1

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
        self.Statuses = [[False, 0, 5], [False, 0], [False, 0, 5]]
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
    global player_icon
    # global global_file.floor_number
    global discovered_tile
    global boss_number
    boss_number = 0
    # global_file.floor_number = 1
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
        selecting_icon = button("Base", 100, 400, 100, 100, 30, icon_1, white, selecting)
        if selecting_validation(selecting_icon):
            selecting_icon = icon_list[0]
            player_1 = player(10, 10, 10, 10, 10)
            player_1.status_point += 10
            break

        selecting_icon = button("Mage", 300, 400, 100, 100, 30, icon_2, white, selecting)
        if selecting_validation(selecting_icon):
            selecting_icon = icon_list[1]
            player_1 = player(10, 10, 15, 15, 10)
            break

        selecting_icon = button("Warrior", 500, 400, 100, 100, 30, icon_3, white, selecting)
        if selecting_validation(selecting_icon):
            selecting_icon = icon_list[2]
            player_1 = player(15, 15, 10, 10, 10)
            break

        exit_button = button("Back", 1005, 330, 146, 75, 30, white, red, exiting)
        if exit_button is True:
            menu()

        pygame.display.update()
        clock.tick(60)

    for i in range(len(skill_list)):
        all_skill_list.append(skill_list[i][0])

    # this part generates the base player and their icon on to the map
    # player_1 = player(100, 100, 100, 100, 100, skills=all_skill_list)
    global_file.player_1 = player_1
    global_file.player_1.reset_stats()

    player_icon = player_icons(0, 0, selecting_icon)

    # generates the initial start, end and respawn points for the player
    player_icon.player_spawn(map_tile_ID)
    player_icon.player_goal(map_tile_ID)
    player_icon.player_respawn(map_tile_ID)

    return map_list, map_tile_ID, map_mask


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
    temp_list = global_file.player_1.get_BattleStats()
    # increase the stats of the enemy to scale with the player strength
    average = sum(temp_list) // len(temp_list) // 5
    temp = (global_file.floor_number // 40) * 100
    if global_file.floor_number <= 3:
        temp = (global_file.floor_number * 2) - 6
    print(temp)
    enemy[1] = abs(int(enemy[1]) + average + temp)
    enemy[2] = abs(int(enemy[2]) + average + temp)
    enemy[3] = abs(int(enemy[3]) + average + temp)
    enemy[4] = abs(int(enemy[4]) + average + temp)
    enemy[5] = abs(int(enemy[5]) + average + temp)

    enemy = enemies(enemy[1], enemy[2], enemy[3], enemy[4], enemy[5], enemy[0], enemy[6])
    global_file.enemy_1 = enemy
    return global_file.enemy_1


# Function to ensure damage is not in the negatives



# The function which checks if an action should be critical
def CriticalCalc(skill_multi, turn):
    number = random.randint(0, 100)
    # If the generated number is less than or equal to the critical chance of the player or enemy
    # Then the effect of the action is doubled
    if turn == 0:
        crit = global_file.player_1.CritChance()
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
    if global_file.player_1.BattleHP <= 0:
        print("player dead")
        Game = False
        game_over()
    elif enemy.BattleHP <= 0:
        print("Enemy dead")

        Game = False
        global_file.player_1.reset_stats()
        global_file.player_1.BattleHP += enemy.HP / 10
        if global_file.player_1.BattleHP > global_file.player_1.HP:
            global_file.player_1.BattleHP = global_file.player_1.HP

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
    temp = global_file.player_1.BattleMP
    cost = skill[4]
    if (temp - cost) < 0:
        return False
    else:
        global_file.player_1.BattleMP -= cost
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


# This is the function that is called when a battle is needed
def battle(boss=False):
    global enemy
    global boss_number
    # global global_file.floor_number
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
        temp_list = global_file.player_1.get_BattleStats()

        average = sum(temp_list) // len(temp_list) // 5

        count = (global_file.floor_number // 5) - (boss_number + 1)

        enemy[1] = int(enemy[1]) + average + count
        enemy[2] = int(enemy[2]) + average + count
        enemy[3] = int(enemy[3]) + average + count
        enemy[4] = int(enemy[4]) + average + count
        enemy[5] = int(enemy[5]) + average + count
        print("generated")

        enemy = enemies(enemy[1], enemy[2], enemy[3], enemy[4], enemy[5], enemy[0], enemy[6])

    print(enemy.display_stats())

    # This section decides who gets the first move
    if global_file.player_1.BattleDexterity > enemy.BattleDexterity:
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
                    global_file.player_1.BattleHP = 0
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

            # player_action = "Attack"
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

    player_Health = round(global_file.player_1.BattleHP / global_file.player_1.HP) * 100
    player_Mana = round(global_file.player_1.BattleMP / global_file.player_1.MP) * 100
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

        for x in global_file.player_1.Statuses:
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

    for x in global_file.player_1.Statuses:
        if True not in x:
            if status_list:
                print("status")
                if random.randint(0, 5) == 0:
                    for i in range(len(status_list)):
                        if enemy_MPcheck(status_list[i]):
                            return status_list[i]

    for x in global_file.player_1.Statuses:
        if True in x:
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

    for i in range(3):
        temp_skill = total_skill_list[random.randint(0, len(total_skill_list) - 1)]
        if enemy_MPcheck(temp_skill):
            return temp_skill
    else:
        return ['Attack', ['HP', '-', 'phy'], 1.0, 'enemy', 0, 'Basic_Attack']


def fight():
    print("action fight")


# this function allows the player to select a skill they own
def skill_selection():
    total_skills = len(global_file.player_1.skills)
    skill_number = 0
    split_skill = int(math.ceil(total_skills / 5))
    split_skill_list = []
    selected_skill = None
    page = 0
    try:
        global_file.player_1.skills.remove("Attack")
    except ValueError:
        pass

    # this for loop splits the skills owned by the player into a 2d array so they are on different pages
    for i in range(split_skill):
        split_skill_list.append([])
        for j in range(5):
            try:
                split_skill_list[i].append(str(global_file.player_1.skills[skill_number]))
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
            global_file.player_1.BattleHP += value[i]
            if global_file.player_1.BattleHP > global_file.player_1.HP:
                global_file.player_1.BattleHP = global_file.player_1.HP
        elif affects[i] == "MP":
            global_file.player_1.BattleMP += value[i]
            if global_file.player_1.BattleMP > global_file.player_1.MP:
                global_file.player_1.BattleMP = global_file.player_1.MP
        elif affects[i] == "Attack":
            global_file.player_1.BattleStrength += value[i]
        elif affects[i] == "Endurance":
            global_file.player_1.BattleEndurance += value[i]
        elif affects[i] == "Intelligence":
            global_file.player_1.BattleIntelligence += value[i]
        elif affects[i] == "Willpower":
            global_file.player_1.BattleWillpower += value[i]
        elif affects[i] == "Dexterity":
            global_file.player_1.BattleDexterity += value[i]
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
            global_file.player_1.change_equipment(equipment_list[i])
            break


# A function that allows the player to select what equipment they want to change
# This function is called from the status screen function
def change_equipment(type_of_equip):
    page = 0
    while True:
        global clicked
        clicked = False
        display.fill(global_file.background)
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
            if global_file.player_1.equipment[1][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(global_file.player_1.equipment[1][0], 650, 110, 250, 100, 15, white, white)

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
            if global_file.player_1.equipment[2][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(global_file.player_1.equipment[2][0], 650, 110, 250, 100, 15, white, white)

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
            if global_file.player_1.equipment[3][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(global_file.player_1.equipment[3][0], 650, 110, 250, 100, 15, white, white)

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
            if global_file.player_1.equipment[4][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(global_file.player_1.equipment[4][0], 650, 110, 250, 100, 15, white, white)

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
            if global_file.player_1.equipment[0][0] == "None":
                button("None", 650, 110, 250, 100, 15, white, white)
            else:
                button(global_file.player_1.equipment[0][0], 650, 110, 250, 100, 15, white, white)

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
    list_of_skill = list(global_file.player_1.skills)

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
    global_file.player_1.reset_stats()
    while True:
        global clicked
        clicked = False
        display.fill(global_file.background)
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
        button(str(global_file.player_1.status_point), 360, 100, 55, 50, 30, white, white)

        button("Strength", 50, 155, 200, 50, 30, white, white)

        # allows the player to use their points to increase their base stats of choice
        button(str(global_file.player_1.BattleStrength), 255, 155, 100, 50, 30, white, white)
        if global_file.player_1.status_point > 0:
            pressing = button("+", 360, 155, 55, 50, 30, white, red, exiting)
            if pressing is True:
                global_file.player_1.increase_stats("strength")

        button("Endurance", 50, 210, 200, 50, 30, white, white)
        button(str(global_file.player_1.BattleEndurance), 255, 210, 100, 50, 30, white, white)

        if global_file.player_1.status_point > 0:
            pressing = button("+", 360, 210, 55, 50, 30, white, red, exiting)
            if pressing is True:
                global_file.player_1.increase_stats("endurance")

        button("Intelligence", 50, 265, 200, 50, 30, white, white)
        button(str(global_file.player_1.BattleIntelligence), 255, 265, 100, 50, 30, white, white)

        if global_file.player_1.status_point > 0:
            pressing = button("+", 360, 265, 55, 50, 30, white, red, exiting)
            if pressing is True:
                global_file.player_1.increase_stats("intelligence")

        button("Willpower", 50, 320, 200, 50, 30, white, white)
        button(str(global_file.player_1.BattleWillpower), 255, 320, 100, 50, 30, white, white)

        if global_file.player_1.status_point > 0:
            pressing = button("+", 360, 320, 55, 50, 30, white, red, exiting)
            if pressing is True:
                global_file.player_1.increase_stats("willpower")

        button("Dexterity", 50, 375, 200, 50, 30, white, white)
        button(str(global_file.player_1.BattleDexterity), 255, 375, 100, 50, 30, white, white)

        if global_file.player_1.status_point > 0:
            pressing = button("+", 360, 375, 55, 50, 30, white, red, exiting)
            if pressing is True:
                global_file.player_1.increase_stats("dexterity")

        pygame.draw.rect(display, global_file.background, (640, 100, 270, 560))

        # displays the currently equipped items on the player and when this button is pressed allows the player to
        # change their equipment
        equipment_types = ["weapon", "head", "chest", "legs", "boots"]
        for i in range(5):
            if global_file.player_1.equipment[i][0] == "None":
                equipping = button("None", 650, 110 + (i * 110), 250, 100, 15, white, red, exiting)
                if equipping:
                    change_equipment(equipment_types[i])
            else:
                equipping = button(global_file.player_1.equipment[i][0], 650, 110 + (i * 110), 250, 100, 15, white, red,
                                   exiting)
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
    list_of_skill = list(global_file.player_1.skills)

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
        display.fill(global_file.background)
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
        display.fill(global_file.background)
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

        button("", 55, 710, ((global_file.player_1.BattleHP / global_file.player_1.HP) * 300), 20, 20, green, green)
        text_surf, text_rect = text_objects(f"{global_file.player_1.BattleHP}/{global_file.player_1.HP}", Text_font)
        text_rect.center = (205, 720)
        display.blit(text_surf, text_rect)

        # Equipment shop
        pygame.draw.rect(display, global_file.background, (45, 45, 365, 335))

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
                    if global_file.player_1.BattleHP - cost >= 1:
                        global_file.player_1.BattleHP -= cost
                        inventory.append([shop_list[0][i][0], 1])
                        inventory = compile_inventory(inventory)
                        shop_list[0][i][0] = "None"

        except (IndexError, UnboundLocalError):
            pass

        # Skill shop
        pygame.draw.rect(display, global_file.background, (545, 45, 365, 335))
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
                        if global_file.player_1.BattleHP - cost >= 1:
                            if shop_list[1][i][0] not in global_file.player_1.skills:
                                global_file.player_1.BattleHP -= cost
                                global_file.player_1.skills.append(shop_list[1][i][0])
                                shop_list[1][i][0] = "None"

        except IndexError:
            pass

        # Consumable shop
        pygame.draw.rect(display, global_file.background, (545, 395, 365, 335))
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
                        if global_file.player_1.BattleHP - cost >= 1:
                            global_file.player_1.BattleHP -= cost
                            inventory.append([shop_list[2][i][0], 1])
                            inventory = compile_inventory(inventory)
                            shop_list[2][i][0] = "None"

        except IndexError:
            pass

        # this section allows the player to refresh the shop of all items and skills and equipment
        refresh = button("Refresh Shop - 10% HP Cost", 50, 750, 300, 25, 20, white, red, selecting)
        if selecting_validation(refresh):
            temp = global_file.player_1.BattleHP
            cost = math.ceil(global_file.player_1.HP / 10)
            # this prevents the player from player from using all their HP when refreshing
            if temp - cost >= 1:
                global_file.player_1.BattleHP -= math.ceil(global_file.player_1.HP / 10)
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
    saving_list = [global_file.player_1.get_base_stats(), global_file.player_1.get_skill(),
                   global_file.player_1.get_equipment(), inventory,
                   discovered_tile, map_tile_ID, shop_list, global_file.floor_number, global_file.player_1.BattleHP,
                   global_file.player_1.BattleMP,
                   player_icon.icon_name, boss_number, respawn_info]

    # this list is then saved to a text file using pickle
    save_file = open(save_file_name, "wb")
    pickle.dump(saving_list, save_file)
    save_file.close()


# This function allows the player to load their previous progress
def load_game(load_file="player save file.txt"):
    global discovered_tile
    # global global_file.player_1
    global inventory

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
    global_file.floor_number = load_list[7]
    boss_number = load_list[11]

    global_file.player_1 = player(stats[0], stats[1], stats[2], stats[3], stats[4], player_skill, player_equipment)
    global_file.player_1.reset_stats()

    global_file.player_1.BattleHP = load_list[8]
    global_file.player_1.BattleMP = load_list[9]

    icon_name = load_list[10]

    player_icon = player_icons(0, 0, icon_name)

    player_icon.respawn_x, player_icon.respawn_y, player_icon.respawn = load_list[12]

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

    global boss_number

    # as long as the player has health points the game will continue
    while global_file.player_1.BattleHP > 0:
        display.fill(global_file.background)
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
            global_file.floor_number += 1
            global_file.player_1.status_point += random.randint(1, 5)
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

        button("Floor", 1005, 330, 146, 50, 50, global_file.background, global_file.background, colour=white)

        shop_selecting = button("Shop", 1005, 170, 146, 75, 30, white, red, selecting)
        if selecting_validation(shop_selecting):
            shop_screen()

        # saves the current state of the game to a text file
        save_selecting = button("Save", 1005, 250, 146, 75, 30, white, red, selecting)
        if selecting_validation(save_selecting):
            save(discovered_tile, map_tile_ID, map_mask)
            display.fill(global_file.background)
            # gives the player a prompt that a successful save has happened
            button("Saved", 0, 200, width, 50, 100, global_file.background, global_file.background, None, red)
            pygame.display.update()
            pygame.time.wait(1000)

        # if the player is on a boss floor then the floor number is displayed as red
        if (global_file.floor_number % 5) == 0:
            button(str(global_file.floor_number), 1005, 380, 146, 146, 75, global_file.background,
                   global_file.background, colour=red)
        else:
            button(str(global_file.floor_number), 1005, 380, 146, 146, 75, global_file.background,
                   global_file.background, colour=white)

        player_icon.draw_player()
        display_file.uncovering(discovered_tile,player_icon.x, player_icon.y)
        # if the player icon's x and y coordinate is within the bounds of the goal then
        # a new map is generated and the player is rewarded one status point
        # if the map floor number was a multiple of 5 then a boss enemy will be spawned to battle the player
        if (player_icon.goal_x - 15) < player_icon.x < (player_icon.goal_x + 15) and (
                player_icon.goal_y - 15) < player_icon.y < (player_icon.goal_y + 15):
            if (global_file.floor_number % 5) == 0:
                battle(True)
                global_file.player_1.BattleHP += global_file.player_1.HP // 10
                global_file.player_1.BattleMP += global_file.player_1.MP // 10
                boss_number += 1
                if boss_number >= len(boss_list):
                    boss_number = 0
            global_file.floor_number += 1
            global_file.player_1.status_point += random.randint(1, 5)
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
