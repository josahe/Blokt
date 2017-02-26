class Shapes:
    '''
    This class describes a user's shapes.
    '''

    shape_map = {0:  [[1]],
                 1:  [[1], [1]],
                 2:  [[1], [1], [1]],
                 3:  [[1, 0], [1, 1]],
                 4:  [[1], [1], [1], [1]],
                 5:  [[0, 1], [0, 1], [1, 1]],
                 6:  [[1, 0], [1, 1], [1, 0]],
                 7:  [[1, 1], [1, 1]],
                 8:  [[1, 1, 0], [0, 1, 1]],
                 9:  [[1], [1], [1], [1], [1]],
                 10: [[0, 1], [0, 1], [0, 1], [1, 1]],
                 11: [[0, 1], [0, 1], [1, 1], [1, 0]],
                 12: [[0, 1], [1, 1], [1, 1]],
                 13: [[1, 1], [0, 1], [1, 1]],
                 14: [[1, 0], [1, 1], [1, 0], [1, 0]],
                 15: [[0, 1, 0], [0, 1, 0], [1, 1, 1]],
                 16: [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
                 17: [[1, 1, 0], [0, 1, 1], [0, 0, 1]],
                 18: [[1, 0, 0], [1, 1, 1], [0, 0, 1]],
                 19: [[1, 0, 0], [1, 1, 1], [0, 1, 0]],
                 20: [[0, 1, 0], [1, 1, 1], [0, 1, 0]]}

    colours1 = {'white'  : "assets/white_square_10x10.ppm",
                'red'    : "assets/red_square_10x10.ppm",
                'yellow' : "assets/yellow_square_10x10.ppm",
                'green'  : "assets/green_square_10x10.ppm",
                'blue'   : "assets/blue_square_10x10.ppm",
                'grey'   : "assets/grey_square_10x10.ppm"}

    colours4 = {'white'  : "assets/white_square_40x40.ppm",
                'red'    : "assets/red_square_40x40.ppm",
                'yellow' : "assets/yellow_square_40x40.ppm",
                'green'  : "assets/green_square_40x40.ppm",
                'blue'   : "assets/blue_square_40x40.ppm"}

    def __init__(self):
        self.shape_map = Shapes.shape_map
        self.colours4 = Shapes.colours4
        self.colours1 = Shapes.colours1
        self.name='shapes'

    def rotate_shape(self, number):
        self.shape_map[number] = zip(*self.shape_map[number][::-1])
        self.shape_map[number] = map(list, self.shape_map[number])

    def flip_shape(self, number):
        for x in self.shape_map[number]:
            x.reverse()
