"""
1.  **Background:** Identify color 7 (orange) as the background. Pixels of this color remain unchanged.

2.  **Center Column:** Find the center column of the grid.
    *   If a pixel in the center column has a value of 3:
        *   If the pixel is above the center row, change it to 2 (red).
        *   If the pixel is below the center row, change it to 4 (yellow).
    * If a pixel in the center column has value of 9:
        * It is unchanged
    * If a pixel in the center colum has value of 4:
        * It is unchanged
    * If a pixel in the center column has value of 5:
        * It is unchanged
3. **Corners and edges**:
   * If the input pixel is on an edge (row = 0, row= max_row, col=0 or col=max_col)
   * Check surrounding (including diagonals) pixels in the input.
      * If any surrounding pixel is the background color, change the output
        pixel to the most common color (mode) among the non-background
        surrounding pixels of the input pixel.

4.  **Output:** Create the output grid by applying these transformations, ensuring the background (color 7) remains unchanged.
"""

import numpy as np
from scipy.stats import mode

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_row = rows // 2
    center_col = cols // 2

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            # Background remains unchanged
            if input_grid[r, c] == 7:
                continue

            # Center Column Transformations
            if c == center_col:
                if input_grid[r, c] == 3:
                    if r < center_row:
                        output_grid[r, c] = 2
                    elif r > center_row:
                        output_grid[r, c] = 4
                elif input_grid[r,c] in [4,5,9]:
                    output_grid[r,c] = input_grid[r,c]


            # Edge Transformations
            elif r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                neighbors = get_neighbors(input_grid, r, c)
                if 7 in neighbors:  # Check if any neighbor is background
                    non_background_neighbors = [val for val in neighbors if val != 7]
                    if non_background_neighbors:
                         output_grid[r,c] = mode(non_background_neighbors)[0]


    return output_grid