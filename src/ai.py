import numpy as np

import config
#from board import Board

class AI:
    def __init__(self, depth=2):
        self.depth = depth

    def get_move(self, board, current_color, is_max) -> tuple[int, int]:
        values = board.values

        moves_count = len(values[values != config.EMPTY])
        if moves_count == 0:
            return self.first_move(board)
        elif moves_count == 1:
            return self.second_move(board)

        best_value = is_max and -9999 or 9999
        best_move = (-1, -1)

        possible_moves = self.get_possible_moves(board, current_color, 10, is_max)
        
        for move in possible_moves:
            move = move[0]
            value = self.minimax(
                board.next(move), 
                -10e5, 
                10e5, 
                self.depth-1, 
                not is_max,
            )

            if ((is_max and value > best_value) or (not is_max and value < best_value)):
                best_value = value
                best_move = move

        if best_move[0] == -1 and best_move[1] == -1:
            return possible_moves[0][0]

        return best_move

    def get_possible_moves(self, board, color, n: int, is_max: bool):
        possible_moves = []
        preferred_moves = board.preferred_moves()
        for move in preferred_moves:
            emulated_move = board.next(move)
            evaluation = self.evaluation(emulated_move, color)
            possible_moves.append((move, evaluation))
        return sorted(possible_moves, key=lambda x: x[1], reverse=is_max)[:n]

    def evaluation(self, values, current_color):
        return self.evaluate_color(values, config.WHITE, current_color) +\
            self.evaluate_color(values, config.BLACK, current_color)

    def evaluate_color(self, board, color, current_color):
        size = board.size
        evaluation = 0
        is_current = (color == current_color)

        for i in range(size):
            evaluation += self.evaluate_line(board.values[i, :], color, is_current)
            evaluation += self.evaluate_line(board.values[:, i], color, is_current)

        for i in range(-size+config.LINE_FOR_WIN, size-(config.LINE_FOR_WIN-1)):
            evaluation += self.evaluate_line(
                np.diag(board.values, k=i), 
                color,
                is_current
            )
            evaluation += self.evaluate_line(
                np.diag(np.fliplr(board.values), k=i),
                color,
                is_current
            )

        return evaluation * color

    def evaluate_line(self, line, color, current):
        evaluation = 0
        size = len(line)
        # consecutive
        consec = 0
        block_count = 2
        empty = False

        for i in range(len(line)):
            value = line[i]
            if value == color:
                consec += 1

            elif value == config.EMPTY and consec > 0:
                if not empty and i < size - 1 and line[i + 1] == color:
                    empty = True
                else:
                    evaluation += self.calc(consec, block_count - 1, current, empty)
                    consec = 0
                    block_count = 1
                    empty = False

            elif value == config.EMPTY:
                block_count = 1

            elif consec > 0:
                evaluation += self.calc(consec, block_count, current)
                consec = 0
                block_count = 2
                
            else:
                block_count = 2

        if consec > 0:
            evaluation += self.calc(consec, block_count, current)

        return evaluation


    def calc(self, consec, block_count, is_current, has_empty_space=False):
        if block_count == 2 and consec < 5:
            return 0

        if consec >= 5:
            if has_empty_space:
                return 8000
            return 100000

        consec_score = (2, 5, 1000, 10000)
        # 3: 0.05
        block_count_score = (0.5, 0.6, 0.01, 0.25)
        not_current_score = (1, 1, 0.2, 0.15)
        empty_space_score = (1, 1.2, 0.9, 0.4)

        consec_idx = consec - 1
        value = consec_score[consec_idx]
        if block_count == 1:
            value *= block_count_score[consec_idx]
        if not is_current:
            value *= not_current_score[consec_idx]
        if has_empty_space:
            value *= empty_space_score[consec_idx]
        return int(value)


    def minimax(self, board, alpha, beta, depth, is_max):
        if depth == 0 or board.is_terminal():
            return self.evaluation(board, -board.color)

        preferred_moves = board.preferred_moves()
        if is_max:
            value = -9999
            for move in preferred_moves:
                value = max(
                    value, 
                    self.minimax(
                        board=board.next(move), 
                        alpha=alpha,
                        beta=beta,
                        depth=depth-1,
                        is_max=False,
                    )
                )
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            return value
        else:
            value = 9999
            for move in preferred_moves:
                value = min(
                    value, 
                    self.minimax(
                        board=board.next(move), 
                        alpha=alpha,
                        beta=beta,
                        depth=depth-1,
                        is_max=True,
                    )
                )
                beta = min(value, alpha)
                if alpha >= beta:
                    break
            return value

    def first_move(self, board):
        x = board.size // 2
        return np.random.choice((x-1, x, x+1), 2)

    def second_move(self, board):
        i, j = board.last_move
        size = board.size
        i2 = i <= size // 2 and 1 or -1
        j2 = j <= size // 2 and 1 or -1
        return i + i2, j + j2