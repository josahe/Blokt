import tkinter as tk
from tkinter import messagebox
from .areas import PlayArea, ShapeArea
#from threading import Thread, Lock

class Board(tk.Frame):
    '''
    This class is the board view of the game.
    '''

    def __init__(self, parent, players, number_of_players=4):
        tk.Frame.__init__(self, parent, background="black")
        self.parent = parent
        self.name = 'board'
        self.players = players
        if (number_of_players == 4):
            self.playarea=PlayArea(parent, rows=20, columns=20)
        elif (number_of_players == 2):
            self.playarea=PlayArea(parent, rows=14, columns=14)
        else:
            raise ValueError
            return None
        self.shapearea = ShapeArea(parent)
        self.shapearea.add_player_shapes(self.players.current_player.shapes)
        #self.lock = Lock()
        self.parent.bind("<Enter>", self.do_event_enter)
        self.parent.bind("<Leave>", self.do_event_leave)
        self.parent.bind("<Button-1>", self.do_event_button_1)
        self.parent.bind("<Button-2>", self.do_event_button_2)
        self.parent.bind("<Button-3>", self.do_event_button_3)

    def do_event_enter(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            self.colour_shape_on_board(grid_info, frame, 'enter')

    def do_event_leave(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            self.colour_shape_on_board(grid_info, frame, 'leave')

    def do_event_button_1(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            if self.rule_is_broken(grid_info) is not True:
                self.playarea.place_shape_on_board(grid_info,
                    self.players.current_player.shapes)
                self.end_current_players_turn()
                self.start_next_players_turn()
        elif frame is not None and frame.name == 'sub_shapearea':
            if self.players.current_player.shapes.shape_map[frame.shape_number].used is False:
                self.shapearea.change_frame_selection(frame)
                self.players.current_player.shapes.update_current_shape(
                    self.shapearea.get_selected_shape_index())

    def do_event_button_2(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            self.colour_shape_on_board(grid_info, frame, 'leave')
            self.shapearea.transform_shape(self.shapearea.selected_block,
                self.players.current_player.shapes, 'rotate')
            self.colour_shape_on_board(grid_info, frame, 'enter')
        elif frame is not None and frame.name == 'sub_shapearea':
            if self.players.current_player.shapes.shape_map[frame.shape_number].used is False:
                self.shapearea.change_frame_selection(frame)
                self.players.current_player.shapes.update_current_shape(
                    self.shapearea.get_selected_shape_index())
                self.shapearea.transform_shape(frame,
                    self.players.current_player.shapes, 'rotate')

    def do_event_button_3(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            self.colour_shape_on_board(grid_info, frame, 'leave')
            self.shapearea.transform_shape(self.shapearea.selected_block,
                self.players.current_player.shapes, 'flip')
            self.colour_shape_on_board(grid_info, frame, 'enter')
        elif frame is not None and frame.name == 'sub_shapearea':
            if self.players.current_player.shapes.shape_map[frame.shape_number].used is False:
                self.shapearea.change_frame_selection(frame)
                self.players.current_player.shapes.update_current_shape(
                    self.shapearea.get_selected_shape_index())
                self.shapearea.transform_shape(frame,
                    self.players.current_player.shapes, 'flip')

    def extract_from_event(self, event):
        try:
            grid_info = event.widget.grid_info()
            frame = grid_info['in']
        except (AttributeError, KeyError) as e:
            return (None, None)
        return (grid_info, frame)

    def colour_shape_on_board(self, grid_info, frame, event_type):
        def callback(grid_info, frame, event_type):
            #self.lock.acquire()
            shape_number = self.shapearea.selected_block.shape_number
            (r_offset, c_offset) = self.playarea.get_grid_coordinates(grid_info)
            if event_type == 'enter':
                self.playarea.colour_squares(
                    self.players.current_player.shapes.colour,
                    self.players.current_player.shapes.current_shape.matrix,
                    r_offset, c_offset)
            else: # event_type == 'leave':
                self.playarea.clear_squares(
                    self.players.current_player.shapes.current_shape.matrix,
                    r_offset, c_offset)
            #self.lock.release()
        #t = Thread(target=callback, args=(grid_info, frame, event_type))
        #t.start()
        callback(grid_info, frame, event_type)

    # This rulebook needs the following added:
    #   + first go must be in a corner
    #   + subsequent goes must be diagonally connected
    def rule_is_broken(self, grid_info):
        (is_illegal,reason) = self.playarea.check_move(grid_info,
            self.players.current_player)
        if is_illegal is True:
            if reason == 'overlap':
                messagebox.showwarning(
                    "Illegal move",
                    "Make sure your piece does not overlap with an existing piece"
                )
            elif reason == 'adjacent':
                messagebox.showwarning(
                    "Illegal move",
                    "Make sure your piece is not adjacent to an existing piece"
                )
            elif reason == 'index':
                messagebox.showwarning(
                    "Illegal move",
                    "Make sure your piece lies within the boundary of the board"
                )
            elif reason == 'diagonal':
                messagebox.showwarning(
                    "Illegal move",
                    "Make sure your piece diagonally connects to an existing piece"
                )
            elif reason == 'corner':
                messagebox.showwarning(
                    "Illegal move",
                    "Make sure your first piece connects to a corner square"
                )
            return True
        return False

    def end_current_players_turn(self):
        self.players.end_turn()
        self.shapearea.remove_player_shapes(self.players.current_player.shapes)

    def start_next_players_turn(self):
        self.players.start_turn()
        self.shapearea.add_player_shapes(self.players.current_player.shapes)
        self.shapearea.change_frame_selection(
            self.shapearea.blocks[self.players.current_player.shapes.current_shape_index])
