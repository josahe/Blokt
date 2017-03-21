from tkinter import Tk
from src.gui.board import Board
from src.backend.players import Players

def test_gui():
    # setup players
    players = Players()

    # setup board/gui
    window = Tk()
    window.resizable(width=False, height=False)
    window.wm_title("Blokt")
    board = Board(window, players)
    window.mainloop()
