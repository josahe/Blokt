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
                      'blue'   : "assets/blue_square_40x40.ppm",
                      'start'  : "assets/start_square_40x40.ppm"}

class PlayArea(tk.Frame):
    '''
    This class renders a 20x20 play area.
    '''

    def __init__(self, parent, number_of_players,
        colour_set=image_assets_40x40, pad=1):
        tk.Frame.__init__(self, parent, background="black")
        self.parent = parent
        self.name = 'playarea'
        self.colour_set = colour_set
        self.squares = []
        self.number_of_players = number_of_players
        if self.number_of_players == 2:
            self.rows = 14
            self.columns = 14
            self.edge = 13
        elif self.number_of_players == 4:
            self.rows = 20
            self.columns = 20
            self.edge = 19
        elif self.number_of_players == 0:
            self.rows = 5
            self.columns = 5
            self.edge = 0
        else:
            raise ValueError
            return None
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                if self.number_of_players == 2:
                    if ((row==4 and column==self.edge-4)
                    or  (row==self.edge-4 and column==4)):
                        photo = tk.PhotoImage(file=self.colour_set['start'])
                        sqr = Square(self, image=photo, row=row, column=column)
                        sqr.photo = photo
                        sqr.true_colour = 'start'
                    else:
                        photo = tk.PhotoImage(file=self.colour_set['white'])
                        sqr = Square(self, image=photo, row=row, column=column)
                        sqr.photo = photo
                elif self.number_of_players == 4:
                    if ((row==0 and column==0)
                    or  (row==0 and column==self.edge)
                    or  (row==self.edge and column==0)
                    or  (row==self.edge and column==self.edge)):
                        photo = tk.PhotoImage(file=self.colour_set['start'])
                        sqr = Square(self, image=photo, row=row, column=column)
                        sqr.photo = photo
                        sqr.true_colour = 'start'
                    else:
                        photo = tk.PhotoImage(file=self.colour_set['white'])
                        sqr = Square(self, image=photo, row=row, column=column)
                        sqr.photo = photo
                else:
                    photo = tk.PhotoImage(file=self.colour_set['white'])
                    sqr = Square(self, image=photo, row=row, column=column)
                    sqr.photo = photo
                sqr.grid(row=row, column=column, sticky="NSEW", padx=pad,
                    pady=pad)
                current_row.append(sqr)
            self.squares.append(current_row)

    def colour_squares(self, colour, shape, r_offset=0, c_offset=0):
        for row in range(len(shape)):
            for column in range(len(shape[0])):
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
        for row in range(len(shape)):
            for column in range(len(shape[0])):
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
        diagonally_adjacent = False
        starting_square = False
        for row in range(len(shape)):
            for column in range(len(shape[0])):
                if (shape[row][column]):
                    # --- OVERLAP/CORNER ---
                    if row+r_offset in range(self.edge+1) and column+c_offset in range(self.edge+1):
                        if self.squares[row+r_offset][column+c_offset].captured is True:
                            return True,'overlap'
                        if self.number_of_players == 2:
                            if ((row+r_offset==4 and column+c_offset==self.edge-4)
                            or  (row+r_offset==self.edge-4 and column+c_offset==4)):
                                starting_square = True
                        else:
                            if ((row+r_offset==0 and column+c_offset==0)
                            or  (row+r_offset==0 and column+c_offset==self.edge)
                            or  (row+r_offset==self.edge and column+c_offset==0)
                            or  (row+r_offset==self.edge and column+c_offset==self.edge)):
                                starting_square = True
                    else:
                        return True,'index'
                    # --- ADJACENT ---
                    if row+r_offset-1 in range(self.edge+1):
                        if shapes.colour == self.squares[row+r_offset-1][column+c_offset].true_colour:
                            return True,'adjacent'
                    if row+r_offset+1 in range(self.edge+1):
                        if shapes.colour == self.squares[row+r_offset+1][column+c_offset].true_colour:
                            return True,'adjacent'
                    if column+c_offset-1 in range(self.edge+1):
                        if shapes.colour == self.squares[row+r_offset][column+c_offset-1].true_colour:
                            return True,'adjacent'
                    if column+c_offset+1 in range(self.edge+1):
                        if shapes.colour == self.squares[row+r_offset][column+c_offset+1].true_colour:
                            return True,'adjacent'
                    # --- DIAGONAL ---
                    if row+r_offset-1 in range(self.edge+1) and column+c_offset-1 in range(self.edge+1):
                        if shapes.colour == self.squares[row+r_offset-1][column+c_offset-1].true_colour:
                            diagonally_adjacent = True
                    if row+r_offset-1 in range(self.edge+1) and column+c_offset+1 in range(self.edge+1):
                        if shapes.colour == self.squares[row+r_offset-1][column+c_offset+1].true_colour:
                            diagonally_adjacent = True
                    if row+r_offset+1 in range(self.edge+1) and column+c_offset-1 in range(self.edge+1):
                        if shapes.colour == self.squares[row+r_offset+1][column+c_offset-1].true_colour:
                            diagonally_adjacent = True
                    if row+r_offset+1 in range(self.edge+1) and column+c_offset+1 in range(self.edge+1):
                        if shapes.colour == self.squares[row+r_offset+1][column+c_offset+1].true_colour:
                            diagonally_adjacent = True
        # --- CORNER ---
        if score == 0:
            if starting_square is False:
                return True,'corner'
        # --- DIAGONAL ---
        else:
            if diagonally_adjacent is False:
                return True,'diagonal'
        return False,'okay'

class ShapeArea(tk.Frame):
    '''
    This class renders a 7x3 display of available shapes.
    '''

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="black")
        self.parent = parent
        self.name = 'shapearea'
        self.blocks = []
        j=0
        for row in range(7):
            for column in range(3):
                block = PlayArea(self, number_of_players=0,
                    colour_set=image_assets_10x10, pad=0)
                block.name = 'sub_shapearea'
                block.shape_number = j
                block.colour_squares('white',[[0]])
                block.configure(highlightthickness=2,
                    highlightbackground='gray')
                block.grid(row=row, column=column)
                self.blocks.append(block)
                j+=1
        self.selected_block = self.blocks[0]
        self.selected_block.configure(highlightbackground="yellow")

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
    This class renders a score area.
    '''

    def __init__(self, parent, players, eliminate_player):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = 'scorearea'
        self.players = players
        self.player_score_vars = []
        self.player_name_labels = []
        self.player_score_labels = []
        title = tk.Label(self, text="Scores:").grid(row=0, column=0)
        for i, p in enumerate(self.players._players):
            self.player_score_vars.append(tk.StringVar())
            self.player_name_labels.append(tk.Label(self, text=(p.name,"-")))
            self.player_score_labels.append(tk.Label(self,
                textvariable=self.player_score_vars[i]))
            self.player_name_labels[i].grid(row=i+1, column=1)
            self.player_score_labels[i].grid(row=i+1, column=2)
            self.player_score_vars[i].set(p.score)
        button = tk.Button(self, text="I'm out! :(",
            command=eliminate_player).grid(row=5, column=2)

    def update_score(self, players):
        for i, p in enumerate(players._players):
            self.player_score_vars[i].set(p.score)

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
