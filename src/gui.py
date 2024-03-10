import tkinter as tk
import tkinter.messagebox as tk_mb

import config
from game import Game
from exceptions import CellNotExists


class GUI:
    def __init__(self, title: str, board_size: int, window_size: int):
        self.game = Game(board_size, player_index=config.PLAYER_COLOR)
        self.board_size = board_size
        self.cell_size = window_size / board_size
        self.player_color = self.assign_color(self.game.player_index)
        self.ai_color = self.assign_color(self.game.ai_index)

        self.root = tk.Tk()
        self.root.title(title)
        self.canvas = tk.Canvas(
            self.root,
            width=window_size,
            height=window_size,
            bg=config.WINDOWS_COLOR_DEFAULT
        )
        self.canvas.pack()
        self.draw_board()

        if self.game.ai_index == config.WHITE:
            self.set_ai()

        self.root.mainloop()

    def draw_board(self):
        ''' Fills the window with cells with the default color '''
        for i in range(self.board_size):
            x = i * self.cell_size
            for j in range(self.board_size):
                y = j * self.cell_size
                self.canvas.create_rectangle(
                    y, x, y+self.cell_size, x+self.cell_size,
                    fill=config.CELL_COLOR_DEFAULT,
                    activefill=config.CELL_HOVER_COLOR
                )
                self.canvas.bind("<Button-1>", self.click)

    def click(self, event):
        '''Cell click event handler '''
        if self.set_player(event):
            self.set_ai()
        if self.game.finished:
            self.show_menu()

    def set_player(self, event):
        ''' User's move '''
        cell_id = self.canvas.find_closest(event.x, event.y)[0]
        position = self.convert_cell_id(cell_id)
        if self.game.play(position):
            self.set_color(position[0], position[1], self.player_color)
            return True
        return False

    def set_ai(self):
        ''' Ai move '''
        status, position = self.game.aiplay()
        if status:
            row, col = position
            self.set_color(row, col, self.ai_color)

    def show_menu(self):
        ''' Menu in terminal game state '''
        if self.game.winner() is not None:
            title = f"Win player {self.game.winner()} "
        else:
            title = "Draw! "
        menu = tk_mb.askyesno(
            title="Game over",
            message=title+"Want to play again?"
        )
        if menu:
            self.restart_game()
        else:
            exit()

    def restart_game(self):
        self.game.restart(config.PLAYER_COLOR)
        self.reload_cells()
        if self.game.ai_index == config.WHITE:
            self.set_ai()

    def reload_cells(self):
        ''' Set all cells to default color '''
        self.player_color = self.assign_color(self.game.player_index)
        self.ai_color = self.assign_color(self.game.ai_index)
        for cell_id in range((self.board_size**2)+1):
            self.canvas.itemconfig(
                cell_id,
                fill=config.CELL_COLOR_DEFAULT,
                activefill=config.CELL_HOVER_COLOR
            )

    def set_color(self, row: int, col: int, color: str):
        ''' Filling a selected cell with color '''
        cell_id = self.convert_to_cell_id(row, col)
        self.canvas.itemconfig(cell_id, fill=color, activefill=color)

    def convert_to_cell_id(self, row: int, col: int) -> int:
        ''' Convert x, y to cell id'''
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            raise CellNotExists
        return row*self.board_size + col + 1

    def convert_cell_id(self, cell_id: int) -> tuple[int, int]:
        ''' Convert cell id to x, y'''
        if not 1 <= cell_id <= self.board_size**2:
            raise CellNotExists
        row = (cell_id - 1) // self.board_size
        col = (cell_id - 1) % self.board_size
        return row, col

    def assign_color(self, player_index: int):
        ''' Matching color to index '''
        if player_index == config.WHITE:
            return config.WHITE_COLOR
        if player_index == config.BLACK:
            return config.BLACK_COLOR
        return None
