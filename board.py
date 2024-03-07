import numpy as np

import config

class Board:
    def __init__(self, size: int, values: np.ndarray | None = None):
        if (np.all(values != None)):
            self.values = np.copy(values)
        else:
            self.values = np.full((size, size), config.EMPTY)

        self.size = size
        self.last_move = None
        self.winner = None
    
    def value(self, position: tuple[int, int]) -> int | None:
        return self.values[position] if self.is_valid_position(position) \
                                                                    else None

    def is_valid_position(self, position) -> bool:
        i, j = position
        return 0 <= i < self.size and 0 <= j < self.size
    
    def set_value(self, position, color) -> bool:
        pass