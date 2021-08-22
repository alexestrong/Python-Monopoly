"""
File:         hw5_part4.py
Author:       Alex Strong
Date:         10/15/2020
Section:      44
E-mail:       astrong3@umbc.edu
Description:  This program accesses a base_creatures.json file that stores
              a dictionary of "creatures". These creatures have stats that
              determine which of the two chosen will win in a fight.  The user
              chooses two of the creatures to fight and the function accesses the
              dictionary to determine who will be alive and/or dead after the fight.
"""
from sys import argv
from random import randint, seed
from board_methods import load_map, display_board
if len(argv) >= 2:
    seed(argv[1])

START_MONEY = 1500
PASSING_MONEY = 200
YES = ['yes', 'y', 'Y', 'YES']
CURRENCY = 'Retriever Ducats'
used_rotation_player_one = [0]
used_rotation_player_two = [0]


def format_display(player_one, player_two, board):
    string_for_function = []
    for y in range(len(board)):
        list_format = list(board[y]['Abbrev'])
        while len(list_format) < 5:
            list_format.append(' ')
        list_format.append('\n')
        position_string_one = str(player_one['Position'] % len(board))
        position_string_two = str(player_two['Position'] % len(board))
        if int(board[y]['Position']) == 0:
            list_format.append('\u261C')
        if position_string_one == board[y]['Position']:
            list_format.append(player_one['Symbol'])
        if position_string_two == board[y]['Position']:
            list_format.append(player_two['Symbol'])
        if board[y]['Owner'] == player_one['Name']:
            list_format.append('\u2691')
        if board[y]['Owner'] == player_two['Name']:
            list_format.append('\u2690')
        if board[y]['Building'] != 'No':
            list_format.append('\u2302')
        while len(list_format) < 11:
            list_format.append(' ')
        joined_string = ''.join(list_format)
        string_for_function.append(joined_string)
        # print(list_format)
        # print(position_string_one, board[y]['Position'])
        # print(position_string_one == board[y]['Position'])
    # print('ONE', string_for_function)

#    updated_board_func = display_board(string_for_function)
#    print(updated_board_func)
    return string_for_function


def play_game(starting_money, board):
    player_one['Current_Money'] = starting_money
    player_two['Current_Money'] = starting_money
    while int(player_one['Current_Money']) > 0 and int(player_two['Current_Money']) > 0:
        take_turn(player_one, player_two)
        take_turn(player_two, player_one)

    pass


def pass_go_checker(individual_player):
    if individual_player['Name'] == player_one['Name']:
        if (individual_player['Position'] // (len(the_map_dictionary) + 1)) not in used_rotation_player_one:
            individual_player['Current_Money'] += PASSING_MONEY
            individual_player['Passed_Go_Rotations'] = (individual_player['Position'] // len(the_map_dictionary))
            used_rotation_player_one.append(individual_player['Passed_Go_Rotations'])
            # print('YOU PASSED GO')
            return True
    if individual_player['Name'] == player_two['Name']:
        if (individual_player['Position'] // (len(the_map_dictionary) + 1)) not in used_rotation_player_two:
            individual_player['Current_Money'] += PASSING_MONEY
            individual_player['Passed_Go_Rotations'] = (individual_player['Position'] // len(the_map_dictionary))
            used_rotation_player_two.append(individual_player['Passed_Go_Rotations'])
            # print('YOU PASSED GO')
            return True


def options_list():
    print()
    print('\t', '1) Buy Property')
    print('\t', '2) Get Property Info')
    print('\t', '3) Get Player Info')
    print('\t', '4) Build a Building')
    print('\t', '5) End Turn')
    print()


def check_location(player):
    for positions in range(len(the_map_dictionary)):
        if str(player['Position'] % len(the_map_dictionary)) == the_map_dictionary[positions]['Position']:
            matched_name = the_map_dictionary[positions]['Place']
            return matched_name


# Buy Property
def option_one(current_player, current_position):
    modded_current_position = current_position % len(the_map_dictionary)
    if int(the_map_dictionary[modded_current_position]['Price']) < 0:
        print('This property cannot be bought!')
    elif the_map_dictionary[modded_current_position]['Owner'] != 'BANK':
        print(the_map_dictionary[modded_current_position]['Place'], 'is already owned')
    elif the_map_dictionary[modded_current_position]['Owner'] == 'BANK':
        print('This property is unowned and costs', the_map_dictionary[modded_current_position]['Price'],
              (CURRENCY + '.'), 'You will have', current_player['Current_Money'] -
              int(the_map_dictionary[modded_current_position]['Price']), CURRENCY, 'remaining.')
        purchase_property = input('Would you like to purchase this property? (y/n) ')
        if purchase_property in YES:
            the_map_dictionary[modded_current_position]['Owner'] = current_player['Name']
            current_player['Current_Money'] -= int(the_map_dictionary[modded_current_position]['Price'])
            current_player['Owned_Property'].append(modded_current_position)
            print('You now own', the_map_dictionary[modded_current_position]['Place'], current_player['Name'])
            print('You now have', current_player['Current_Money'], 'Retriever Ducats remaining.')

    pass


# Get Property Info
def option_two():
    selected_property = input('Enter the abbreviation of the property you would like information for: ')
    for board_place in range(len(the_map_dictionary)):
        if selected_property == the_map_dictionary[board_place]['Abbrev']:
            print()
            print('\t', the_map_dictionary[board_place]['Place'])
            print('\t', 'Price:', the_map_dictionary[board_place]['Price'])
            print('\t', 'Owner:', the_map_dictionary[board_place]['Owner'])
            print('\t', 'Building:', the_map_dictionary[board_place]['Building'])
            print('\t', 'Cost to build:', the_map_dictionary[board_place]['BuildingCost'])
            print('\t', 'Rent:', the_map_dictionary[board_place]['Rent'] + ',', end=' ')
            print(the_map_dictionary[board_place]['BuildingRent'], '(with building)')
            print()

    pass


# Get Player Info
def option_three():
    print('The players are:')
    print('\t', player_one['Name'])
    print('\t', player_two['Name'])
    requested_name = input('Which player do you wish to know about? ')
    if requested_name == player_one['Name']:
        print()
        print('Player Info:')
        print('\tPlayer Name:', player_one['Name'])
        print('\tPlayer Symbol:', player_one['Symbol'])
        print('\tCurrent Money:', player_one['Current_Money'])
        print()
        print('Properties Owned:')
        print()
        for name_scanning in range(len(the_map_dictionary)):
            if player_one['Name'] == the_map_dictionary[name_scanning]['Owner']:
                print('\t', the_map_dictionary[name_scanning]['Place'], end=',')
                if the_map_dictionary[name_scanning]['Building'] == 'No':
                    print('without building.')
                else:
                    print('with building.')
    if requested_name == player_two['Name']:
        print()
        print('\tPlayer Name:', player_two['Name'])
        print('\tPlayer Symbol:', player_two['Symbol'])
        print('\tCurrent Money:', player_two['Current_Money'])
        print()
        print('Properties Owned:')
        print()
        for name_scanning in range(len(the_map_dictionary)):
            if player_two['Name'] == the_map_dictionary[name_scanning]['Owner']:
                print(the_map_dictionary[name_scanning]['Place'], end=',')
                if the_map_dictionary[name_scanning]['Building'] == 'No':
                    print('without building.')
                else:
                    print('with building.')
    pass


# Build a Building
def option_four(current_player, current_position):
    modded_current_position = current_position % len(the_map_dictionary)
    print('You have', current_player['Current_Money'], CURRENCY, 'and can build on: ')
    for name_scanning in range(len(the_map_dictionary)):
        if current_player['Name'] == the_map_dictionary[name_scanning]['Owner']:
            if the_map_dictionary[name_scanning]['Building'] == 'No':
                print('\t', the_map_dictionary[name_scanning]['Place'], '|', the_map_dictionary[name_scanning]['Abbrev']
                      , '|', the_map_dictionary[name_scanning]['BuildingCost'])
    building_choice = input('Enter the abbreviation of the property that you would you like to build on: ')
    found_building = False
    for scanning in range(len(the_map_dictionary)):
        if building_choice == the_map_dictionary[scanning]['Abbrev']:
            the_map_dictionary[scanning]['Building'] = 'Yes'
            current_player['Owned_Buildings'].append(modded_current_position)
            current_player['Current_Money'] -= int(the_map_dictionary[modded_current_position]['BuildingCost'])
            print('You have built the building for', the_map_dictionary[scanning]['Place'])
            print('You now have', current_player['Current_Money'], 'Retriever Ducats remaining.')
            found_building = True
    if not found_building:
        print('The property either has a building, isn\'t yours, or doesn\'t exist')
    pass


# End Turn
def option_five():
    pass


def take_turn(player, secondary_player):
    dice_roll = randint(1, 6) + randint(1, 6)
    player['Position'] += dice_roll
    display_board(format_display(player_one, player_two, the_map_dictionary))
    print('Current Position:', player['Position'])
    print(player['Name'], 'you have rolled a', dice_roll)
    if pass_go_checker(player):
        print('You passed go, collect', PASSING_MONEY, '~', 'New balance:', player['Current_Money'])

    print(player['Name'], 'you landed on', check_location(player), 'and you have', player['Current_Money'],
          'Retriever Ducats.')
    current_position_mod = player['Position'] % len(the_map_dictionary)
    if current_position_mod in secondary_player['Owned_Property']:
        if current_position_mod in secondary_player['Owned_Buildings']:
            player['Current_Money'] -= int(the_map_dictionary[current_position_mod]['BuildingRent'])
            secondary_player['Current_Money'] += int(the_map_dictionary[current_position_mod]['BuildingRent'])
            print('You landed on the building owned by', secondary_player['Name'])
            print('You have paid', the_map_dictionary[current_position_mod]['BuildingRent'], 'in building rent to',
                  secondary_player['Name'], '~', 'New Balance:', player['Current_Money'])

        else:
            player['Current_Money'] -= int(the_map_dictionary[current_position_mod]['Rent'])
            secondary_player['Current_Money'] += int(the_map_dictionary[current_position_mod]['Rent'])
            print('You landed on the property owned by', secondary_player['Name'])
            print('You have paid', the_map_dictionary[current_position_mod]['Rent'], 'in rent to',
                  secondary_player['Name'], '~', 'New Balance:', player['Current_Money'])

    # print('new money', player['Current_Money'])

    # print(player)
    options_list()
    user_choice = int(input('\t' + player['Name'] + ', What would you like to do? '))
    while user_choice != 5:
        if user_choice == 1:
            option_one(player, player['Position'])
        elif user_choice == 2:
            option_two()
        elif user_choice == 3:
            option_three()
        elif user_choice == 4:
            option_four(player, player['Position'])
        options_list()
        user_choice = int(input('\t' + player['Name'] + ', What would you like to do? '))

    return user_choice

    pass


map_list = []
player_one = {'Position': 0, 'Current_Money': 0, 'Passed_Go_Rotations': 0, 'Owned_Property': [], 'Owned_Buildings': []}
player_two = {'Position': 0, 'Current_Money': 0, 'Passed_Go_Rotations': 0, 'Owned_Property': [], 'Owned_Buildings': []}

if __name__ == '__main__':

    the_map_dictionary = load_map('proj1_board2.csv')
    # print(the_map)
    for owned_and_buildings in range(len(the_map_dictionary)):
        the_map_dictionary[owned_and_buildings]['Owner'] = 'BANK'
        the_map_dictionary[owned_and_buildings]['Building'] = 'No'

    player_one['Name'] = input('First player, what is your name? ')
    symbol_one = input('First player, what symbol do you want your character to use? ')
    player_one['Symbol'] = symbol_one.upper()
    while len(list(player_one['Symbol'])) != 1:
        symbol_one = input('Please enter a 1-Character symbol: ')
        player_one['Symbol'] = symbol_one.upper()

    player_two['Name'] = input('Second player, what is your name? ')
    symbol_two = input('Second player, what symbol do you want your character to use? ')
    player_two['Symbol'] = symbol_two.upper()
    while len(list(player_two['Symbol'])) != 1:
        symbol_two = input('Please enter a 1-Character symbol: ')
        player_two['Symbol'] = symbol_two.upper()

    '''for x in range(len(the_map)):
        print(the_map[x], end='\n')'''
    # play_game(START_MONEY, the_map_dictionary)
    # formatted_map = format_display(player_one, player_two, the_map_dictionary)
    # display_board(formatted_map)
    play_game(START_MONEY, the_map_dictionary)
