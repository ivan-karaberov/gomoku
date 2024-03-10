from ai import AI
from board import Board


class Game:
    def __init__(self, size: int, player_index: int):
        self.size = size
        self.finished = False
        self.ai = AI()
        self.restart(player_index)

    def restart(self, player_index: int = 1) -> None:
        self.board = Board(self.size)
        self.player_index = player_index
        self.ai_index = -player_index
        self.finished = False

    def aiplay(self) -> tuple[bool, int, int]:
        is_max = (self.player_index == -1)
        position = self.ai.get_move(self.board, self.ai_index, is_max)
        if self.play(position):
            return True, position
        return False, (0, 0)

    def play(self, position: tuple[int, int]) -> bool:
        if self.board.set_value(position):
            self.finished = self.board.is_terminal()
            return True
        return False

    def winner(self):
        return self.board.winner
