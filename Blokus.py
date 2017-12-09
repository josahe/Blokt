import sys, getopt
from tkinter import Tk
from src.gui.board import Board
from src.backend.players import Players

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"","two-player")
    except getopt.GetoptError:
        sys.exit(2)
    number_of_players = 4
    for opt, arg in opts:
        if opt in ("--two-player"):
            number_of_players = 2
    window = Tk()
    window.resizable(width=False, height=False)
    window.wm_title("Blokt")
    board = Board(window, Players(number_of_players=number_of_players))
    window.mainloop()

if __name__ == "__main__":
    main(sys.argv[1:])
