from board import Board

class Game:
    def __init__(self, size, player_index):
        self.size = size
        self.now_move = player_index
        self.finished = False
        self.restart(player_index)

    def restart(self, player_index=1) -> None:
        self.board = Board(self.size)
        self.ai_color = player_index * -1
        self.finished = False

    def play(self, row: int, col: int) -> bool:
        position = (row, col)
        
        if self.board.set_value(position, self.now_move):
            self.finished = self.board.is_terminal()
            self.change_move_player()
            return True

        return False

    def aiplay(self):
        move = self.ai.get_move()
        self.finished = self.board.is_terminal()
        return move

    def change_move_player(self):
        self.now_move *= -1