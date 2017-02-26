import Tkinter as tk
from shape import Shapes
from random import randint
from threading import Thread, Lock

class Board(tk.Frame):
    '''
    This class is the board view of the game.
    '''

    def __init__(self, parent, number_of_players=4):
        tk.Frame.__init__(self, parent, background="black")
        self.parent = parent
        self.name = 'board'
        if (number_of_players == 4):
            self.playarea=PlayArea(parent, rows=20, columns=20)
        elif (number_of_players == 2):
            self.playarea=PlayArea(parent, rows=14, columns=14)
        else:
            raise ValueError
            return None
        self.shapearea = ShapeArea(parent)
        self.lock = Lock()
        self.parent.bind("<Enter>", self.colour_shape_on_grid)
        self.parent.bind("<Leave>", self.colour_shape_on_grid)

    def background_tasks():
        num_enters = 0
        num_leaves = 0

    # the callback could execute faster..
    def colour_shape_on_grid(self, event):
        def callback(event):
            self.lock.acquire()
            try: grid_info = event.widget.grid_info()
            except AttributeError as e:
                self.lock.release()
                return None
            try: frame = grid_info['in']
            except KeyError as e:
                self.lock.release()
                return None
            if (frame.name == 'playarea'):
                for b in self.shapearea.blocks:
                    if b.selected is True:
                        shape_number=b.shape_number
                (r_offset,
                 c_offset) = self.playarea.get_grid_coordinates(event)
                if (int(event.type) == 7): # <Enter>
                    self.playarea.colour_squares('blue',
                        Shapes.shape_map[shape_number],
                        int(r_offset), int(c_offset))
                elif (int(event.type) == 8): # <Leave>
                    self.playarea.colour_squares('white',
                        Shapes.shape_map[shape_number],
                        int(r_offset), int(c_offset))
            self.lock.release()
        t = Thread(target=callback, args=(event,))
        t.start()

class PlayArea(tk.Frame):
    '''
    This class renders a 20x20 playing board and packs into a parent window.
    '''

    def __init__(self, parent, rows=20, columns=20, colour_set=Shapes.colours4,
        pad=1):
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
        parent.bind("<Button-1>", self.place_shape_on_grid)

    def colour_squares(self, colour, shape, r_offset, c_offset):
        photo = tk.PhotoImage(file=self.colour_set[colour])
        numrows = len(shape)
        numcols = len(shape[0])
        for row in range(numrows):
            for column in range(numcols):
                if (shape[row][column]):
                    try:
                        sqr = self.squares[row+r_offset][column+c_offset]
                        sqr.configure(image = photo)
                        sqr.photo = photo
                        sqr.grid(row=row+r_offset, column=column+c_offset)
                    except IndexError as e:
                        pass

    def clear_squares(self, shape=None):
        photo = tk.PhotoImage(file=self.colour_set['white'])
        if shape is None:
            numrows = 5
            numcols = 5
        else:
            numrows = len(shape)
            numcols = len(shape[0])
        for row in range(numrows):
            for column in range(numcols):
                sqr = self.squares[row][column]
                sqr.configure(image=photo)
                sqr.photo = photo
                sqr.grid(row=row, column=column)

    def get_grid_coordinates(self, event):
        try:
            grid_info = event.widget.grid_info()
            row = grid_info['row']
            column = grid_info['column']
            return (row, column)
        except (AttributeError, KeyError) as e:
            return None

    def place_shape_on_grid(self, event):
        (r_offset, c_offset) = self.playarea.get_grid_coordinates(event)


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
                    colour_set=Shapes.colours1, pad=0)
                block.name = 'sub_shapearea'
                block.selected = False
                block.shape_number = j
                block.colour_squares('blue', Shapes.shape_map[j], 0, 0)
                block.configure(highlightthickness=3)
                block.pack(side='left')
                self.blocks.append(block)
                j+=1
            self.sub_frames[row].pack(side='top')
        self.blocks[0].configure(highlightbackground="yellow")
        self.blocks[0].selected = True
        self.pack(side="bottom")
        parent.bind("<Button-1>", self.get_shape_from_frame)
        parent.bind("<Button-2>", self.rotate_shape_in_frame)
        parent.bind("<Button-3>", self.flip_shape_in_frame)

    def change_frame_selection(self, frame):
        for b in self.blocks:
            if b.selected is True:
                b.selected = False
                b.configure(highlightbackground="white")
            if b == frame:
                b.selected = True
                b.configure(highlightbackground="yellow")

    def get_shape_from_frame(self, event):
        try:
            grid_info = event.widget.grid_info()
            frame = grid_info['in']
        except (AttributeError, KeyError) as e:
            return None
        for b in self.blocks:
            if b == frame:
                self.change_frame_selection(frame)

    def rotate_shape_in_frame(self, event):
        blue_shapes = Shapes()
        try:
            grid_info = event.widget.grid_info()
            frame = grid_info['in']
        except (AttributeError, KeyError) as e:
            return None
        for b in self.blocks:
            if b == frame:
                self.change_frame_selection(frame)
                b.clear_squares(blue_shapes.shape_map[b.shape_number])
                blue_shapes.rotate_shape(b.shape_number)
                b.colour_squares('blue', blue_shapes.shape_map[b.shape_number],
                    0, 0)

    def flip_shape_in_frame(self, event):
        blue_shapes = Shapes()
        try:
            grid_info = event.widget.grid_info()
            frame = grid_info['in']
        except (AttributeError, KeyError) as e:
            return None
        for b in self.blocks:
            if b == frame:
                self.change_frame_selection(frame)
                b.clear_squares(blue_shapes.shape_map[b.shape_number])
                blue_shapes.flip_shape(b.shape_number)
                b.colour_squares('blue', blue_shapes.shape_map[b.shape_number],
                    0, 0)

class Square(tk.Label):
    '''
    This class is a single square in the grid.
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
