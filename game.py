'''The main game file, which you run to run the game.
run_game() runs demo mode by default.'''

from math import hypot
from os import get_terminal_size
from random import choice, randrange

import script


DIVIDER = '-' * get_terminal_size()[0]
MOVEMENT_OPERATORS = {'+': 1, '-': -1, '': 0}

class Game:
    '''Handles in-game abstractions'''
    def __init__(self, dimensions, size, demo):
        self.demo = demo
        self.dimensions = dimensions
        self.size = size

        dimension_center = int(self.size / 2)
        self.dimension_range = range(dimensions)

        self.goal = tuple(map(lambda _: randrange(self.size), self.dimension_range))
        self.player_location = tuple(map(lambda _: dimension_center, self.dimension_range))

    def get_movement(self, velocity):
        '''Retrieves movement data from the player'''
        def demo_movement():
            def get_operator_input(dimension):
                return validate_input(
                    message=f'Movement in dimension {dimension}: ',
                    condition=lambda x: x in MOVEMENT_OPERATORS.keys(),
                    failure_message='Please enter "+", "-", or nothing at all.'
                )

            print(DIVIDER)
            print('Coordinates:', self.player_location)
            print('Current velocity:', str(velocity))
            return map(get_operator_input, self.dimension_range)

        movement = demo_movement() if self.demo else script.move(velocity)
        return map(lambda x: MOVEMENT_OPERATORS[x], movement)

    def move_player(self, movement):
        '''Where the action happens'''
        self.player_location = tuple(map(sum, zip(self.player_location, movement)))

def eat_food():
    '''Victory message'''
    with open('foods.txt', 'r') as foods_file:
        foods = list(foods_file)
    food = choice(foods)
    food = food.rstrip('\n')
    print(f'The mouse finds {food} and scarfs it down. Good job!')

def get_bool_input(message):
    '''Gets boolean input from the terminal'''
    values = {'y': True, 'yes': True, 'n': False, 'no': False, '': False}
    return values[validate_input(
        message=message,
        condition = lambda x: x in values,
        failure_message='Please enter input that can be parsed as "yes" or "no".'
    )]

def get_int_input(message):
    '''Gets an integer input from the terminal'''
    def converts_to_int(check_string):
        try:
            int(check_string)
        except ValueError:
            return False
        else:
            return True

    return int(validate_input(
        message=message,
        condition=lambda x: converts_to_int(x) and int(x) > 0,
        failure_message='Please enter a positive integer.'
    ))

def get_game_details(demo):
    '''Defines the size and dimension of the game by user input'''
    def demo_game_details():
        '''Uses get_int_input to get game details from the user'''
        def succinct_game_details():
            return map(get_int_input, (
                'How many units long would you like this game to be in each dimension? ',
                'In how many dimensions would you like to play? '
            ))

        def tutorial_game_details():
            details = size, dimensions = 5, 3
            print(DIVIDER)
            with open('tutorial.txt', 'r') as tutorial_text:
                print(tutorial_text.read())
            print(f'We will set this first game to {dimensions} dimensions, each of length {size}.')
            return details

        tutorial = get_bool_input('Would you like to play the tutorial? (y/n)')
        return tutorial_game_details() if tutorial else succinct_game_details()

    return demo_game_details() if demo else (script.game_size, script.game_dimensions)

def run_game(demo=True):
    '''The main game loop
    The tutorial is available within demo mode.'''
    def play_and_get_moves():
        '''Runs the actual gameplay; returns the number of moves the player took'''
        velocity = moves = 0
        to_position = game.player_location
        abs_difference = lambda x, y: abs(x - y)
        abs_difference_of_tuple = lambda x: abs_difference(*x)
        distance = lambda address1, address2: hypot(*map(abs_difference_of_tuple, zip(address1, address2)))
        get_velocity = (
            lambda goal, from_address, to_address:
            distance(from_address, goal) - distance(to_address, goal)
        )
        while tuple(to_position) != game.goal:
            from_position = to_position
            game.move_player(game.get_movement(velocity))
            to_position = game.player_location
            velocity = get_velocity(game.goal, from_position, to_position)
            moves += 1
        return moves

    if demo:
        with open('intro.txt', 'r') as intro_text:
            print(DIVIDER, intro_text.read(), DIVIDER, sep='\n')
    game_size, game_dimensions = get_game_details(demo)
    game = Game(game_dimensions, game_size, demo)
    moves = play_and_get_moves()
    if demo:
        eat_food()
    print(f'You won in only {moves} moves!')

def validate_input(message, condition, failure_message):
    '''Applies a condition to input to check it'''
    text = input(message)
    text_valid = condition(text)
    while not text_valid:
        text = input(failure_message)
        text_valid = condition(text)
    return text

if __name__ == '__main__':
    run_game()
