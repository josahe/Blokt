class Shape(object):
    '''This class describes a single shape.
    '''
    def __init__(self, matrix):
        self.matrix = matrix
        self.used = False
        self.value = 0
        for m in self.matrix:
            self.value += m.count(1)

class Shapes(object):
    '''This class describes a user's shapes.
    '''
    def __init__(self):
        self.shape_map = {0:  Shape([[1]]),
                          1:  Shape([[1], [1]]),
                          2:  Shape([[1], [1], [1]]),
                          3:  Shape([[1, 0], [1, 1]]),
                          4:  Shape([[1], [1], [1], [1]]),
                          5:  Shape([[0, 1], [0, 1], [1, 1]]),
                          6:  Shape([[1, 0], [1, 1], [1, 0]]),
                          7:  Shape([[1, 1], [1, 1]]),
                          8:  Shape([[1, 1, 0], [0, 1, 1]]),
                          9:  Shape([[1], [1], [1], [1], [1]]),
                          10: Shape([[0, 1], [0, 1], [0, 1], [1, 1]]),
                          11: Shape([[0, 1], [0, 1], [1, 1], [1, 0]]),
                          12: Shape([[0, 1], [1, 1], [1, 1]]),
                          13: Shape([[1, 1], [0, 1], [1, 1]]),
                          14: Shape([[1, 0], [1, 1], [1, 0], [1, 0]]),
                          15: Shape([[0, 1, 0], [0, 1, 0], [1, 1, 1]]),
                          16: Shape([[1, 0, 0], [1, 0, 0], [1, 1, 1]]),
                          17: Shape([[1, 1, 0], [0, 1, 1], [0, 0, 1]]),
                          18: Shape([[1, 0, 0], [1, 1, 1], [0, 0, 1]]),
                          19: Shape([[1, 0, 0], [1, 1, 1], [0, 1, 0]]),
                          20: Shape([[0, 1, 0], [1, 1, 1], [0, 1, 0]])}
        self.name = 'shapes'
        self.active_shape_index = 20
        self.active_shape = self.shape_map[self.active_shape_index]

    def update_active_shape(self, next_shape_index=None):
        if next_shape_index == 'next':
            self.active_shape_index += 1
            if self.active_shape_index > 20:
                self.active_shape_index = 0
        elif next_shape_index == 'previous':
            self.active_shape_index -= 1
            if self.active_shape_index < 0:
                self.active_shape_index = 20
        else:
            self.active_shape_index = next_shape_index
        self.active_shape = self.shape_map[self.active_shape_index]

    def rotate_shape(self):
        self.active_shape.matrix = list(zip(*self.active_shape.matrix[::-1]))
        self.active_shape.matrix = list(map(list, self.active_shape.matrix))

    def rotate_right(self):
        self.rotate_shape()

    def rotate_left(self):
        for i in range(3):
            self.rotate_shape()

    def flip_shape(self):
        for x in self.active_shape.matrix:
            x.reverse()

    def flip_horizontal(self):
        self.flip_shape()

    def flip_vertical(self):
        self.rotate_right()
        self.flip_horizontal()
        self.rotate_left()

    def set_colour(self, colour):
        self.colour = colour

    def all_shapes_used(self):
        num_shapes_used = 0
        for i in self.shape_map:
            if self.shape_map[i].used is True:
                num_shapes_used += 1
        if num_shapes_used == 21:
            return True
        return False
