"""
The input grid is duplicated and placed side-by-side. Then, additional rows are appended to the bottom, 
mirroring the color sequence of the columns in the original grid, to form a 10x10 output grid. The color sequence
cycles through the colors of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid.
    input_grid = np.array(input_grid)
    duplicated_grid = np.copy(input_grid)

    # Combine the original and duplicated grids horizontally.
    output_grid = np.concatenate((input_grid, duplicated_grid), axis=1)

    # Get original input_grid size
    in_rows, in_cols = input_grid.shape

    # Get the sequence of colors
    color_sequence = input_grid.flatten()

    # Append rows cyclically
    while output_grid.shape[0] < 10:
      next_row_index = (output_grid.shape[0] - in_rows) % len(color_sequence)
      next_row = np.array([color_sequence[next_row_index]] * (in_cols * 2))
      output_grid = np.concatenate((output_grid, [next_row]), axis=0)
    
    # Crop to 10x10
    output_grid = output_grid[:10, :10]

    return output_grid.tolist()