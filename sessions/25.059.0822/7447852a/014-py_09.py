"""
1.  **Identify Red Pixels:** Locate all pixels with the color red (value 2).
2.  **Horizontal Scan:** For each row, iterate through the pixels from left to right.
3.  **Conditional Color Change:**
    *   If a white pixel (0) is encountered and is horizontally between two red pixels, change its color to yellow.
    *   If a red pixel is encountered and if is horizontally between white and yellow or yellow and white, change its color to yellow.
4. **Vertical Scan** For each column, iterate through the pixels from top to bottom.
5. **Conditional Color Change:**
        *    If a white pixel is encountered and is vertically between two red pixels change its color to yellow.
        *    If a red pixel is encountered and if is vertically between white and yellow or yellow and white, change its color to yellow.
6. The locations of the yellow pixels in relation to the red suggests the transformation rule may be related to identifying the white pixels surrounded on two sides by the red pixels.
"""

import numpy as np

def get_adjacent(grid, row, col, max_row, max_col):
     # Get adjacent cells, including diagonals
    adjacent_cells = []

    for i in range(max(0, row - 1), min(max_row, row + 2)):
        for j in range(max(0, col - 1), min(max_col, col + 2)):
            if (i, j) != (row, col):
                adjacent_cells.append((i, j, grid[i][j]))
    return adjacent_cells

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Horizontal Scan and Color Change
    for i in range(rows):
        for j in range(cols):
            if output_grid[i][j] == 0:  # White pixel
                if j > 0 and j < cols - 1:
                    if output_grid[i][j-1] == 2 and output_grid[i][j+1] == 2:
                        output_grid[i][j] = 4
            if output_grid[i][j] == 2: # red pixel
                if j > 0 and j < cols -1:
                    if (output_grid[i][j-1] == 0 and output_grid[i][j+1] == 4) or (output_grid[i][j-1] == 4 and output_grid[i][j+1] == 0):
                         output_grid[i][j] = 4
    # Vertical Scan and Color Change
    for j in range(cols):  # Iterate through columns
        for i in range(rows):
            if output_grid[i][j] == 0: #white
                if i > 0 and i < rows -1:
                    if output_grid[i-1][j] == 2 and output_grid[i+1][j] == 2:
                        output_grid[i][j] = 4
            if output_grid[i][j] == 2: # red
                if i > 0 and i < rows - 1:
                     if (output_grid[i-1][j] == 0 and output_grid[i+1][j] == 4) or (output_grid[i-1][j] == 4 and output_grid[i+1][j] == 0):
                        output_grid[i][j] = 4

    return output_grid