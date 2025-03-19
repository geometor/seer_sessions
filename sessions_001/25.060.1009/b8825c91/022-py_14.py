"""
The transformation rule is as follows:
1. Iterate through each pixel of the input grid.
2. If a pixel's color is yellow (4):
   - Check its adjacent pixels (horizontally, vertically, and diagonally).
   - If the surrounding pixels have the color 1(blue), change the yellow pixel to 5(grey).
   - Otherwise keep the yellow pixels to be itself.
3. If a pixel's color is green (3), change it to black(0)
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the adjacent pixels, including diagonals."""
    rows, cols = grid.shape
    adjacent = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                adjacent.append(grid[i, j])
    return adjacent

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for i in range(rows):
        for j in range(cols):
            # Rule for yellow (4) pixels
            if input_grid[i, j] == 4:
                adjacent = get_adjacent_pixels(input_grid, i, j)
                
                #check if adjacent pixels include other color, then change to grey(5)
                change = True
                for neighbor in adjacent:
                  if neighbor != 4 and neighbor != 1:
                    change = False
                    break
                
                if change:
                  output_grid[i,j] = 5

            # Rule for green(3) pixels
            if input_grid[i,j] == 3:
                output_grid[i,j] = 0

    return output_grid