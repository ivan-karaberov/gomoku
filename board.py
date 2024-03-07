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
    
    def value(self, position) -> int | None:
        pass

    def is_valid_position(self, position) -> bool:
        pass
    
    def set_value(self, position, color) -> bool:
        pass