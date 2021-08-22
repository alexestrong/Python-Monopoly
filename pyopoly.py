"""
File:         pyopoly.py
Author:       Alex Strong
Date:         10/25/2020
Section:      44
E-mail:       astrong3@umbc.edu
Description:  This program emulates the real game of monopoly.  While it is
              simply a two player game, there are functions that enable
              the players to roll dice, buy property, sell property, collect
              money and much more alike the real monopoly game.  The game
              continues until the other player runs out of money and loses.
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
# below two line used to keep track of rotations around board
used_rotation_player_one = [0]
used_rotation_player_two = [0]
# below two lines define pre-existing conditions of both players
player_one = {'Position': 0, 'Current_Money': 0, 'Passed_Go_Rotations': 0, 'Owned_Property': [], 'Owned_Buildings': []}
player_two = {'Position': 0, 'Current_Money': 0, 'Passed_Go_Rotations': 0, 'Owned_Property': [], 'Owned_Buildings': []}


# starter function used to loop through turns until someone wins (AKA other player runs out of money)
def play_game(starting_money):
    player_one['Current_Money'] = starting_money
    player_two['Current_Money'] = starting_money
    while int(player_one['Current_Money']) > 0 and int(player_two['Current_Money']) > 0:
        take_turn(player_one, player_two)
        take_turn(player_two, player_one)
    if int(player_one['Current_Money']) > 0:
        print(player_one['Name'], 'wins the game.', player_two['Name'], 'loses.')
    else:
        print(player_two['Name'], 'wins the game.', player_one['Name'], 'loses.')
    pass


# this function does the heavy lifting of running the game for each players turn
def take_turn(player, secondary_player):
    # if you choose the small map, the dice will only be rolled once
    if map_selection == 2:
        dice_roll = randint(1, 6)
    else:
        dice_roll = randint(1, 6) + randint(1, 6)
    player['Position'] += dice_roll
    display_board(format_display(the_map_dictionary))
    print(player['Name'], 'you have rolled a', dice_roll)

    # after the players position is moved, the function to check if they pass go will commence
    if pass_go_checker(player):
        print('You passed go, collect', PASSING_MONEY, '~', 'Previous balance:', (int(player['Current_Money']) -
                                                                                  PASSING_MONEY))

    print(player['Name'], 'you landed on', check_location(player), 'and you have', player['Current_Money'],
          'Retriever Ducats.')

    current_position_mod = player['Position'] % len(the_map_dictionary)
    # checks to see if the spot landed on is property owned by the other player
    if current_position_mod in secondary_player['Owned_Property']:
        # then checks to see if there is a building on that other player's property to charge building rent
        if current_position_mod in secondary_player['Owned_Buildings']:
            player['Current_Money'] -= int(the_map_dictionary[current_position_mod]['BuildingRent'])
            secondary_player['Current_Money'] += int(the_map_dictionary[current_position_mod]['BuildingRent'])
            print('You landed on the building owned by', secondary_player['Name'])
            print('You have paid', the_map_dictionary[current_position_mod]['BuildingRent'], 'in building rent to',
                  secondary_player['Name'], '~', 'New Balance:', player['Current_Money'])
        # if there is no building, then just the property rent will be charged
        else:
            player['Current_Money'] -= int(the_map_dictionary[current_position_mod]['Rent'])
            secondary_player['Current_Money'] += int(the_map_dictionary[current_position_mod]['Rent'])
            print('You landed on the property owned by', secondary_player['Name'])
            print('You have paid', the_map_dictionary[current_position_mod]['Rent'], 'in rent to',
                  secondary_player['Name'], '~', 'New Balance:', player['Current_Money'])

    # prints list of options for the player to choose
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


# simple function to print options list (prevents having duplicate code)
def options_list():
    print()
    print('\t', '1) Buy Property')
    print('\t', '2) Get Property Info')
    print('\t', '3) Get Player Info')
    print('\t', '4) Build a Building')
    print('\t', '5) End Turn')
    print()


# Buy Property; checks to see if you can buy, asks you to confirm, then charges and makes you the owner of the property
def option_one(current_player, current_position):
    modded_current_position = current_position % len(the_map_dictionary)
    # checks if property is purchasable
    if int(the_map_dictionary[modded_current_position]['Price']) < 0:
        print('This property cannot be bought!')
    # then checks if property is already owned by other players
    elif the_map_dictionary[modded_current_position]['Owner'] != 'BANK':
        print(the_map_dictionary[modded_current_position]['Place'], 'is already owned')
    # occurs if property is purchasable and unowned by other players
    elif the_map_dictionary[modded_current_position]['Owner'] == 'BANK':
        print('This property is unowned and costs', the_map_dictionary[modded_current_position]['Price'],
              (CURRENCY + '.'), 'You will have', current_player['Current_Money'] -
              int(the_map_dictionary[modded_current_position]['Price']), CURRENCY, 'remaining.')
        purchase_property = input('Would you like to purchase this property? (y/n) ')
        if purchase_property in YES:
            # failsafe to make sure the player has enough money to actually purchase the property
            if (current_player['Current_Money'] - int(the_map_dictionary[modded_current_position]['Price'])) > 0:
                the_map_dictionary[modded_current_position]['Owner'] = current_player['Name']
                current_player['Current_Money'] -= int(the_map_dictionary[modded_current_position]['Price'])
                current_player['Owned_Property'].append(modded_current_position)
                print(current_player['Name'], 'You now own', the_map_dictionary[modded_current_position]['Place'])
                print('You now have', current_player['Current_Money'], 'Retriever Ducats remaining.')
            else:
                print('You do not have the funds to purchase this property')
    pass


# Get Property Info; asks you to enter a place name or abbreviation to provide information on the property
def option_two():
    selected_property = input('Enter the name or abbreviation of the property you would like information for: ')
    found_result = False
    # the for loop iterates through every position on the board to see if it can find a matching name or abbreviation
    for board_place in range(len(the_map_dictionary)):
        if (selected_property == the_map_dictionary[board_place]['Abbrev']) or \
                (selected_property == the_map_dictionary[board_place]['Place']):
            found_result = True
            print()
            print('\t', the_map_dictionary[board_place]['Place'])
            print('\t', 'Price:', the_map_dictionary[board_place]['Price'])
            print('\t', 'Owner:', the_map_dictionary[board_place]['Owner'])
            print('\t', 'Building:', the_map_dictionary[board_place]['Building'])
            print('\t', 'Cost to build:', the_map_dictionary[board_place]['BuildingCost'])
            print('\t', 'Rent:', the_map_dictionary[board_place]['Rent'] + ',', end=' ')
            print(the_map_dictionary[board_place]['BuildingRent'], '(with building)')
            print()
    if not found_result:
        print('Could not find the name or abbreviation')
    pass


# Get Player Info; list players, asks what player you would like to know about, then outputs that information
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
            # determines if this player is the owner of any properties
            if player_one['Name'] == the_map_dictionary[name_scanning]['Owner']:
                print('\t', the_map_dictionary[name_scanning]['Place'], end=',')
                # then will determine if they own any buildings on that property
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


# Build a Building; asks where you want to build on, then subtracts and places a building on the property
def option_four(current_player, current_position):
    mod_current_position = current_position % len(the_map_dictionary)
    print('You have', current_player['Current_Money'], CURRENCY, 'and can build on: ')
    # scans through entire dictionary
    for name_scanning in range(len(the_map_dictionary)):
        # pulls out the properties that you own
        if current_player['Name'] == the_map_dictionary[name_scanning]['Owner']:
            # pulls out the properties that don't already have a building
            if the_map_dictionary[name_scanning]['Building'] == 'No':
                print('\t', the_map_dictionary[name_scanning]['Place'], '|', the_map_dictionary[name_scanning]['Abbrev']
                      , '|', the_map_dictionary[name_scanning]['BuildingCost'])

    building_choice = input('Enter the abbreviation of the property that you would you like to build on: ')
    for scanning in range(len(the_map_dictionary)):
        if building_choice == the_map_dictionary[scanning]['Abbrev']:
            if (current_player['Current_Money'] - int(the_map_dictionary[mod_current_position]['BuildingCost'])) > 0:
                if current_player['Name'] == the_map_dictionary[scanning]['Owner']:
                    if the_map_dictionary[scanning]['Building'] == 'No':
                        the_map_dictionary[scanning]['Building'] = 'Yes'
                        current_player['Owned_Buildings'].append(mod_current_position)
                        current_player['Current_Money'] -= int(the_map_dictionary[mod_current_position]['BuildingCost'])
                        print('You have built the building for', the_map_dictionary[scanning]['Place'])
                        print('You now have', current_player['Current_Money'], 'Retriever Ducats remaining.')
                    else:
                        print('There is already a building on this property.')
                else:
                    print('You do not own this property.')
            else:
                print('You do not have the funds to build.')

    pass


# Every dice roll, this function runs to see if the user has made a full rotation around the board
def pass_go_checker(individual_player):
    if individual_player['Name'] == player_one['Name']:
        if (individual_player['Position'] // (len(the_map_dictionary))) not in used_rotation_player_one:
            individual_player['Current_Money'] += PASSING_MONEY
            individual_player['Passed_Go_Rotations'] = (individual_player['Position'] // len(the_map_dictionary))
            used_rotation_player_one.append(individual_player['Passed_Go_Rotations'])
            return True
    if individual_player['Name'] == player_two['Name']:
        if (individual_player['Position'] // (len(the_map_dictionary))) not in used_rotation_player_two:
            individual_player['Current_Money'] += PASSING_MONEY
            individual_player['Passed_Go_Rotations'] = (individual_player['Position'] // len(the_map_dictionary))
            used_rotation_player_two.append(individual_player['Passed_Go_Rotations'])
            return True


# simple function to take in a players information to turn their numbered position into the name the place on the board
def check_location(player):
    for positions in range(len(the_map_dictionary)):
        if str(player['Position'] % len(the_map_dictionary)) == the_map_dictionary[positions]['Position']:
            matched_name = the_map_dictionary[positions]['Place']
            return matched_name


# Turns the board data into a list of strings that are in the correct format to print the board
def format_display(board):
    string_for_function = []
    # first adds the abbreviations to the list
    for y in range(len(board)):
        list_format = list(board[y]['Abbrev'])
        # then if that list is less than 5 characters, spaces will be added until it is 5 characters
        while len(list_format) < 5:
            list_format.append(' ')
        # the 6th character must be a '/n'
        list_format.append('\n')
        position_string_one = str(player_one['Position'] % len(board))
        position_string_two = str(player_two['Position'] % len(board))
        # only applies to the "Start" position on the board
        if int(board[y]['Position']) == 0:
            # unicode finger sign, represents "Go" as in the real monopoly board
            list_format.append('\u261C')
        # only applies if player ones position is on that specific board position
        if position_string_one == board[y]['Position']:
            list_format.append(player_one['Symbol'])
        # only applies if player twos position is on that specific board position
        if position_string_two == board[y]['Position']:
            list_format.append(player_two['Symbol'])
        # only applies if player one owns a property
        if board[y]['Owner'] == player_one['Name']:
            # unicode symbol of a white flag, representing the property is owned
            list_format.append('\u2691')
        # only applies if player two owns a property
        if board[y]['Owner'] == player_two['Name']:
            # unicode symbol of a black flag, representing the property is owned
            list_format.append('\u2690')
        # only applies if there is a building on a specific board position
        if board[y]['Building'] != 'No':
            # unicode symbol of a house, to represent a building is built there
            list_format.append('\u2302')
        while len(list_format) < 11:
            list_format.append(' ')
        # this list if then joined together to become an individual string series
        joined_string = ''.join(list_format)
        # that string is then appended to a list that will contain the strings of each position on the board
        string_for_function.append(joined_string)
    return string_for_function


if __name__ == '__main__':

    # allows the .csv file to be put into a variable to store and change values in the dictionary
    the_map_dictionary = load_map('proj1_board1.csv')
    print('1. Large board')
    print('2. Small board')
    map_selection = int(input('Enter the number for the board that you would you like to use (large by default): '))
    if map_selection == 1:
        the_map_dictionary = load_map('proj1_board1.csv')
    if map_selection == 2:
        the_map_dictionary = load_map('proj1_board2.csv')

    # appends "starter keys" to the dictionary
    for owned_and_buildings in range(len(the_map_dictionary)):
        the_map_dictionary[owned_and_buildings]['Owner'] = 'BANK'
        the_map_dictionary[owned_and_buildings]['Building'] = 'No'

    # Player 1 requested info
    player_one['Name'] = input('First player, what is your name? ')
    symbol_one = input('First player, what symbol do you want your character to use? ')
    player_one['Symbol'] = symbol_one.upper()
    while len(list(player_one['Symbol'])) != 1:
        symbol_one = input('Please enter a 1-Character symbol: ')
        player_one['Symbol'] = symbol_one.upper()

    # Player 2 requested info
    player_two['Name'] = input('Second player, what is your name? ')
    symbol_two = input('Second player, what symbol do you want your character to use? ')
    player_two['Symbol'] = symbol_two.upper()
    while len(list(player_two['Symbol'])) != 1:
        symbol_two = input('Please enter a 1-Character symbol: ')
        player_two['Symbol'] = symbol_two.upper()

    # begins the series of functions to play the game
    play_game(START_MONEY)
