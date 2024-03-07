import tkinter as tk
import tkinter.messagebox as tk_mb

import config
from game import Game
from exceptions import CellNotExists

class GUI:
    def __init__(self, title: str, board_size: int, window_size: int):
        self.game = Game(board_size, player_index=1)
        self.title = title
        self.board_size = board_size
        self.window_size = window_size
        self.cell_size = self.window_size / self.board_size
        self.player_color = self.assign_color(self.game.player_index)
        self.ai_color = self.assign_color(self.game.ai_index)        
        self.display()

    def display(self):
        self.root = tk.Tk()
        self.root.title(self.title)
        self.canvas = tk.Canvas(
            self.root, 
            width=self.window_size,
            height=self.window_size,
            bg=config.WINDOWS_COLOR_DEFAULT   
        )
        self.canvas.pack()
        self.draw_board()
        if self.game.ai_index == config.WHITE:
            self.set_ai()

        self.root.mainloop()

    def draw_board(self):
        for i in range(self.board_size):
            x = i  * self.cell_size
            for j in range(self.board_size):
                y = j * self.cell_size
                self.canvas.create_rectangle(
                    y, x, y+self.cell_size, x+self.cell_size, 
                    fill=config.CELL_COLOR_DEFAULT, 
                    activefill=config.CELL_HOVER_COLOR
                )
                self.canvas.bind("<Button-1>", self.click)
    
    def click(self, event):
        self.set_player(event)
        self.set_ai()
        if self.game.finished:
            self.show_menu()

    def set_player(self, event):
        cell_id = self.canvas.find_closest(event.x, event.y)[0]
        row, col = self.convert_cell_id(cell_id)
        if self.game.play(row, col):
            self.set_color(row, col, self.player_color)

    def set_ai(self):
        status, position = self.game.aiplay()
        if status:
            row, col = position
            self.set_color(row, col, self.ai_color)

    def show_menu(self):
        if self.game.winner() is not None:
            title = f"Win player {self.game.winner()} "
        else:
            title = f"Draw "
        result = tk_mb.askyesno(title="Game over", message=title+"Want to play again?")
        if result: 
            self.game.restart()
            self.reload_cells()
        else: 
            exit()

    def reload_cells(self):
        for cell_id in range((self.board_size**2)+1):
            self.canvas.itemconfig(
                cell_id,
                fill=config.CELL_COLOR_DEFAULT,
                activefill=config.CELL_HOVER_COLOR
            )

    def set_color(self, row, col, color):
        cell_id = self.convert_to_cell_id(row, col)
        self.canvas.itemconfig(cell_id, fill=color, activefill=color)
    
    def convert_to_cell_id(self, row, col) -> int:
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            raise CellNotExists
        return row*self.board_size + col + 1
    
    def convert_cell_id(self, cell_id: int) -> tuple[int, int]:
        if not 1 <= cell_id <= self.board_size**2:
            raise CellNotExists
        row = (cell_id - 1) // self.board_size
        col = (cell_id - 1) % self.board_size
        return row, col

    def assign_color(self, player_index):
        if player_index == config.WHITE:
            return config.WHITE_COLOR
        if player_index == config.BLACK:
            return config.BLACK_COLOR
        return None