"""
1.  **Identify and Replace:** Find all gray pixels (value '5') in the input grid. Replace each gray pixel with a blue pixel (value '1') in the output grid.
2.  **Create Blue Blocks:** For each of the original gray pixel locations, create a 3x3 block of blue pixels (value '1') in the output grid, centered on the location of the replaced gray pixel.
3.  **Conditional Expansion:** Examine the pixels directly adjacent to the 3x3 blue blocks created in the previous step. If any of these adjacent pixels are white (value '0') in the *input* grid, change them to blue (value '1') in the output grid.
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
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify and Replace '5' with '1'
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r,c] = 1

    # 2. Create 3x3 Blue Blocks
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:  # Check *input* grid for original '5' locations
                for i in range(max(0, r - 1), min(rows, r + 2)):
                    for j in range(max(0, c - 1), min(cols, c + 2)):
                        output_grid[i,j] = 1

    # 3. Conditional Expansion
    output_grid_copy = np.copy(output_grid) # Use a copy for checking neighbors.
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 5:
              for i in range(max(0, r - 1), min(rows, r + 2)):
                  for j in range(max(0, c - 1), min(cols, c + 2)):
                      for nr, nc in get_neighbors(output_grid_copy, i, j):
                          if input_grid[nr, nc] == 0:  # Check *input* grid for '0'
                              output_grid[nr, nc] = 1

    return output_grid.tolist()