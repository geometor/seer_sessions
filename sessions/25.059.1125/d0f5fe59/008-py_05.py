"""
The program extracts a diagonal sequence of azure pixels from the input. The size of the output grid and the number of azure pixels placed on its diagonal are determined by the longest continuous diagonal of azure pixels in the input, up to a maximum size, and applies different rules if fewer than three such pixels are found or when input grid consists of only azure pixels.
"""

import numpy as np

def get_azure_diagonal(grid):
    """Finds the longest continuous diagonal of azure pixels."""
    azure_pixels = []
    max_len = 0
    for start_row in range(grid.shape[0]):
        for start_col in range(grid.shape[1]):
          if grid[start_row,start_col] == 8:
            current_len = 0
            current_row = start_row
            current_col = start_col
            temp_pixels = []
            while current_row < grid.shape[0] and current_col < grid.shape[1] and grid[current_row, current_col] == 8:
                temp_pixels.append((current_row, current_col))
                current_len += 1
                current_row += 1
                current_col += 1
            if current_len > max_len:
                max_len = current_len
                azure_pixels = temp_pixels
    return azure_pixels

def transform(input_grid):
    """Transforms the input grid to the output grid."""

    input_grid = np.array(input_grid)
    
    # find azure diagonal
    azure_diagonal = get_azure_diagonal(input_grid)
    
    # determine output size based on azure diagonal length or if input is all azure
    if np.all(input_grid == 8):
        output_grid = input_grid.copy()
        return output_grid

    output_size = len(azure_diagonal)

    if output_size >= 4:
      output_size = 4
    elif output_size == 3:
        output_size = 3
    elif output_size < 3:
        output_size = 2
    
    # initialize output_grid
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # fill output pixels on the diagonal with azure
    for i in range(min(output_size, len(azure_diagonal))):
            output_grid[i, i] = 8

    return output_grid