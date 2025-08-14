import tkinter as tk
from sudoku_board import SudokuGame

def main(game):
    # Main function of Sudoku game
    sudoku = tk.Label(root, text="Sudoku", font=("Arial", 6 * 3))
    sudoku.pack(pady= 10)
    top_frame = tk.Frame(root)
    bottom_frame = tk.Frame(root)
    top_frame.pack(side="top", pady=15, anchor="center")
    bottom_frame.pack(side="bottom", padx=15, pady=(0, 25), anchor="center")
    game.top_frame = top_frame
    game.bottom_frame = bottom_frame
    game.create_grid(top_frame) # Show Sudoku grid
    game.create_progress_bar(bottom_frame) # Show progress bar
    game.show_game_buttons(bottom_frame) # Show buttons  

if __name__ == "__main__":
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.resizable(False, False)
    root.title("SudokuGame")
    game = SudokuGame(root)
    main(game)
    root.mainloop()
