```python
"""
Copies white (0) pixels from the input grid to the output. Expands each gray
(5) pixel into a 3x3 square of blue (1) pixels in the output grid. If gray
pixels are diagonally adjacent in the input grid, they are also connected by
a single-pixel-wide blue (1) line in the output grid, which can extend beyond
the 3x3 expansions.
"""

import numpy as np

def get_gray_pixels(grid):
    # Find coordinates of all gray pixels (value 5).
    return np.argwhere(grid == 5)

def are_diagonally_adjacent(pixel1, pixel2):
    # Check if two pixels are diagonally adjacent.
    return abs(pixel1[0] - pixel2[0]) == abs(pixel1[1] - pixel2[1]) and not np.array_equal(pixel1,pixel2)

def expand_to_blue_square(grid, row, col):
    # Create a 3x3 blue square centered at (row, col).
    output_grid = np.copy(grid)
    for i in range(max(0, row - 1), min(grid.shape[0], row + 2)):
        for j in range(max(0, col - 1), min(grid.shape[1], col + 2)):
            output_grid[i, j] = 1
    return output_grid

def connect_with_blue_line(grid, pixel1, pixel2):
    # Connect two diagonally adjacent pixels with a single-pixel-wide blue line.
    output_grid = np.copy(grid)
    row1, col1 = pixel1
    row2, col2 = pixel2

    row_step = 1 if row2 > row1 else -1
    col_step = 1 if col2 > col1 else -1

    current_row, current_col = row1, col1
    while current_row != row2 + row_step or current_col != col2 + col_step:
      # only set to 1 if the current pixel is not part of the expansion
      if output_grid[current_row,current_col] != 1:
        output_grid[current_row, current_col] = 1
      current_row += row_step
      current_col += col_step

    return output_grid

def transform(input_grid):
    # Initialize output grid with the same values as input grid.
    output_grid = np.copy(input_grid)

    # Expand gray pixels to 3x3 blue squares.
    gray_pixels = get_gray_pixels(input_grid)
    for r, c in gray_pixels:
        output_grid = expand_to_blue_square(output_grid, r, c)
        
    # Connect diagonally adjacent gray pixels with blue lines AFTER expansion.
    for i in range(len(gray_pixels)):
        for j in range(i + 1, len(gray_pixels)):
            if are_diagonally_adjacent(gray_pixels[i], gray_pixels[j]):
                output_grid = connect_with_blue_line(output_grid, gray_pixels[i], gray_pixels[j])

    #change all remaining gray pixels to blue
    output_grid[output_grid == 5] = 1

    return output_grid
```