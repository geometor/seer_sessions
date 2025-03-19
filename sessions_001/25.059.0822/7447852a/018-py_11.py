"""
1.  **Identify White and Red Pixels:** Locate all pixels that are white (value 0) and red (value 2).
2.  **Horizontal Scan:** Iterate through each row of the grid.
3.  **Horizontal Betweenness:** If a white pixel is found, check if it has a red pixel immediately to its left AND a red pixel immediately to its right. If so, change the white pixel to yellow (value 4).
4.  **Vertical Scan:** Iterate through each column of the grid.
5.  **Vertical Betweenness:** If a white pixel is found, check if it has a red pixel immediately above it AND a red pixel immediately below it. If so, change the white pixel to yellow (value 4).
6. **Diagonal Scan:** Iterate through all possible diagonals (both top-left to bottom-right and top-right to bottom-left)
7.  **Diagonal Betweenness:** If a white pixel is found, check if it has red pixels immediately diagonally adjacent, if so, change the white pixel to yellow (value 4).
"""

import numpy as np

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

    # Vertical Scan and Color Change
    for j in range(cols):  # Iterate through columns
        for i in range(rows):
            if output_grid[i][j] == 0: #white
                if i > 0 and i < rows -1:
                    if output_grid[i-1][j] == 2 and output_grid[i+1][j] == 2:
                        output_grid[i][j] = 4

    # Diagonal Scan (Top-left to bottom-right)
    for i in range(rows):
        for j in range(cols):
            if output_grid[i][j] == 0:
                if i > 0 and i < rows - 1 and j > 0 and j < cols - 1:
                    if output_grid[i-1][j-1] == 2 and output_grid[i+1][j+1] == 2:
                        output_grid[i][j] = 4


    # Diagonal Scan (Top-right to bottom-left)
    for i in range(rows):
        for j in range(cols):
            if output_grid[i][j] == 0:
                if i > 0 and i < rows-1 and j > 0 and j < cols -1:
                    if output_grid[i-1][j+1] == 2 and output_grid[i+1][j-1] == 2:
                        output_grid[i][j] = 4

    return output_grid