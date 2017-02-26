from Tkinter import Tk
from src.gui.board import Board

def test_gui():
    window=Tk()
    window.resizable(width=False,height=False)
    window.wm_title("Get Blokt")
    board=Board(window)
    window.mainloop()
