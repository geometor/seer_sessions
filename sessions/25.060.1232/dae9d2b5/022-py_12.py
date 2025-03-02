"""
Counts the number of non-white (non-zero) pixels in the input grid and creates
a 3x3 output grid. The output grid is filled with magenta (6) pixels
corresponding to the count of non-white pixels in the input, and the rest are
filled with white (0).
"""

import numpy as np

def transform(input_grid):
    # Count non-white pixels
    non_white_count = np.count_nonzero(input_grid)

    # Create output grid (3x3)
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill output grid with magenta (6) up to the counted number
    count = 0
    for i in range(3):
        for j in range(3):
            if count < non_white_count:
                output_grid[i, j] = 6
                count += 1
            else:
                break
        if count >= non_white_count:
            break
    
    return output_grid