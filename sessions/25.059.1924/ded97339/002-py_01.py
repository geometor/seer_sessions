"""
Identify all azure pixels (value 8) in the input grid. Extend lines of azure pixels horizontally from each identified azure pixel, first to the left and then to the right, until a boundary (another azure pixel or the grid edge) is reached. Then, extend lines vertically from the original azure pixels and the horizontally extended ones, if necessary, to connect all azure pixels. The shape is formed only by horizontal and vertical lines; diagonal connections are not allowed.
"""

import numpy as np

def get_azure_pixels(grid):
    # Find coordinates of all azure pixels (value 8).
    return np.argwhere(grid == 8)

def extend_horizontally(grid, start_row, start_col):
    # Extend azure pixels horizontally to the left and right.
    
    # Extend to the left
    col = start_col - 1
    while col >= 0 and grid[start_row, col] != 8 :
        grid[start_row, col] = 8
        col -= 1

    # Extend to the right
    col = start_col + 1
    while col < grid.shape[1] and grid[start_row, col] != 8:
        grid[start_row, col] = 8
        col += 1
    return grid

def extend_vertically(grid, start_row, start_col):
    # Extend azure pixels vertically downwards
    row = start_row + 1
    while row < grid.shape[0]:
        if grid[row,start_col] == 8:
            break
        grid[row, start_col] = 8
        row += 1
    return grid

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Get coordinates of all azure pixels.
    azure_pixels = get_azure_pixels(output_grid)

    # first pass, extend horizontally
    for r, c in azure_pixels:
      output_grid = extend_horizontally(output_grid, r, c)

    # second pass, extend vertically
    azure_pixels = get_azure_pixels(output_grid)
    for r,c in azure_pixels:
        output_grid = extend_vertically(output_grid,r,c)
    
    return output_grid