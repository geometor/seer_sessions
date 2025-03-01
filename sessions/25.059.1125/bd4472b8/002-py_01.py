"""
Copies the first two rows of the input grid to the output grid. Then, it repeats the colors from the first row of the input grid vertically downwards, creating stripes, until the output grid is filled to a height derived from the original. The second row is all 5s (grey).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Copy the first two rows
    output_grid = input_grid[:2].copy()

    # build color sequence from the first row
    color_sequence = input_grid[0:1]

    # stack sequence until longer than input size
    while len(output_grid) < rows*2:
        output_grid = np.vstack([output_grid, color_sequence])
    
    # remove extra rows if any.
    output_grid = output_grid[:rows*2-2]
    

    return output_grid.tolist()