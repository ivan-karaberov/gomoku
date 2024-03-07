import tkinter as tk

import config

class GUI:
    def __init__(self, title: str, board_size: int, window_size: int):
        self.title = title
        self.board_size = board_size
        self.window_size = window_size
        self.cell_size = self.window_size / self.board_size
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
        print(event)
