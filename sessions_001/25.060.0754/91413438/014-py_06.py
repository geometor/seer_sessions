"""
1. Tile: Replicate the input 3x3 grid multiple times in a 3x3 pattern to conceptually create a 9x9 grid.
2. Fill last rows with 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_np = np.array(input_grid)
    output_np = np.tile(input_np, (3, 3))

    # set the bottom 3 rows to 0
    output_np[6:, :] = 0
    
    return output_np.tolist()