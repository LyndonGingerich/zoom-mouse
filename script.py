'''Modify this file, especially move(), to play Gridmaus by script.'''

from collections import namedtuple
from random import choice # needed only for sample code

game_dimensions = 3
game_size = 5

Log = namedtuple('Log', ['movement', 'velocity'])
logs = []

def move(velocity):
    '''The function run by the game to get new movements
    Returns an iterable of length game_size of values from movement_operators.
    Give this some better logic.'''
    movement_operators = ('+', '-', '')
    movement = [choice(movement_operators) for _ in range(game_dimensions)] # definitely edit this
    logs.append(Log(movement, velocity))
    return movement
