from src.backend.shapes import Shapes

class Players(object):
    '''This class keeps a record of every player object, manages whose turn it
    is, and communicates with the Board class.
    '''
    def __init__(self, number_of_players=4):
        self.number_of_players = number_of_players
        self._players = []
        self._player = self.update_active_player()
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
        self.active_player = next(self._player)

    def update_active_player(self):
        while True:
            for i in range(self.number_of_players):
                yield self._players[i]

    def end_turn(self):
        self.active_player.score += self.active_player.shapes.active_shape.value
        self.active_player.shapes.active_shape.used = True
        while self.active_player.shapes.active_shape.used is True:
            if self.active_player.shapes.all_shapes_used() is True:
                self.active_player.eliminate()
                break
            self.active_player.shapes.update_active_shape('previous')

    def start_turn(self):
        if self.active_player.out is True:
            temp_player = self.active_player
            self.active_player = next(self._player)
        else:
            self.active_player = next(self._player)
            temp_player = self.active_player
        while self.active_player.out is True:
            self.active_player = next(self._player)
            if self.active_player == temp_player:
                return False
        return True

class Player(object):
    '''This class keeps a record of a single player's attributes.
    '''
    def __init__(self, name, colour, shapes):
        self.name = name
        self.colour = colour
        self.shapes = shapes
        self.shapes.set_colour(self.colour)
        self.score = 0
        self.out = False

    def eliminate(self):
        self.out = True
