from board import Board
import config

class Game:
    def __init__(self, size, player_index):
        self.size = size
        self.now_move = config.WHITE
        self.finished = False
        self.restart(player_index)

    def restart(self, player_index=1) -> None:
        self.board = Board(self.size)
        self.player_index = player_index
        self.ai_index = player_index * -1
        self.finished = False

    def play(self, row: int, col: int) -> bool:
        position = (row, col)
        
        if self.board.set_value(position, self.now_move):
            self.finished = self.board.is_terminal()
            self.change_move_player()
            return True

        return False

    def aiplay(self) -> tuple[bool, int, int]:
        row, col = self.ai.get_move()
        if self.play(row, col):
            return True, (row, col)
        return False, (0,0)

    def change_move_player(self):
        self.now_move *= -1
    
    def winner(self):
        return self.board.winner