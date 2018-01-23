import numpy as np
import tkinter as tk
from tkinter import messagebox
from .areas import PlayArea, ShapeArea, ScoreArea

class Board(tk.Frame):
    '''This class is the board view of the game.
    '''
    def __init__(self, parent, players):
        tk.Frame.__init__(self, parent, background="black")
        self.parent = parent
        self.name = 'board'
        self.players = players
        self.number_of_players = self.players.number_of_players
        self.playarea = PlayArea(parent, number_of_players=self.number_of_players)
        self.scorearea = ScoreArea(parent, self.players, self.eliminate_player)
        self.shapearea = ShapeArea(parent)
        self.shapearea.add_player_shapes(self.players.active_player.shapes)
        self.parent.bind("<Enter>", self.do_event_enter)
        self.parent.bind("<Leave>", self.do_event_leave)
        self.parent.bind("<Button-1>", self.do_event_click)
        self.parent.bind("<Button-2>", self.do_event_other)
        self.parent.bind("<Button-3>", self.do_event_other)
        self.parent.bind("<Key>", self.do_event_keypress)
        self.playarea.grid(row=0, column=0, rowspan=2)
        self.scorearea.grid(row=0, column=1, sticky='NW')
        self.shapearea.grid(row=1, column=1, sticky='S')
        self.current_grid_info = None
        self.previous_grid_info = None
        self.current_frame = None
        self.previous_frame = None
        self.previous_shape = None
        self.ones_5x5 = np.ones((5,5))

    def do_event_enter(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        self.current_grid_info, self.current_frame = grid_info, frame
        if frame is not None and frame.name == 'playarea':
            if self.previous_frame is not None:
                self.colour_shape_on_board(self.previous_grid_info, self.previous_frame, 'leave')
            self.colour_shape_on_board(grid_info, frame, 'enter')

    def do_event_leave(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            self.previous_grid_info, self.previous_frame = grid_info, frame
            self.previous_shape = self.players.active_player.shapes.active_shape

    def do_event_click(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            if self.rulebook(grid_info) == 'satisfied':
                self.playarea.place_shape_on_board(grid_info,
                    self.players.active_player.shapes)
                self.end_active_players_turn()
                if self.start_next_players_turn() is not True:
                    self.game_over()
        elif frame is not None and frame.name == 'sub_shapearea':
            if self.players.active_player.shapes.shape_map[frame.shape_number].used is False:
                self.shapearea.change_shape_with_frame(frame)
                self.players.active_player.shapes.update_active_shape(
                    self.shapearea.active_shape_index())

    def do_event_other(self, event, action=None):
        (grid_info, frame) = self.extract_from_event(event)
        if action is None:
            if event.num == 2:
                action = 'rotate right'
            elif event.num == 3:
                action = 'flip horizontal'
        else:
            grid_info, frame = self.current_grid_info, self.current_frame
        if frame is not None and frame.name == 'playarea':
            self.colour_shape_on_board(grid_info, frame, 'leave')
            self.shapearea.transform_shape(self.shapearea.selected_block,
                self.players.active_player.shapes, action)
            self.colour_shape_on_board(grid_info, frame, 'enter')
        elif frame is not None and frame.name == 'sub_shapearea':
            if self.players.active_player.shapes.shape_map[frame.shape_number].used is False:
                self.shapearea.change_shape_with_frame(frame)
                self.players.active_player.shapes.update_active_shape(
                    self.shapearea.active_shape_index())
                self.shapearea.transform_shape(frame,
                    self.players.active_player.shapes, action)
        else:
            self.shapearea.transform_shape(self.shapearea.selected_block,
                self.players.active_player.shapes, action)

    def do_event_keypress(self, event):
        # Movement keys
        if event.keysym == 'Up':
            pass # to be implemented
        elif event.keysym == 'Down':
            pass # to be implemented
        elif event.keysym == 'Left':
            pass # to be implemented
        elif event.keysym == 'Right':
            pass # to be implemented

        # Mutate shape keys
        elif event.char == 'h':
            self.do_event_other(event, 'flip horizontal')
        elif event.char == 'v':
            self.do_event_other(event, 'flip vertical')
        elif event.char == 'r':
            self.do_event_other(event, 'rotate right')
        elif event.char == 'l':
            self.do_event_other(event, 'rotate left')

        # Change shape keys
        elif event.char in ['n', 'p']:
            if event.char == 'n':
                action = 'next'
            else:
                action = 'previous'
            self.colour_shape_on_board(self.current_grid_info, self.current_frame, 'leave')
            self.shapearea.choose_shape_with_action(action)
            self.players.active_player.shapes.update_active_shape(action)
            self.colour_shape_on_board(self.current_grid_info, self.current_frame, 'enter')

    def extract_from_event(self, event):
        try:
            grid_info = event.widget.grid_info()
            frame = grid_info['in']
            name = frame.name
        except (AttributeError, KeyError) as e:
            return (None, None)
        return (grid_info, frame)

    def colour_shape_on_board(self, grid_info, frame, event_type):
        (r_offset, c_offset) = self.playarea.get_grid_coordinates(grid_info)
        if event_type == 'enter':
            self.playarea.colour_squares(
                self.players.active_player.shapes.colour,
                self.players.active_player.shapes.active_shape.matrix,
                r_offset, c_offset)
        else: # event_type == 'leave':
            self.playarea.clear_squares(self.ones_5x5, r_offset, c_offset)

    def rulebook(self, grid_info):
        (is_illegal,reason) = self.playarea.check_move(grid_info,
            self.players.active_player)
        if is_illegal is True:
            if reason == 'overlap':
                messagebox.showwarning(
                    title="Illegal move",
                    message="Your piece is overlapping with an existing piece",
                    parent=self.playarea
                )
            elif reason == 'adjacent':
                messagebox.showwarning(
                    title="Illegal move",
                    message="Your piece is adjacent to an existing piece",
                    parent=self.playarea
                )
            elif reason == 'index':
                messagebox.showwarning(
                    title="Illegal move",
                    message="Your piece is not within the boundary of the board",
                    parent=self.playarea
                )
            elif reason == 'diagonal':
                messagebox.showwarning(
                    title="Illegal move",
                    message="Your piece is not diagonally connecting to an existing piece",
                    parent=self.playarea
                )
            elif reason == 'corner':
                messagebox.showwarning(
                    title="Illegal move",
                    message="Your first piece must begin on a starting square",
                    parent=self.playarea
                )
            return 'broken'
        return 'satisfied'

    def end_active_players_turn(self):
        self.players.end_turn()
        self.shapearea.remove_player_shapes(self.players.active_player.shapes)
        self.scorearea.update_score(self.players)

    def start_next_players_turn(self):
        if self.players.start_turn() is True:
            self.shapearea.add_player_shapes(self.players.active_player.shapes)
            self.shapearea.change_shape_with_frame(
                self.shapearea.blocks[self.players.active_player.shapes.active_shape_index])
            return True
        return False

    def eliminate_player(self):
        self.shapearea.remove_player_shapes(self.players.active_player.shapes)
        self.players.active_player.eliminate()
        if self.start_next_players_turn() is False:
            self.game_over()

    def game_over(self):
        scores = [p.score for p in self.players._players]
        if len([i for i, x in enumerate(scores) if x == max(scores)]) > 1:
            winner = "It's a draw!"
        else:
            winner = "The winner is {0}".format(self.players._players[scores.index(max(scores))].name)
        messagebox.showinfo("Game over", winner, parent=self.playarea)

        # close app / start new game
        self.parent.quit()
