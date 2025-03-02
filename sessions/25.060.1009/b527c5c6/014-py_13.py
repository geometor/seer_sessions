"""
1.  **Copy Grid:** Begin by creating a copy of the input grid. This copy will be modified to produce the output grid.

2.  **Single Red Pixel Rule:** Locate any "single" red pixels. A red pixel is considered "single" if it has *no* adjacent red pixels (horizontally, vertically, or diagonally). If a single red pixel is found, and if there are three pixels directly above it in the grid, change those three pixels to the sequence: green, red, green (3, 2, 3).

3.  **Conditional Green to Red Transform:** After applying the single red pixel rule, iterate through all the green pixels in the grid.
    *   A green pixel will change to red if and only if:
        *   It has *at least* one red neighbor (horizontally, vertically, or diagonally).
        *   It does *not* have two or more red neighbors.

4.  **Preserve Other Colors:** Pixels that are not red or green, and do not meet the single red pixel condition remain unchanged.
"""

import numpy as np

def get_neighbors(grid, r, c, include_diagonal=True):
    """Gets the neighbors of a cell, optionally including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0):
                continue
            if not include_diagonal and (abs(i) + abs(j) != 1):
                continue

            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def is_single_red(grid, r, c):
    """Checks if a red pixel is isolated (not adjacent to other red pixels)."""
    if grid[r, c] != 2:
        return False
    neighbors = get_neighbors(grid, r, c, include_diagonal=True)
    for nr, nc in neighbors:
        if grid[nr, nc] == 2:
            return False
    return True

def count_red_neighbors(grid, r, c):
    """Counts the number of red neighbors for a given pixel."""
    neighbors = get_neighbors(grid, r, c, include_diagonal=True)
    count = 0
    for nr, nc in neighbors:
        if grid[nr, nc] == 2:
            count += 1
    return count

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Single Red Pixel Rule
    for r in range(rows):
        for c in range(cols):
            if is_single_red(input_grid, r, c):
                if r > 2:  # Ensure there are three pixels above
                    output_grid[r - 3, c] = 3
                    output_grid[r - 2, c] = 2
                    output_grid[r - 1, c] = 3

    # Conditional Green to Red Transform
    temp_grid = np.copy(output_grid) # work from a copy to prevent changes
    for r in range(rows):
        for c in range(cols):
            if temp_grid[r, c] == 3:
                red_neighbors = count_red_neighbors(temp_grid, r, c)
                if 0 < red_neighbors < 2:
                    output_grid[r,c] = 2

    return output_grid