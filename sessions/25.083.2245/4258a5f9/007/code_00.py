"""
1.  **Initialization:** Start with the output grid as a copy of the input grid.

2.  **Locate and Create:** Find all gray pixels (value 5) in the *input* grid. For each gray pixel:
    *   Create a 3x3 block of blue pixels (value 1) in the *output* grid, centered on the location of the gray pixel.

3.  **Preserve Gray:** Ensure all pixels that were originally gray (value 5) in the input, remain gray in the output.

4.  **Conditional Expansion:** Iterate through the *neighbors* of each gray pixel in the *input* grid.
    *  If a neighbor in the input grid is white (value 0), then change the color of corresponding cell in the *output* to blue (value of 1).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the 8 neighbors of a pixel (Moore neighborhood).
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Locate and Create 3x3 Blue Blocks
    gray_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                gray_pixels.append((r, c))
                for i in range(max(0, r - 1), min(rows, r + 2)):
                    for j in range(max(0, c - 1), min(cols, c + 2)):
                        output_grid[i, j] = 1

    # 3. Preserve Gray Pixels
    for r, c in gray_pixels:
        output_grid[r,c] = 5 # Set back to gray

    # 4. Conditional Expansion
    for r, c in gray_pixels:
        for nr, nc in get_neighbors(input_grid, r, c):  # Check neighbors of the original gray pixel
            if input_grid[nr, nc] == 0:  # If the neighbor in input is white
                output_grid[nr, nc] = 1  # Expand to the corresponding cell in output

    return output_grid.tolist()