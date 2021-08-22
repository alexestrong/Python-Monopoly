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

string_for_function = []


def format_display(player_one, player_two, board):
    for y in range(len(board)):
        list_format = list(board[y]['Abbrev'])
        while len(list_format) < 5:
            list_format.append(' ')
        list_format.append('\n')
        position_string_one = str(player_one['Position'] % len(board))
        position_string_two = str(player_two['Position'] % len(board))
        if position_string_one == board[y]['Position'] and position_string_two == board[y]['Position']:
            list_format.append(player_one['Symbol'])
            list_format.append(' ')
            list_format.append('&')
            list_format.append(' ')
            list_format.append(player_two['Symbol'])
        elif position_string_one == board[y]['Position']:
            list_format.append(player_one['Symbol'])
        elif position_string_two == board[y]['Position']:
            list_format.append(player_two['Symbol'])
        while len(list_format) < 11:
            list_format.append(' ')
        joined_string = ''.join(list_format)
        string_for_function.append(joined_string)
        print(list_format)
        print(position_string_one, board[y]['Position'])
        print(position_string_one == board[y]['Position'])
    # print(string_for_function)

#    updated_board_func = display_board(string_for_function)
#    print(updated_board_func)
    return string_for_function


def play_game(starting_money, board_file):
    player_one['Current_Money'] = starting_money
    player_two['Current_Money'] = starting_money
    while player_one['Current_Money'] or player_two['Current_Money'] != 0:
        take_turn(player_one, board_file)
        take_turn(player_two, board_file)

    pass


def take_turn(player, board):
    dice_roll = randint(1, 6) + randint(1, 6)
    player['Position'] += dice_roll
    format_display(player_one, player_two, the_map_dictionary)
    print(player['Name'], 'you have rolled a', dice_roll)
    user_choice = input('What would you like to do?')
    return user_choice

    pass


map_list = []
player_one = {'Position': 0, 'Current_Money': 0}
player_two = {'Position': 0, 'Current_Money': 0}

if __name__ == '__main__':

    the_map_dictionary = load_map('proj1_board2.csv')
    # print(the_map)

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
    formatted_map = format_display(player_one, player_two, the_map_dictionary)
    display_board(formatted_map)
    print(player_one)
    print(player_two)
