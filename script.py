'''Modify this file, especially move(), to play Zoom Mouse by script.'''

from collections import namedtuple
from random import randint # needed only for sample code

game_dimensions = 3
game_size = 5

Log = namedtuple('Log', ['movement', 'velocity'])
logs = []

def move(velocity):
    '''The function run by the game to get new movements
    Returns an iterable of length game_size of integers.
    Give this some better logic.'''
    movement = [randint(-game_size, game_size) for _ in range(game_dimensions)] # definitely edit this
    logs.append(Log(movement, velocity))
    return movement
