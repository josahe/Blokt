from Tkinter import *
from src.gui.board import Grid, Score

def test_gui():
    window=Tk()
    window.resizable(width=False,height=False)
    window.wm_title("Get Blokt")

    board_4player=Grid(window,rows=20,columns=20)
    #board_2player=Board(window,rows=14,columns=14)

    #board.pack(side="top",fill="x")
    board_4player.pack()

    score_area=Score(window)
    score_area.pack()

    window.mainloop()
