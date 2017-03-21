import tkinter as tk

image_assets_10x10 = {'white'  : "assets/white_square_10x10.ppm",
                      'red'    : "assets/red_square_10x10.ppm",
                      'yellow' : "assets/yellow_square_10x10.ppm",
                      'green'  : "assets/green_square_10x10.ppm",
                      'blue'   : "assets/blue_square_10x10.ppm",
                      'grey'   : "assets/grey_square_10x10.ppm"}

image_assets_40x40 = {'white'  : "assets/white_square_40x40.ppm",
                      'red'    : "assets/red_square_40x40.ppm",
                      'yellow' : "assets/yellow_square_40x40.ppm",
                      'green'  : "assets/green_square_40x40.ppm",
                      'blue'   : "assets/blue_square_40x40.ppm"}

class PlayArea(tk.Frame):
    '''
    This class renders a 20x20 play area and packs into a parent window.
    '''

    def __init__(self, parent, rows=20, columns=20,
        colour_set=image_assets_40x40, pad=1):
        tk.Frame.__init__(self, parent, background="black")
        self.parent = parent
        self.name = 'playarea'
        self.colour_set = colour_set
        photo = tk.PhotoImage(file=self.colour_set['white'])
        self.squares = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                sqr = Square(self, image=photo, row=row, column=column)
                sqr.photo = photo
                sqr.grid(row=row, column=column, sticky="NSEW", padx=pad,
                    pady=pad)
                current_row.append(sqr)
            self.squares.append(current_row)
        self.pack(side="left")

    def colour_squares(self, colour, shape, r_offset=0, c_offset=0):
        numrows = len(shape)
        numcols = len(shape[0])
        for row in range(numrows):
            for column in range(numcols):
                if (shape[row][column]):
                    try:
                        sqr = self.squares[row+r_offset][column+c_offset]
                        if colour == 'clear':
                            sqr.colour = sqr.true_colour
                        else:
                            sqr.colour = colour
                        photo = tk.PhotoImage(file=self.colour_set[sqr.colour])
                        sqr.configure(image = photo)
                        sqr.photo = photo
                        sqr.grid(row=row+r_offset, column=column+c_offset)
                    except IndexError as e:
                        pass

    def clear_squares(self, shape, r_offset=0, c_offset=0):
        self.colour_squares('clear', shape, r_offset, c_offset)

    def get_grid_coordinates(self, grid_info):
        try:
            row = grid_info['row']
            column = grid_info['column']
            return (int(row), int(column))
        except KeyError as e:
            return None

    def place_shape_on_board(self, grid_info, shapes):
        (r_offset, c_offset) = self.get_grid_coordinates(grid_info)
        shape = shapes.current_shape.matrix
        numrows = len(shape)
        numcols = len(shape[0])
        for row in range(numrows):
            for column in range(numcols):
                if (shape[row][column]):
                    try:
                        sqr = self.squares[row+r_offset][column+c_offset]
                        sqr.true_colour = shapes.colour
                        sqr.captured = True
                        sqr.grid(row=row+r_offset, column=column+c_offset)
                    except IndexError as e:
                        pass

    def check_move(self, grid_info, current_player):
        (r_offset, c_offset) = self.get_grid_coordinates(grid_info)
        shapes = current_player.shapes
        shape = shapes.current_shape.matrix
        score = current_player.score
        numrows = len(shape)
        numcols = len(shape[0])
        diagonally_adjacent = False
        corner_square = False
        for row in range(numrows):
            for column in range(numcols):
                if (shape[row][column]):
                    try:
                        if self.squares[row+r_offset][column+c_offset].captured is True:
                            return True,'overlap'
                        if ((row+r_offset==0 and column+c_offset==0) # REVISIT must change to size of board
                        or   (row+r_offset==0 and column+c_offset==19)
                        or   (row+r_offset==19 and column+c_offset==0)
                        or   (row+r_offset==19 and column+c_offset==19)):
                            corner_square = True
                    except IndexError as e:
                        return True,'index'
                    try:
                        if (shapes.colour == self.squares[row+r_offset-1][column+c_offset].true_colour
                        or  shapes.colour == self.squares[row+r_offset+1][column+c_offset].true_colour
                        or  shapes.colour == self.squares[row+r_offset][column+c_offset-1].true_colour
                        or  shapes.colour == self.squares[row+r_offset][column+c_offset+1].true_colour):
                            return True,'adjacent'
                    except IndexError as e:
                        pass
                    try:
                        if (shapes.colour == self.squares[row+r_offset-1][column+c_offset-1].true_colour
                        or  shapes.colour == self.squares[row+r_offset-1][column+c_offset+1].true_colour
                        or  shapes.colour == self.squares[row+r_offset+1][column+c_offset-1].true_colour
                        or  shapes.colour == self.squares[row+r_offset+1][column+c_offset+1].true_colour):
                            diagonally_adjacent = True
                    except IndexError as e:
                        pass
        if score == 0:
            if corner_square is False:
                return True,'corner'
        else:
            if diagonally_adjacent is False:
                return True,'diagonal'
        return False,'okay'

class ShapeArea(tk.Frame):
    '''
    This class renders a 7x3 display of available shapes and packs into a parent
    window.
    '''

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="black")
        self.parent = parent
        self.name = 'shapearea'
        self.sub_frames = []
        for row in range(7):
            self.sub_frames.append(tk.Frame(self, background="black"))
        self.blocks = []
        j=0
        for row in range(7):
            for column in range(3):
                block = PlayArea(self.sub_frames[row], rows=5, columns=5,
                    colour_set=image_assets_10x10, pad=0)
                block.name = 'sub_shapearea'
                block.shape_number = j
                block.colour_squares('white',[[0]])
                block.configure(highlightthickness=2,
                    highlightbackground='gray')
                block.pack(side='left')
                self.blocks.append(block)
                j+=1
            self.sub_frames[row].pack(side='top')
        self.selected_block = self.blocks[0]
        self.selected_block.configure(highlightbackground="yellow")
        self.pack(side="bottom")

    def add_player_shapes(self, shapes):
        j=0
        for row in range(7):
            for column in range(3):
                block = self.blocks[j]
                if shapes.shape_map[j].used is False:
                    colour = shapes.colour
                else:
                    colour = 'grey'
                block.colour_squares(colour,shapes.shape_map[j].matrix)
                self.blocks[j] = block
                j+=1

    def remove_player_shapes(self, shapes):
        j=0
        for row in range(7):
            for column in range(3):
                block = self.blocks[j]
                block.clear_squares(shapes.shape_map[j].matrix)
                self.blocks[j] = block
                j+=1

    def change_frame_selection(self, frame):
        self.selected_block.configure(highlightbackground="gray")
        self.selected_block = frame
        self.selected_block.configure(highlightbackground="yellow")


    def get_selected_shape_index(self):
        return self.selected_block.shape_number

    def transform_shape(self, frame, shapes, transform):
        self.change_frame_selection(frame)
        self.selected_block.clear_squares(
            shapes.current_shape.matrix)
        if transform == 'rotate':
            shapes.rotate_shape()
        elif transform == 'flip':
            shapes.flip_shape()
        self.selected_block.colour_squares(shapes.colour,
            shapes.current_shape.matrix)

class ScoreArea(tk.Frame):
    '''
    This class renders a score area and packs into a parent window.
    '''

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="black")

class Square(tk.Label):
    '''
    This class is a single square on the board.
    '''

    def __init__(self, parent, image, row, column):
        tk.Label.__init__(self, parent, borderwidth=0, image=image)
        self.parent = parent
        self.name = 'square'
        self.row = row
        self.column = column
        self.colour = 'white'
        self.true_colour = 'white'
        self.captured = False
