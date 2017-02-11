import Tkinter as tk
from shape import Shapes
from random import randint


class Grid(tk.Frame):
    '''
    This class renders a 20x20 playing board and packs into a parent window.
    '''

    colours = {'white'  : "assets/white_square_40x40.ppm",
               'red'    : "assets/red_square_40x40.ppm",
               'yellow' : "assets/yellow_square_40x40.ppm",
               'green'  : "assets/green_square_40x40.ppm",
               'blue'   : "assets/blue_square_40x40.ppm"}

    def __init__(self, parent, rows=20, columns=20):
        tk.Frame.__init__(self, parent, background="black")

        self.parent = parent
        self.frame = tk.Frame(parent, background="black")

        photo = tk.PhotoImage(file=Grid.colours['white'])

        parent.bind("<Button-1>", self.get_grid_coordinates)

        for row in range(rows):
            for column in range(columns):
                entry = tk.Label(self.frame, borderwidth=0, image=photo)
                entry.photo = photo
                entry.grid(row=row, column=column, sticky="NSEW",
                    padx=1, pady=1)

        self.frame.pack(side="left")

    def colour_squares(self, colour, shape, r_offset, c_offset):
        photo = tk.PhotoImage(file=Grid.colours[colour])
        numrows = len(shape)
        numcols = len(shape[0])

        for row in range(numrows):
            for column in range(numcols):
                if (shape[row][column]):
                    entry = tk.Label(self.frame, borderwidth=0, image=photo)
                    entry.photo = photo
                    entry.grid(row=row+r_offset, column=column+c_offset)

    def get_grid_coordinates(self, event):
        try:
            grid_info = event.widget.grid_info()
            row = grid_info['row']
            column = grid_info['column']
            return (row, column)
        except (AttributeError, KeyError) as e:
            return None


class Score(tk.Frame):
    '''
    This class renders a 20x20 playing board and packs into a parent window.
    '''

    colours = {'white'  : "assets/white_square_10x10.ppm",
               'red'    : "assets/red_square_10x10.ppm",
               'yellow' : "assets/yellow_square_10x10.ppm",
               'green'  : "assets/green_square_10x10.ppm",
               'blue'   : "assets/blue_square_10x10.ppm",
               'grey'   : "assets/grey_square_10x10.ppm"}

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="black")

        self.parent = parent
        self.frame = tk.Frame(parent, background="black", width=100, height=100)
        self.sub_frame_rows = []
        self.sub_frame_cols = [[],[],[],[],[],[]]

        photo = tk.PhotoImage(file=Score.colours['white'])

        parent.bind("<Button-1>", self.get_shape_from_frame)
        parent.bind("<Button-2>", self.rotate_shape_in_frame)
        parent.bind("<Button-3>", self.flip_shape_in_frame)

        for x in range(5):
            self.sub_frame_rows.append(tk.Frame(self.frame, background="black"))
            for y in range(5):
                self.sub_frame_cols[x].append(tk.Frame(self.sub_frame_rows[x],
                    background="gray40", borderwidth=1))
                for row in range(6):
                    for column in range(5):
                        entry = tk.Label(self.sub_frame_cols[x][y],
                            borderwidth=0, image=photo)
                        entry.photo = photo
                        entry.grid(row=row, column=column, sticky="NSEW")
                self.sub_frame_cols[x][y].pack(side='left')
            self.sub_frame_rows[x].pack(side='top')

        map_index = 1
        for x in range(5):
            for y in range(5):
                if map_index < 22:
                    self.colour_squares('blue', Shapes.shape_map[map_index], x, y)
                    map_index+=1

        self.frame.pack(side="bottom")

    def colour_squares(self, colour, shape, x, y):
        photo = tk.PhotoImage(file=Score.colours[colour])
        numrows = len(shape)
        numcols = len(shape[0])

        for row in range(numrows):
            for column in range(numcols):
                if (shape[row][column]):
                    entry = tk.Label(self.sub_frame_cols[x][y],
                        borderwidth=0, image=photo)
                    entry.photo = photo
                    entry.grid(row=row, column=column)

    def clear_squares(self, x, y):
        photo = tk.PhotoImage(file=Score.colours['white'])
        numrows = 5
        numcols = 5

        for row in range(numrows):
            for column in range(numcols):
                entry = tk.Label(self.sub_frame_cols[x][y],
                    borderwidth=0, image=photo)
                entry.photo = photo
                entry.grid(row=row, column=column)

    def get_shape_from_frame(self, event):
        try:
            grid_info = event.widget.grid_info()
        except (AttributeError) as e:
            return None
        frame = grid_info['in']
        for f in self.sub_frame_cols:
            for ff in f:
                if ff == frame:
                    print self.sub_frame_cols.index(f),f.index(ff)
                    return self.sub_frame_cols.index(f),f.index(ff)

    def rotate_shape_in_frame(self, event):
        blue_shapes = Shapes()
        try:
            grid_info = event.widget.grid_info()
        except (AttributeError) as e:
            pass
        frame = grid_info['in']
        map_index = 1
        x = 0
        for f in self.sub_frame_cols:
            y = 0
            for ff in f:
                if ff == frame and map_index < 22:
                    self.clear_squares(x, y)
                    blue_shapes.rotate_shape(map_index)
                    self.colour_squares('blue', blue_shapes.shape_map[map_index], x, y)
                map_index+=1
                y+=1
            x+=1

    def flip_shape_in_frame(self, event):
        blue_shapes = Shapes()
        try:
            grid_info = event.widget.grid_info()
        except (AttributeError) as e:
            pass
        frame = grid_info['in']
        map_index = 1
        x = 0
        for f in self.sub_frame_cols:
            y = 0
            for ff in f:
                if ff == frame and map_index < 22:
                    self.clear_squares(x, y)
                    blue_shapes.flip_shape(map_index)
                    self.colour_squares('blue', blue_shapes.shape_map[map_index], x, y)
                map_index+=1
                y+=1
            x+=1
