import numpy as np

import config

class AI:
    def __init__(self):
        pass

    def get_move(self, board) -> tuple[int, int]:
        values = board.values

        if len(values[values != config.EMPTY]) == 0:
            return self.first_move(board)

        return (0, 0) # Only for test

    def first_move(self, board):
        x = board.size // 2
        return np.random.choice((x-1, x, x+1), 2)