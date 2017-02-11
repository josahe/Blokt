class Shapes:
    '''
    This class describes a user's shapes.
    '''
    shape_map = {1:  [[1]],
                 2:  [[1], [1]],
                 3:  [[1], [1], [1]],
                 4:  [[1, 0], [1, 1]],
                 5:  [[1], [1], [1], [1]],
                 6:  [[0, 1], [0, 1], [1, 1]],
                 7:  [[1, 0], [1, 1], [1, 0]],
                 8:  [[1, 1], [1, 1]],
                 9:  [[1, 1, 0], [0, 1, 1]],
                 10: [[1], [1], [1], [1], [1]],
                 11: [[0, 1], [0, 1], [0, 1], [1, 1]],
                 12: [[0, 1], [0, 1], [1, 1], [1, 0]],
                 13: [[0, 1], [1, 1], [1, 1]],
                 14: [[1, 1], [0, 1], [1, 1]],
                 15: [[1, 0], [1, 1], [1, 0], [1, 0]],
                 16: [[0, 1, 0], [0, 1, 0], [1, 1, 1]],
                 17: [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
                 18: [[1, 1, 0], [0, 1, 1], [0, 0, 1]],
                 19: [[1, 0, 0], [1, 1, 1], [0, 0, 1]],
                 20: [[1, 0, 0], [1, 1, 1], [0, 1, 0]],
                 21: [[0, 1, 0], [1, 1, 1], [0, 1, 0]]}


    def __init__(self):
        self.shape_map = Shapes.shape_map

    def rotate_shape_old(original):
        rotated = zip(*original[::-1])
        return rotated

    def rotate_shape(self, number):
        self.shape_map[number] = zip(*self.shape_map[number][::-1])
        self.shape_map[number] = map(list, self.shape_map[number])

    def flip_shape(self, number):
        for x in self.shape_map[number]:
            x.reverse()
