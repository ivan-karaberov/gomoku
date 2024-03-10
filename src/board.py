import numpy as np

import config


class Board:
    def __init__(
        self,
        size: int,
        values: np.ndarray[np.ndarray[int]] | None = None,
        color: int = config.WHITE
    ):
        if (np.all(values != None)):
            self.values = np.copy(values)
        else:
            self.values = np.full((size, size), config.EMPTY)

        self.size = size
        self.last_move = None
        self.winner = None
        self.color = color

    def set_value(self, position: tuple[int, int]) -> bool:
        if self.value(position) == config.EMPTY:
            self.values[position] = self.color
            self.color = -self.color
            self.last_move = position
            return True
        return False

    def value(self, position: tuple[int, int]) -> int | None:
        return self.values[position] if self.is_valid_position(position) \
                                                                    else None

    def is_valid_position(self, position: tuple[int, int]) -> bool:
        i, j = position
        return 0 <= i < self.size and 0 <= j < self.size

    def is_terminal(self):
        is_win, _ = self.check_win()
        is_full = self.is_full()
        if is_win or is_full:
            return True
        return False

    def check_win(self) -> tuple[bool, int]:
        if self.winner:
            return True, self.winner

        pattern = np.full((config.LINE_FOR_WIN), 1)

        if self.check_pattern(pattern * config.WHITE):
            self.winner = config.WHITE
            return True, self.winner
        elif self.check_pattern(pattern * config.BLACK):
            self.winner = config.BLACK
            return True, self.winner

        return False, config.EMPTY

    def check_pattern(self, pattern: np.ndarray[int]) -> int:
        counter = 0
        lines = self.get_lines()
        for line in lines:
            if self.contains(line, pattern):
                counter += 1
        return counter

    def get_lines(self) -> list[np.ndarray]:
        lines = []
        for i in range(self.size):
            lines.append(self.values[i, :])
            lines.append(self.values[:, i])

        for i in range(-self.size+config.LINE_FOR_WIN,
                       self.size-(config.LINE_FOR_WIN-1)):
            lines.append(np.diag(self.values, k=i))
            lines.append(np.diag(np.fliplr(self.values), k=i))

        return lines

    def contains(self, line: np.ndarray[int], pattern: np.ndarray[int]):
        for i in range(line.size-(pattern.size-1)):
            sub_line = line[i:i+pattern.size]
            if np.array_equal(sub_line, pattern):
                return True
        return False

    def is_full(self):
        return not np.any(self.values == config.EMPTY)

    def preferred_moves(self) -> np.ndarray[np.ndarray[int, int]]:
        cell_status = self.expand_area(self.values != config.EMPTY)
        return np.column_stack(np.where(cell_status == True))

    def expand_area(self, cell_status: np.ndarray[np.ndarray[bool]]):
        area_status = cell_status.copy()
        for i in range(self.size):
            for j in range(self.size):
                if not cell_status[i, j]:
                    continue
                for direction in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    di, dj = direction
                    for side in (-1, 1):
                        ni = i + di * side
                        nj = j + dj * side
                        if self.is_valid_position((ni, nj)):
                            area_status[ni, nj] = True
        return np.bitwise_xor(area_status, cell_status)

    def next(self, position):
        board = Board(self.size, self.values, self.color)
        board.set_value(tuple(position))
        return board
