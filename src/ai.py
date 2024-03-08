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

    def evaluation(self, values, current_color):
        return self.evaluate_color(values, config.WHITE, current_color) - \
            self.evaluate_color(values, config.BLACK, current_color)

    def evaluate_color(self, values, color, current_color):
        size = len(values)
        evaluation = 0
        is_current = (color == current_color)

        for i in range(size):
            evaluation += self.evaluate_line(values[i, :], color, is_current)
            evaluation += self.evaluate_line(values[:, i], color, is_current)

        for i in range(-size+config.LINE_FOR_WIN, size-(config.LINE_FOR_WIN-1)):
            evaluation += self.evaluate_line(
                np.diag(values, k=i), 
                color,
                is_current
            )
            evaluation += self.evaluate_line(
                np.diag(np.fliplr(values), k=i),
                color,
                is_current
            )

        return evaluation

    def evaluate_line(self, line, color, is_current):
        filled = 0
        empty = 0
        
        evaluation = 0
        for cell in line:
            if cell == color:
                filled += 1
            elif cell == config.EMPTY: 
                empty += 1
            else: 
                evaluation += self.check_pattern(filled, empty, is_current)
                filled = 0
                empty = 0

        evaluation += self.check_pattern(filled, empty, is_current)

        return evaluation
    
    def check_pattern(self, filled, empty, is_current):
        if filled < 0 or filled+empty < 5: 
            return 0
        
        if filled >= 5:
            return 100000
        
        filled_score = (2, 5, 1000, 10000)
        empty_score = (1, 1.2, 0.9, 0.4)
        
        value = filled_score[filled-1]
        value *= empty_score[empty-1 if empty < 4 else 3]
        value *= 1.1 if is_current else 1

        return int(value)

    def minimax(self):
        pass

    def first_move(self, board):
        x = board.size // 2
        return np.random.choice((x-1, x, x+1), 2)