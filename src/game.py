from board import Board

class Game:
    def __init__(self, size, player_index):
        self.size = size
        self.now_move = player_index
        self.finished = False
        self.restart(player_index)

    def restart(self, player_index=1):
        self.board = Board(self.size)
        self.ai_color = player_index * -1
        self.finished = False

    def play(self):
        pass

    def aiplay(self):
        pass

    def change_move_player(self):
        self.now_move *= -1