from src.gui.shapes import Shapes

class Players(object):
    '''This class keeps a record of every player object, manages whose turn it
    is, and communicates with the Board class'''

    def __init__(self, number_of_players=4):
        self._players = []
        if (number_of_players >= 2):
            self._players.append(Player(name='player1', colour='blue',
                shapes=Shapes()))
            self._players.append(Player(name='player2', colour='green',
                shapes=Shapes()))
        if (number_of_players == 4):
            self._players.append(Player(name='player3', colour='red',
                shapes=Shapes()))
            self._players.append(Player(name='player4', colour='yellow',
                shapes=Shapes()))
        self.current_player_index = 0
        self.current_player = self._players[self.current_player_index]

    def update_current_player(self):
        self.current_player_index += 1
        if self.current_player_index > 3:
            self.current_player_index = 0
        self.current_player = self._players[self.current_player_index]

    def end_turn(self):
        #update score
        self.current_player.score += self.current_player.shapes.current_shape.value
        #disable used shape
        self.current_player.shapes.current_shape.used = True
        #select next available shape
        while self.current_player.shapes.current_shape.used is not False:
            self.current_player.shapes.update_current_shape()

    def start_turn(self):
        #select next player
        self.update_current_player()

    def print_score(self):
        for p in self._players:
            print(p.name,p.score)

class Player(object):
    '''This class keeps a record of a single player's attributes, such as their
    colour, their shapes and their score'''

    def __init__(self, name, colour, shapes):
        self.name = name
        self.colour = colour
        self.shapes = shapes
        self.shapes.set_colour(self.colour)
        self.score = 0

    def update_score(self, new_score):
        self.score = new_score

    def get_score(self):
        return self.score
