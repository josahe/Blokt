import tkinter as tk
from tkinter import messagebox
from .areas import PlayArea, ShapeArea, ScoreArea

class Board(tk.Frame):
    '''
    This class is the board view of the game.
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
        self.shapearea.add_player_shapes(self.players.current_player.shapes)
        self.parent.bind("<Enter>", self.do_event_enter)
        self.parent.bind("<Leave>", self.do_event_leave)
        self.parent.bind("<Button-1>", self.do_event_button_1)
        self.parent.bind("<Button-2>", self.do_event_button_2)
        self.parent.bind("<Button-3>", self.do_event_button_3)
        self.playarea.grid(row=0, column=0, rowspan=2)
        self.scorearea.grid(row=0, column=1, sticky='NW')
        self.shapearea.grid(row=1, column=1, sticky='S')
        self.previous_grid_info = None
        self.previous_frame = None
        self.previous_shape = None

    def do_event_enter(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            if self.previous_frame is not None:
                self.colour_shape_on_board(self.previous_grid_info, self.previous_frame, 'leave')
            self.colour_shape_on_board(grid_info, frame, 'enter')

    def do_event_leave(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            self.previous_grid_info, self.previous_frame = grid_info, frame
            self.previous_shape = self.players.current_player.shapes.current_shape

    def do_event_button_1(self, event):
        (grid_info, frame) = self.extract_from_event(event)
        if frame is not None and frame.name == 'playarea':
            if self.rulebook(grid_info) == 'satisfied':
                self.playarea.place_shape_on_board(grid_info,
                    self.players.current_player.shapes)
                self.end_current_players_turn()
                if self.start_next_players_turn() is not True:
                    self.game_over()
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
            name = frame.name
        except (AttributeError, KeyError) as e:
            return (None, None)
        return (grid_info, frame)

    def colour_shape_on_board(self, grid_info, frame, event_type):
        shape_number = self.shapearea.selected_block.shape_number
        (r_offset, c_offset) = self.playarea.get_grid_coordinates(grid_info)
        if event_type == 'enter':
            self.playarea.colour_squares(
                self.players.current_player.shapes.colour,
                self.players.current_player.shapes.current_shape.matrix,
                r_offset, c_offset)
        else: # event_type == 'leave':
            self.playarea.clear_squares(
                self.previous_shape.matrix,
                r_offset, c_offset)

    def rulebook(self, grid_info):
        (is_illegal,reason) = self.playarea.check_move(grid_info,
            self.players.current_player)
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
                    message="Your piece is not laying within the boundary of the board",
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
                    message="Your first piece must connect to a starting square",
                    parent=self.playarea
                )
            return 'broken'
        return 'satisfied'

    def end_current_players_turn(self):
        self.players.end_turn()
        self.shapearea.remove_player_shapes(self.players.current_player.shapes)
        self.scorearea.update_score(self.players)

    def start_next_players_turn(self):
        if self.players.start_turn() is True:
            self.shapearea.add_player_shapes(self.players.current_player.shapes)
            self.shapearea.change_frame_selection(
                self.shapearea.blocks[self.players.current_player.shapes.current_shape_index])
            return True
        return False

    def eliminate_player(self):
        self.shapearea.remove_player_shapes(self.players.current_player.shapes)
        self.players.current_player.eliminate()
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
