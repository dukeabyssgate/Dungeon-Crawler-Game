import global_file
import random
import pygame
#from main import button, text_objects, display

white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (50, 200, 255)


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
                    print("player", global_file.player_1.BattleHP)
                    if form == "mag":
                        damage = (global_file.player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.player_1.BattleStrength * multiplyer)
                    global_file.player_1.BattleHP = global_file.player_1.BattleHP + damageCheck(damage)
                    if global_file.player_1.BattleHP > global_file.player_1.HP:
                        global_file.player_1.BattleHP = global_file.player_1.HP
                        print("Overflow HP removed")
                else:
                    print("global_file.player_1", global_file.player_1.BattleHP)
                    if form == "mag":
                        damage = (global_file.player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.player_1.BattleStrength * multiplyer)
                    global_file.player_1.BattleHP = global_file.player_1.BattleHP - damageCheck(damage)
                battle_calc_info(turn, picked_skill, damage)
                print("player HP is", global_file.player_1.BattleHP)
            else:
                if effect == "+":
                    if form == "mag":
                        damage = (global_file.enemy_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.enemy_1.BattleStrength * multiplyer)
                    global_file.enemy_1.BattleHP = global_file.enemy_1.BattleHP + damageCheck(damage)
                    if global_file.enemy_1.BattleHP > global_file.enemy_1.HP:
                        global_file.enemy_1.BattleHP = global_file.enemy_1.HP
                        print("Overflow HP removed")
                else:
                    if form == "mag":
                        damage = (global_file.enemy_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.enemy_1.BattleStrength * multiplyer)
                    global_file.enemy_1.BattleHP = global_file.enemy_1.BattleHP - damageCheck(damage)
                battle_calc_info(turn, picked_skill, damage)
                print("global_file.enemy_1 HP is", global_file.enemy_1.BattleHP)

        elif action == "MP":
            if turn % 2 == 0:
                if effect == "+":
                    if form == "mag":
                        damage = (global_file.player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.player_1.BattleStrength * multiplyer)
                        temp = global_file.player_1.HP * (cost / 100)
                        print(temp, damage, cost)
                        if global_file.player_1.BattleHP - temp < 0:
                            damage = 0
                        else:
                            global_file.player_1.BattleHP -= temp
                    global_file.player_1.BattleMP = global_file.player_1.BattleMP + damageCheck(damage)
                    if global_file.player_1.BattleMP > global_file.player_1.MP:
                        global_file.player_1.BattleMP = global_file.player_1.MP
                        print("overflow MP released")
                else:
                    if form == "mag":
                        damage = (global_file.player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.player_1.BattleStrength * multiplyer)
                        temp = abs(damage * (cost / 100))
                        if global_file.player_1.BattleHP - temp < 0:
                            damage = 0
                        else:
                            global_file.player_1.BattleHP -= temp
                    global_file.player_1.BattleMP = global_file.player_1.BattleMP - damage
                    if global_file.player_1.BattleMP < 0:
                        global_file.player_1.BattleMP = 20
                battle_calc_info(turn, picked_skill, damage)
                print("player MP is", global_file.player_1.BattleMP)
            else:
                if effect == "+":
                    if form == "mag":
                        damage = (global_file.enemy_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.enemy_1.BattleStrength * multiplyer)
                        temp = abs(damage * (cost / 100))
                        if global_file.enemy_1.BattleHP - temp < 0:
                            damage = 0
                        else:
                            global_file.enemy_1.BattleHP -= temp
                    global_file.enemy_1.BattleMP = global_file.enemy_1.BattleMP + damageCheck(damage)
                    if global_file.enemy_1.BattleMP > global_file.enemy_1.MP:
                        global_file.enemy_1.BattleMP = global_file.enemy_1.MP
                        print("overflow MP released")
                else:
                    if form == "mag":
                        damage = (global_file.enemy_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.enemy_1.BattleStrength * multiplyer)
                        temp = abs(damage * (cost / 100))
                        if global_file.enemy_1.BattleHP - temp < 0:
                            damage = 0
                        else:
                            global_file.enemy_1.BattleHP -= temp
                    global_file.enemy_1.BattleMP = global_file.enemy_1.BattleMP - damage
                    if global_file.player_1.BattleMP < 0:
                        global_file.player_1.BattleMP = 20
                battle_calc_info(turn, picked_skill, damage)
                print("global_file.enemy_1 MP is", global_file.enemy_1.BattleMP)

        elif action == "Attack":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.player_1.BattleStrength = global_file.player_1.BattleStrength \
                                                          + (global_file.player_1.strength * multiplyer)
                else:
                    global_file.player_1.BattleStrength = global_file.player_1.BattleStrength \
                                                          - (global_file.player_1.strength * multiplyer)
                    global_file.player_1.Battle_stats_check()
                print("player Strength is", global_file.player_1.BattleStrength)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    global_file.enemy_1.BattleStrength = global_file.enemy_1.BattleStrength \
                                                         + (global_file.enemy_1.strength * multiplyer)
                    battle_calc_info(turn, picked_skill)
                else:
                    global_file.enemy_1.BattleStrength = global_file.enemy_1.BattleStrength \
                                                         - (global_file.enemy_1.strength * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                print("global_file.enemy_1 Strength is", global_file.enemy_1.BattleStrength)
                battle_calc_info(turn, picked_skill)

        elif action == "Defence":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.player_1.BattleEndurance = global_file.player_1.BattleEndurance \
                                                           + (global_file.player_1.endurance * multiplyer)
                else:
                    global_file.player_1.BattleEndurance = global_file.player_1.BattleEndurance \
                                                           - (global_file.player_1.endurance * multiplyer)
                    global_file.player_1.Battle_stats_check()
                print("player Endurance is", global_file.player_1.BattleEndurance)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    global_file.enemy_1.BattleEndurance = global_file.enemy_1.BattleEndurance \
                                                          + (global_file.enemy_1.endurance * multiplyer)

                else:
                    global_file.enemy_1.BattleEndurance = global_file.enemy_1.BattleEndurance \
                                                          - (global_file.enemy_1.endurance * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                print("global_file.enemy_1 Endurance is", global_file.enemy_1.BattleEndurance)
                battle_calc_info(turn, picked_skill)

        elif action == "Intelligence":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.player_1.BattleIntelligence = global_file.player_1.BattleIntelligence \
                                                              + (global_file.player_1.intelligence * multiplyer)
                else:
                    global_file.player_1.BattleIntelligence = global_file.player_1.BattleIntelligence \
                                                              - (global_file.player_1.intelligence * multiplyer)
                    global_file.player_1.Battle_stats_check()
                print("player Intelligence is", global_file.player_1.BattleIntelligence)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    global_file.enemy_1.BattleIntelligence = global_file.enemy_1.BattleIntelligence \
                                                             + (global_file.enemy_1.intelligence * multiplyer)
                else:
                    global_file.enemy_1.BattleIntelligence = global_file.enemy_1.BattleIntelligence \
                                                             - (global_file.enemy_1.intelligence * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                print("global_file.enemy_1 Intelligence is", global_file.enemy_1.BattleIntelligence)
                battle_calc_info(turn, picked_skill)

        elif action == "Willpower":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.player_1.BattleWillpower = global_file.player_1.BattleWillpower + \
                                                           (global_file.player_1.willpower * multiplyer)
                else:
                    global_file.player_1.BattleWillpower = global_file.player_1.BattleWillpower \
                                                           - (global_file.player_1.willpower * multiplyer)
                    global_file.player_1.Battle_stats_check()
                print("player Willpower is", global_file.player_1.BattleWillpower)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    global_file.enemy_1.BattleWillpower = global_file.enemy_1.BattleWillpower \
                                                          + (global_file.enemy_1.willpower * multiplyer)
                else:
                    global_file.enemy_1.BattleWillpower = global_file.enemy_1.BattleWillpower \
                                                          - (global_file.enemy_1.willpower * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                print("global_file.enemy_1 Willpower is", global_file.enemy_1.BattleWillpower)
                battle_calc_info(turn, picked_skill)

        elif action == "Dexterity":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.player_1.BattleDexterity = global_file.player_1.BattleDexterity \
                                                           + (global_file.player_1.dexterity * multiplyer)
                else:
                    global_file.player_1.BattleDexterity = global_file.player_1.BattleDexterity \
                                                           - (global_file.player_1.dexterity * multiplyer)
                    global_file.player_1.Battle_stats_check()
                print("player Dexterity is", global_file.player_1.BattleDexterity)
                battle_calc_info(turn, picked_skill)
            else:
                if effect == "+":
                    global_file.enemy_1.BattleDexterity = global_file.enemy_1.BattleDexterity \
                                                          + (global_file.enemy_1.dexterity * multiplyer)
                else:
                    global_file.enemy_1.BattleDexterity = global_file.enemy_1.BattleDexterity \
                                                          - (global_file.enemy_1.dexterity * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                print("global_file.enemy_1 Dexterity is", global_file.enemy_1.BattleDexterity)
                battle_calc_info(turn, picked_skill)

        elif action == "All":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.player_1.BattleStrength += (global_file.player_1.strength * multiplyer)
                    global_file.player_1.BattleEndurance += (global_file.player_1.endurance * multiplyer)
                    global_file.player_1.BattleIntelligence += (global_file.player_1.intelligence * multiplyer)
                    global_file.player_1.BattleWillpower += (global_file.player_1.willpower * multiplyer)
                    global_file.player_1.BattleDexterity += (global_file.player_1.dexterity * multiplyer)
                else:
                    global_file.player_1.BattleStrength -= (global_file.player_1.strength * multiplyer)
                    global_file.player_1.BattleEndurance -= (global_file.player_1.endurance * multiplyer)
                    global_file.player_1.BattleIntelligence -= (global_file.player_1.intelligence * multiplyer)
                    global_file.player_1.BattleWillpower -= (global_file.player_1.willpower * multiplyer)
                    global_file.player_1.BattleDexterity -= (global_file.player_1.dexterity * multiplyer)
                    global_file.player_1.Battle_stats_check()
            else:
                if effect == "+":
                    global_file.enemy_1.BattleStrength += (global_file.enemy_1.strength * multiplyer)
                    global_file.enemy_1.BattleEndurance += (global_file.enemy_1.endurance * multiplyer)
                    global_file.enemy_1.BattleIntelligence += (global_file.enemy_1.intelligence * multiplyer)
                    global_file.enemy_1.BattleWillpower += (global_file.enemy_1.willpower * multiplyer)
                    global_file.enemy_1.BattleDexterity += (global_file.enemy_1.dexterity * multiplyer)

                else:
                    global_file.enemy_1.BattleStrength -= (global_file.enemy_1.strength * multiplyer)
                    global_file.enemy_1.BattleEndurance -= (global_file.enemy_1.endurance * multiplyer)
                    global_file.enemy_1.BattleIntelligence -= (global_file.enemy_1.intelligence * multiplyer)
                    global_file.enemy_1.BattleWillpower -= (global_file.enemy_1.willpower * multiplyer)
                    global_file.enemy_1.BattleDexterity -= (global_file.enemy_1.dexterity * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
            battle_calc_info(turn, picked_skill)

        elif action == "Status":
            print("status")

    elif Target == "global_file.enemy_1":

        if action == "HP":
            if turn % 2 == 0:
                if effect == "+":
                    if form == "mag":
                        damage = (global_file.player_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.player_1.BattleStrength * multiplyer)
                    global_file.enemy_1.BattleHP = global_file.enemy_1.BattleHP + damageCheck(damage)
                    if global_file.enemy_1.BattleHP > global_file.enemy_1.HP:
                        global_file.enemy_1.BattleHP = global_file.enemy_1.HP
                        print("Overflow HP removed")
                    print("global_file.enemy_1 HP is", global_file.enemy_1.BattleHP)
                else:
                    if picked_skill[0] in ["Back Stab", "Assassinate"]:
                        damage = ((global_file.player_1.BattleStrength
                                   + global_file.player_1.BattleDexterity) * multiplyer) - (
                                         global_file.enemy_1.BattleEndurance / 2)
                    elif form == "mag":
                        damage = (global_file.player_1.BattleIntelligence * multiplyer) \
                                 - (global_file.enemy_1.BattleWillpower / 2)
                    elif form == "phy":
                        damage = (global_file.player_1.BattleStrength * multiplyer) \
                                 - (global_file.enemy_1.BattleEndurance / 2)
                    elif form in temp_list:
                        damage = 0
                        for i in temp_list:
                            if i == form and global_file.enemy_1.Statuses[temp_list.index(form)][0]:
                                damage = global_file.enemy_1.HP * multiplyer
                        if damage == 0:
                            damage = 10

                    global_file.enemy_1.BattleHP = global_file.enemy_1.BattleHP - damageCheck(damage)
                    print("global_file.enemy_1 HP is", global_file.enemy_1.BattleHP)
                battle_calc_info(turn, picked_skill, damage)
            else:
                if effect == "+":
                    if form == "mag":
                        damage = (global_file.enemy_1.BattleIntelligence * multiplyer)
                    elif form == "phy":
                        damage = (global_file.enemy_1.BattleStrength * multiplyer)
                    global_file.player_1.BattleHP = global_file.player_1.BattleHP \
                                                    + (global_file.enemy_1.BattleStrength * multiplyer)
                    if global_file.player_1.BattleHP > global_file.player_1.HP:
                        global_file.player_1.BattleHP = global_file.player_1.HP
                        print("Overflow HP removed")
                    print("player HP is", global_file.player_1.BattleHP)
                else:
                    if picked_skill[0] in ["Back Stab", "Assassinate"]:
                        damage = ((global_file.enemy_1.BattleStrength + global_file.enemy_1.BattleDexterity)
                                  * multiplyer) - (global_file.player_1.BattleEndurance / 2)
                    elif form == "mag":
                        damage = (global_file.enemy_1.BattleIntelligence * multiplyer) \
                                 - (global_file.player_1.BattleWillpower / 2)
                    elif form == "phy":
                        damage = (global_file.enemy_1.BattleStrength * multiplyer) \
                                 - (global_file.player_1.BattleEndurance / 2)
                    elif form in temp_list:
                        damage = 0
                        for i in temp_list:
                            if i == form and global_file.player_1.Statuses[temp_list.index(form)][0]:
                                damage = global_file.player_1.HP * multiplyer
                        if damage == 0:
                            damage = 10

                    global_file.player_1.BattleHP = global_file.player_1.BattleHP - damageCheck(damage)
                    print("player HP is", global_file.player_1.BattleHP)
                battle_calc_info(turn, picked_skill, damage)

        elif action == "MP":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.enemy_1.BattleMP = global_file.enemy_1.BattleMP + (global_file.enemy_1.intelligence
                                                                                   * multiplyer)
                    if global_file.enemy_1.BattleMP > global_file.enemy_1.MP:
                        global_file.enemy_1.BattleMP = global_file.enemy_1.MP
                        print("overflow MP released")
                else:
                    global_file.enemy_1.BattleMP = global_file.enemy_1.BattleMP - (global_file.enemy_1.intelligence
                                                                                   * multiplyer)
                print("global_file.enemy_1 MP is", global_file.enemy_1.BattleMP)
                battle_calc_info(turn, picked_skill, (global_file.enemy_1.intelligence * multiplyer))
            else:
                if effect == "+":
                    global_file.player_1.BattleMP = global_file.player_1.BattleMP \
                                                    + (global_file.player_1.intelligence * multiplyer)
                    if global_file.player_1.BattleMP > global_file.player_1.MP:
                        global_file.player_1.BattleMP = global_file.player_1.MP
                        print("overflow MP released")
                else:
                    global_file.player_1.BattleMP = global_file.player_1.BattleMP \
                                                    - (global_file.player_1.intelligence * multiplyer)
                print("global_file.player_1 MP is", global_file.player_1.BattleMP)
                battle_calc_info(turn, picked_skill, (global_file.player_1.intelligence * multiplyer))

        elif action == "Attack":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.enemy_1.BattleStrength = global_file.enemy_1.BattleStrength \
                                                         + (global_file.player_1.strength * multiplyer)
                    print("global_file.enemy_1 Strength is", global_file.enemy_1.BattleStrength)
                else:
                    global_file.enemy_1.BattleStrength = global_file.enemy_1.BattleStrength \
                                                         - (global_file.player_1.strength * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                    print("global_file.enemy_1 Strength is", global_file.enemy_1.BattleStrength)
            else:
                if effect == "+":
                    global_file.player_1.BattleStrength = global_file.player_1.BattleStrength \
                                                          + (global_file.enemy_1.strength * multiplyer)
                    print("player Strength is", global_file.player_1.BattleStrength)
                else:
                    global_file.player_1.BattleStrength = global_file.player_1.BattleStrength \
                                                          - (global_file.enemy_1.strength * multiplyer)
                    global_file.player_1.Battle_stats_check()
                    print("player Strength is", global_file.player_1.BattleStrength)
            battle_calc_info(turn, picked_skill)

        elif action == "Defence":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.enemy_1.BattleEndurance = global_file.enemy_1.BattleEndurance \
                                                          + (global_file.player_1.endurance * multiplyer)
                    print("global_file.enemy_1 Endurance is", global_file.enemy_1.BattleEndurance)
                else:
                    global_file.enemy_1.BattleEndurance = global_file.enemy_1.BattleEndurance \
                                                          - (global_file.player_1.endurance * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                    print("global_file.enemy_1 Endurance is", global_file.enemy_1.BattleEndurance)
            else:
                if effect == "+":
                    global_file.player_1.BattleEndurance = global_file.player_1.BattleEndurance \
                                                           + (global_file.enemy_1.endurance * multiplyer)
                    print("player Endurance is", global_file.player_1.BattleEndurance)
                else:
                    global_file.player_1.BattleEndurance = global_file.player_1.BattleEndurance \
                                                           - (global_file.enemy_1.endurance * multiplyer)
                    global_file.player_1.Battle_stats_check()
                    print("player Endurance is", global_file.player_1.BattleEndurance)
            battle_calc_info(turn, picked_skill)

        elif action == "Intelligence":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.enemy_1.BattleIntelligence = global_file.enemy_1.BattleIntelligence \
                                               + (global_file.player_1.intelligence * multiplyer)
                else:
                    global_file.enemy_1.BattleIntelligence = global_file.enemy_1.BattleIntelligence \
                                               - (global_file.player_1.intelligence * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                print("global_file.enemy_1 Intelligence is", global_file.enemy_1.BattleIntelligence)
            else:
                if effect == "+":
                    global_file.player_1.BattleIntelligence = global_file.player_1.BattleIntelligence \
                                                              + (global_file.enemy_1.intelligence * multiplyer)
                else:
                    global_file.player_1.BattleIntelligence = global_file.player_1.BattleIntelligence \
                                                              - (global_file.enemy_1.intelligence * multiplyer)
                    global_file.player_1.Battle_stats_check()
                print("player Intelligence is", global_file.player_1.BattleIntelligence)
            battle_calc_info(turn, picked_skill)

        elif action == "Willpower":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.enemy_1.BattleWillpower = global_file.enemy_1.BattleWillpower \
                                                          + (global_file.player_1.willpower * multiplyer)
                else:
                    global_file.enemy_1.BattleWillpower = global_file.enemy_1.BattleWillpower \
                                                          - (global_file.player_1.willpower * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                print("global_file.enemy_1 Willpower is", global_file.enemy_1.BattleWillpower)
            else:
                if effect == "+":
                    global_file.player_1.BattleWillpower = global_file.player_1.BattleWillpower \
                                                           + (global_file.enemy_1.willpower * multiplyer)
                else:
                    global_file.player_1.BattleWillpower = global_file.player_1.BattleWillpower \
                                                           - (global_file.enemy_1.willpower * multiplyer)
                    global_file.player_1.Battle_stats_check()
                print("player Willpower is", global_file.player_1.BattleWillpower)
            battle_calc_info(turn, picked_skill)

        elif action == "Dexterity":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.enemy_1.BattleDexterity = global_file.enemy_1.BattleDexterity \
                                                          + (global_file.player_1.dexterity * multiplyer)
                else:
                    global_file.enemy_1.BattleDexterity = global_file.enemy_1.BattleDexterity \
                                                          - (global_file.player_1.dexterity * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
                print("global_file.enemy_1 Dexterity is", global_file.enemy_1.BattleDexterity)
            else:
                if effect == "+":
                    global_file.player_1.BattleDexterity = global_file.player_1.BattleDexterity \
                                                           + (global_file.enemy_1.dexterity * multiplyer)
                else:
                    global_file.player_1.BattleDexterity = global_file.player_1.BattleDexterity \
                                                           - (global_file.enemy_1.dexterity * multiplyer)
                    global_file.player_1.Battle_stats_check()
                print("player Dexterity is", global_file.player_1.BattleDexterity)
            battle_calc_info(turn, picked_skill)

        elif action == "All":
            if turn % 2 == 0:
                if effect == "+":
                    global_file.enemy_1.BattleStrength += (global_file.player_1.strength * multiplyer)
                    global_file.enemy_1.BattleEndurance += (global_file.player_1.endurance * multiplyer)
                    global_file.enemy_1.BattleIntelligence += (global_file.player_1.intelligence * multiplyer)
                    global_file.enemy_1.BattleWillpower += (global_file.player_1.willpower * multiplyer)
                    global_file.enemy_1.BattleDexterity += (global_file.player_1.dexterity * multiplyer)
                else:
                    global_file.enemy_1.BattleStrength -= (global_file.player_1.strength * multiplyer)
                    global_file.enemy_1.BattleEndurance -= (global_file.player_1.endurance * multiplyer)
                    global_file.enemy_1.BattleIntelligence -= (global_file.player_1.intelligence * multiplyer)
                    global_file.enemy_1.BattleWillpower -= (global_file.player_1.willpower * multiplyer)
                    global_file.enemy_1.BattleDexterity -= (global_file.player_1.dexterity * multiplyer)
                    global_file.enemy_1.Battle_stats_check()
            else:
                if effect == "+":
                    global_file.player_1.BattleStrength += (global_file.enemy_1.strength * multiplyer)
                    global_file.player_1.BattleEndurance += (global_file.enemy_1.endurance * multiplyer)
                    global_file.player_1.BattleIntelligence += (global_file.enemy_1.intelligence * multiplyer)
                    global_file.player_1.BattleWillpower += (global_file.enemy_1.willpower * multiplyer)
                    global_file.player_1.BattleDexterity += (global_file.enemy_1.dexterity * multiplyer)

                else:
                    global_file.player_1.BattleStrength -= (global_file.enemy_1.strength * multiplyer)
                    global_file.player_1.BattleEndurance -= (global_file.enemy_1.endurance * multiplyer)
                    global_file.player_1.BattleIntelligence -= (global_file.enemy_1.intelligence * multiplyer)
                    global_file.player_1.BattleWillpower -= (global_file.enemy_1.willpower * multiplyer)
                    global_file.player_1.BattleDexterity -= (global_file.enemy_1.dexterity * multiplyer)
                    global_file.player_1.Battle_stats_check()
            battle_calc_info(turn, picked_skill)

        # This section checks if the action should inflict the corresponding status effect
        elif action == "Status":
            chance = random.randint(0, 100)
            if effect == "Burn":
                if chance <= multiplyer:
                    if turn % 2 == 0:
                        global_file.enemy_1.Statuses[0][0] = True
                        global_file.enemy_1.Statuses[0][1] += 1
                        if global_file.enemy_1.Statuses[0][1] == 4:
                            global_file.enemy_1.Statuses[0][1] = 3
                        else:
                            global_file.enemy_1.BattleEndurance = global_file.enemy_1.BattleEndurance \
                                                                  - (global_file.enemy_1.endurance * 0.1)
                        global_file.enemy_1.Statuses[0][2] = 3
                        print("Burn stage", global_file.enemy_1.Statuses[0][1], "was applied")
                    else:
                        global_file.player_1.Statuses[0][0] = True
                        global_file.player_1.Statuses[0][1] += 1
                        if global_file.player_1.Statuses[0][1] == 4:
                            global_file.player_1.Statuses[0][1] = 3
                        global_file.player_1.BattleEndurance = global_file.player_1.BattleEndurance \
                                                               - (global_file.player_1.endurance * 0.1)
                        global_file.player_1.Statuses[0][2] = 3
                        print("Burn stage", global_file.player_1.Statuses[0][1], "was applied")
                    battle_calc_info(turn, picked_skill, 0, 1)

                else:
                    print("Burn was ineffective")
                    battle_calc_info(turn, picked_skill, 0, -1)

            elif effect == "Sleep":
                if chance <= multiplyer:
                    if turn % 2 == 0:
                        global_file.enemy_1.Statuses[1][0] = True
                        global_file.enemy_1.Statuses[1][1] += 1
                        if global_file.enemy_1.Statuses[1][1] == 4:
                            global_file.enemy_1.Statuses[1][1] = 3
                        print("Sleep stage", global_file.enemy_1.Statuses[1][1], "was applied")
                    else:
                        global_file.player_1.Statuses[1][0] = True
                        global_file.player_1.Statuses[1][1] += 1
                        if global_file.player_1.Statuses[1][1] == 4:
                            global_file.player_1.Statuses[1][1] = 3
                        print("Sleep stage", global_file.player_1.Statuses[1][1], "was applied")
                    battle_calc_info(turn, picked_skill, 0, 1)
                else:
                    print("Sleep was ineffective")
                    battle_calc_info(turn, picked_skill, 0, 0)

            elif effect == "Poison":
                if chance <= multiplyer:
                    if turn % 2 == 0:
                        global_file.enemy_1.Statuses[2][0] = True
                        global_file.enemy_1.Statuses[2][1] += 1
                        if global_file.enemy_1.Statuses[2][1] == 4:
                            global_file.enemy_1.Statuses[2][1] = 3
                        else:
                            global_file.enemy_1.BattleDexterity = global_file.enemy_1.BattleDexterity \
                                                                  - (global_file.enemy_1.dexterity * 0.1)
                        global_file.enemy_1.Statuses[2][2] = 3
                        print("Poison stage", global_file.enemy_1.Statuses[2][1], "was applied")
                    else:
                        global_file.player_1.Statuses[2][0] = True
                        global_file.player_1.Statuses[2][1] += 1
                        if global_file.player_1.Statuses[2][1] == 4:
                            global_file.player_1.Statuses[2][1] = 3
                        global_file.player_1.BattleDexterity = global_file.player_1.BattleDexterity \
                                                               - (global_file.player_1.dexterity * 0.1)
                        global_file.player_1.Statuses[2][2] = 3
                        print("Poison stage", global_file.player_1.Statuses[2][1], "was applied")
                    battle_calc_info(turn, picked_skill, 0, 1)
                else:
                    print("Poison was ineffective")
                    battle_calc_info(turn, picked_skill, 0, -1)


# This function is called at the start of every turn so active status effects can take place
def status_check(turn):
    sleep = False
    player_checklist = []
    enemy_1_checklist = []
    # This part allows for the check if the player or global_file.enemy_1 has any status effects active
    for i in range(3):
        player_checklist.append(global_file.player_1.Statuses[i][0])
    for i in range(3):
        enemy_1_checklist.append(global_file.enemy_1.Statuses[i][0])

    if turn == 0:
        if True in player_checklist:
            # this checks if the burn status on the player is active
            if global_file.player_1.Statuses[0][0]:
                print("Activate player Burn")
                # this line deals the corresponding damage due to the burn to the player
                global_file.player_1.BattleHP = global_file.player_1.BattleHP - (global_file.player_1.endurance * 0.1
                                                                                 * global_file.player_1.Statuses[0][1])
                global_file.player_1.Statuses[0][2] -= 1
                # The duration of the burn is then decreased by one
                if global_file.player_1.Statuses[0][2] == 0:
                    # If the duration reaches zero then the player is given back their endurance
                    # and other values are reset and the status is removed
                    global_file.player_1.Statuses[0][0] = False
                    for i in range(global_file.player_1.Statuses[0][1]):
                        global_file.player_1.BattleEndurance = global_file.player_1.BattleEndurance \
                                                               + (global_file.player_1.endurance * 0.1)
                    global_file.player_1.Statuses[0][1] = 0
                    global_file.player_1.Statuses[0][2] = 5
                    print("Burn removed")

            if global_file.player_1.Statuses[1][0]:
                print("Activate player Sleep")
                chance = random.randint(0, 100)
                if global_file.player_1.Statuses[1][1] == 1:
                    if chance <= 50:
                        global_file.player_1.Statuses[1][0] = False
                        print("sleep deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in sleep")
                elif global_file.player_1.Statuses[1][1] == 2:
                    if chance <= 30:
                        global_file.player_1.Statuses[1][0] = False
                        print(" deep sleep deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in deep sleep")
                elif global_file.player_1.Statuses[1][1] == 3:
                    if chance <= 25:
                        global_file.player_1.Statuses[1][0] = False
                        print("coma deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in a coma")

            if global_file.player_1.Statuses[2][0]:
                global_file.player_1.BattleHP = global_file.player_1.BattleHP - (global_file.player_1.HP * 0.01
                                                                                 * global_file.player_1.Statuses[2][1])
                global_file.player_1.Statuses[2][2] -= 1
                if global_file.player_1.Statuses[2][2] == 0:
                    global_file.player_1.Statuses[2][0] = False
                    for i in range(global_file.player_1.Statuses[2][1]):
                        global_file.player_1.BattleDexterity = global_file.player_1.BattleDexterity \
                                                               + (global_file.player_1.dexterity * 0.1)
                    global_file.player_1.Statuses[2][1] = 0
                    global_file.player_1.Statuses[2][2] = 5
                    print("Poison removed")

                print("Activate player poison")
        return sleep

    elif turn == 1:
        if True in enemy_1_checklist:
            if global_file.enemy_1.Statuses[0][0]:
                print("Activate global_file.enemy_1 Burn")
                global_file.enemy_1.BattleHP = global_file.enemy_1.BattleHP - (global_file.enemy_1.endurance * 0.1
                                                                               * global_file.enemy_1.Statuses[0][1])
                global_file.enemy_1.Statuses[0][2] -= 1
                if global_file.enemy_1.Statuses[0][2] == 0:
                    global_file.enemy_1.Statuses[0][0] = False
                    for i in range(global_file.enemy_1.Statuses[0][1]):
                        global_file.enemy_1.BattleEndurance = global_file.enemy_1.BattleEndurance \
                                                              + (global_file.enemy_1.endurance * 0.1)
                    global_file.enemy_1.Statuses[0][1] = 0
                    global_file.enemy_1.Statuses[0][2] = 3

            if global_file.enemy_1.Statuses[1][0]:
                print("Activate enemy Sleep")
                chance = random.randint(0, 100)
                if global_file.enemy_1.Statuses[1][1] == 1:
                    if chance <= 50:
                        global_file.enemy_1.Statuses[1][0] = False
                        global_file.enemy_1.Statuses[1][1] = 0
                        print("sleep deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in sleep")
                elif global_file.enemy_1.Statuses[1][1] == 2:
                    if chance <= 30:
                        global_file.enemy_1.Statuses[1][0] = False
                        global_file.enemy_1.Statuses[1][1] = 0
                        print(" deep sleep deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in deep sleep")
                elif global_file.enemy_1.Statuses[1][1] == 3:
                    if chance <= 25:
                        global_file.enemy_1.Statuses[1][0] = False
                        global_file.enemy_1.Statuses[1][1] = 0
                        print("coma deactivated")
                    else:
                        sleep = True
                        print("turn skipped, remain in a coma")

            if global_file.enemy_1.Statuses[2][0]:
                print(global_file.enemy_1.BattleHP)
                global_file.enemy_1.BattleHP = global_file.enemy_1.BattleHP - (global_file.enemy_1.HP * 0.01
                                                                               * global_file.enemy_1.Statuses[2][1])
                print(global_file.enemy_1.BattleHP)
                global_file.enemy_1.Statuses[2][2] -= 1
                if global_file.enemy_1.Statuses[2][2] == 0:
                    global_file.enemy_1.Statuses[2][0] = False
                    for i in range(global_file.enemy_1.Statuses[2][1]):
                        global_file.enemy_1.BattleDexterity = global_file.enemy_1.BattleDexterity \
                                                              + (global_file.enemy_1.dexterity * 0.1)
                    global_file.enemy_1.Statuses[2][1] = 0
                    global_file.enemy_1.Statuses[2][2] = 3

                print("Activate enemy poison")
        return sleep


# draws the health bars and the sprites for the player and enemy
# and indicate if they are suffering from any status effects
def battle_info_draw():
    Text_font = pygame.font.Font("freesansbold.ttf", 20)
    sleep = pygame.image.load(r"sleep.png")
    poison = pygame.image.load(r"poison.png")
    burn = pygame.image.load(r"burn.png")

    player_sprite = pygame.image.load(r"player sprite.png")
    enemy_sprite = pygame.image.load(r"enemy sprites" + chr(92) + str(global_file.enemy_1.name) + ".png")

    # enemy info
    display.blit(enemy_sprite, (600, 125))
    pygame.draw.rect(display, white, (795, 75, 330, 75))
    pygame.draw.rect(display, global_file.background, (790, 70, 340, 85))
    button(global_file.enemy_1.name, 795, 75, 330, 35, 20, white, white)
    button("", 825, 110, 300, 40, 1, red, red)
    button("HP", 795, 110, 30, 20, 20, white, white)
    button("MP", 795, 130, 30, 20, 20, white, white)

    # indicate what statuses are affecting the enemy
    if global_file.enemy_1.Statuses[0][0]:
        display.blit(burn, (800, 50))
    if global_file.enemy_1.Statuses[1][0]:
        display.blit(sleep, (825, 50))
    if global_file.enemy_1.Statuses[2][0]:
        display.blit(poison, (850, 50))

    # the health and mana bars
    if global_file.enemy_1.BattleHP > 0:
        button("", 825, 110, ((global_file.enemy_1.BattleHP / global_file.enemy_1.HP) * 300), 20, 20, green, green)
    text_surf, text_rect = text_objects(f"{global_file.enemy_1.BattleHP}/{global_file.enemy_1.HP}", Text_font)
    text_rect.center = (975, 120)
    display.blit(text_surf, text_rect)

    if global_file.enemy_1.BattleMP > 0:
        button("", 825, 130, ((global_file.enemy_1.BattleMP / global_file.enemy_1.MP) * 300), 20, 20, blue, blue)
    text_surf, text_rect = text_objects(f"{global_file.enemy_1.BattleMP}/{global_file.enemy_1.MP}", Text_font)
    text_rect.center = (975, 140)
    display.blit(text_surf, text_rect)

    # player info
    display.blit(player_sprite, (50, 350))
    pygame.draw.rect(display, white, (25, 675, 330, 75))
    pygame.draw.rect(display, global_file.background, (20, 670, 340, 85))
    button("Player", 25, 675, 330, 35, 20, white, white)
    button("", 55, 710, 300, 40, 1, red, red)
    button("HP", 25, 710, 30, 20, 20, white, white)
    button("MP", 25, 730, 30, 20, 20, white, white)

    if global_file.player_1.Statuses[0][0]:
        display.blit(burn, (25, 650))
    if global_file.player_1.Statuses[1][0]:
        display.blit(sleep, (50, 650))
    if global_file.player_1.Statuses[2][0]:
        display.blit(poison, (75, 650))

    if global_file.player_1.BattleHP > 0:
        button("", 55, 710, ((global_file.player_1.BattleHP / global_file.player_1.HP) * 300), 20, 20, green, green)
    text_surf, text_rect = text_objects(f"{global_file.player_1.BattleHP}/{global_file.player_1.HP}", Text_font)
    text_rect.center = (205, 720)
    display.blit(text_surf, text_rect)

    if global_file.player_1.BattleMP > 0:
        button("", 55, 730, ((global_file.player_1.BattleMP / global_file.player_1.MP) * 300), 20, 20, blue, blue)
    text_surf, text_rect = text_objects(f"{global_file.player_1.BattleMP}/{global_file.player_1.MP}", Text_font)
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
    # pygame.time.wait(1500)

    button(message, 150, 150, 400, 100, 20, white, white)
    pygame.display.update()
    # pygame.time.wait(1500)

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
        # pygame.time.wait(1500)
    print(message)


def damageCheck(damage):
    if damage <= 0:
        damage = 1
    return damage

