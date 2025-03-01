"""
Finds all non-zero pixels in the input grid. Rearranges them in a new grid
based on the number of non-zero pixels: one pixel at [0,0], two pixels
diagonally, more than two vertically in the first column. Trims the output
grid to the minimum size.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds the coordinates and values of all non-zero pixels in a grid.

    Args:
        grid: A 2D numpy array.

    Returns:
        A list of tuples: (row, column, value).
    """
    nonzero_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_pixels.append((r, c, grid[r, c]))
    return nonzero_pixels

def trim_grid(grid):
    """
    Removes empty rows and columns from the edges of a grid.

    Args:
        grid: A 2D numpy array

    Returns: A 2D numpy array
    """
    #find dimensions needed
    max_row = -1
    max_col = -1

    for r in range(grid.shape[0]):
      for c in range(grid.shape[1]):
        if grid[r,c] != 0:
          if r > max_row:
            max_row = r
          if c > max_col:
            max_col = c

    if max_row == -1:
        return np.array([[]])
    else:
        return grid[:max_row+1,:max_col+1] #trim
    

def transform(input_grid):
    """
    Transforms the input grid based on the described rules.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # 1. Identify and count non-zero pixels.
    nonzero_pixels = get_nonzero_pixels(input_grid)
    num_nonzero = len(nonzero_pixels)

    # 2. Create output grid (initially large enough).
    output_grid = np.zeros((num_nonzero, num_nonzero if num_nonzero > 1 else 1), dtype=int)

    # 3. Arrange pixels based on count.
    if num_nonzero == 1:
        output_grid[0, 0] = nonzero_pixels[0][2]
    elif num_nonzero == 2:
        output_grid[0, 0] = nonzero_pixels[0][2]
        output_grid[1, 1] = nonzero_pixels[1][2]
    else:
        for i, (_, _, value) in enumerate(nonzero_pixels):
            output_grid[i, 0] = value

    # 4. Trim the output grid.
    trimmed_grid = trim_grid(output_grid)

    return trimmed_grid