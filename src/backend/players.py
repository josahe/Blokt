from src.backend.shapes import Shapes

class Players(object):
    '''This class keeps a record of every player object, manages whose turn it
    is, and communicates with the Board class'''

    def __init__(self, number_of_players=4):
        self.number_of_players = number_of_players
        self._players = []
        if (self.number_of_players >= 2):
            self._players.append(Player(name='player1', colour='blue',
                shapes=Shapes()))
            self._players.append(Player(name='player2', colour='green',
                shapes=Shapes()))
        if (self.number_of_players == 4):
            self._players.append(Player(name='player3', colour='red',
                shapes=Shapes()))
            self._players.append(Player(name='player4', colour='yellow',
                shapes=Shapes()))
        self.current_player_index = 0
        self.current_player = self._players[self.current_player_index]

    def update_current_player(self):
        self.current_player_index += 1
        if self.current_player_index > (self.number_of_players-1):
            self.current_player_index = 0
        self.current_player = self._players[self.current_player_index]

    def end_turn(self):
        self.current_player.score += self.current_player.shapes.current_shape.value
        self.current_player.shapes.current_shape.used = True
        while self.current_player.shapes.current_shape.used is True:
            if self.current_player.shapes.all_shapes_used() is True:
                self.current_player.eliminate()
                break
            self.current_player.shapes.update_current_shape()

    def start_turn(self):
        if self.current_player.out is True:
            temp_player = self.current_player
            self.update_current_player()
        else:
            self.update_current_player()
            temp_player = self.current_player
        while self.current_player.out is True:
            self.update_current_player()
            if self.current_player == temp_player:
                return False
        return True

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
        self.out = False

    def update_score(self, new_score):
        self.score = new_score

    def get_score(self):
        return self.score

    def eliminate(self):
        self.out = True
