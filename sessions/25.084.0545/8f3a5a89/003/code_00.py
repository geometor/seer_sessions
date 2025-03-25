"""
1.  **Seed Identification:** Locate all pixels with color 6 (magenta).
2.  **Azure (8) Transformation:**
    *   An azure (8) pixel changes to orange (7) if it is adjacent to a magenta (6) pixel.
    *   An azure (8) pixel *also* changes to orange (7) if a blue (1) pixel is to its *left*. Note: The 1 must be directly to the left and on the same row. This condition holds *even without* an adjacent magenta.
3.  **Blue (1) Transformation:**
    *  A blue (1) pixel will change to an orange (7) pixel if a neighboring azure (8) pixel is transformed into an orange (7) pixel.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                neighbors.append((r, c))
    return neighbors

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid to apply the 8-to-7 transformation rules
    for row in range(rows):
        for col in range(cols):
            # Rule 1: 8 next to a 6 becomes 7
            if output_grid[row, col] == 8:
                neighbors = get_neighbors(input_grid, row, col)
                for r, c in neighbors:
                    if input_grid[r, c] == 6:
                        output_grid[row, col] = 7
                        break  # Apply only one rule per iteration

    for row in range(rows):
         for col in range(cols):
            # Rule 2: 8 to the right of a 1 becomes 7
             if output_grid[row, col] == 8:
                if col > 0 and input_grid[row, col - 1] == 1:
                    output_grid[row, col] = 7


    # Iterate again to apply the 1-to-7 rule based on changes
    for row in range(rows):
        for col in range(cols):

            if input_grid[row,col] == 1:
                neighbors = get_neighbors(input_grid, row, col)
                for r,c in neighbors:
                    if input_grid[r,c] == 8 and output_grid[r,c] == 7:
                        output_grid[row,col] = 7

    return output_grid