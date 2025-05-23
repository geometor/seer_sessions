"""
1.  **Identify Key Pixels:** Find all pixels in the input grid that are not white (0).

2.  **Azure (8) Expansion:** If a pixel is azure (8), change *adjacent* white (0)
    pixels to orange (7). Adjacent pixels are those directly above, below,
    left, or right (not diagonal, not L1=2).

3. **Red (2) and Blue (1) Expansion**: For red (2) or blue (1) pixels replace white pixels (0) at L1 distance 2 with yellow (4).

4.  **Magenta Behavior**: Pixels that are magenta (6) do not change the color of any surrounding pixels.
"""

import numpy as np

def get_neighbors(grid, row, col, distance=1):
    """Gets the neighbors of a cell within a specified L1 distance."""
    neighbors = []
    rows, cols = grid.shape
    for i in range(max(0, row - distance), min(rows, row + distance + 1)):
        for j in range(max(0, col - distance), min(cols, col + distance + 1)):
            if (abs(row - i) + abs(col - j)) <= distance and (row,col) != (i,j):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify Key Pixels
    key_pixels = []
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 0:
                key_pixels.append((i, j, input_grid[i, j]))

    # change output pixels
    for r, c, color in key_pixels:
        # Azure (8) Expansion
        if color == 8:
             neighbors = get_neighbors(input_grid, r, c) # distance = 1, default
             for nr, nc in neighbors:
                if output_grid[nr, nc] == 0:  # Check if white
                    output_grid[nr, nc] = 7   # Change to orange

        # Red (2) and Blue (1) Expansion
        elif color == 1 or color == 2:
            neighbors = get_neighbors(input_grid, r, c, distance=2)
            for nr, nc in neighbors:
                if output_grid[nr, nc] == 0:   # Check if white
                    output_grid[nr, nc] = 4    # Change to Yellow

        # Magenta (6) behavior - no change
        elif color == 6:
            pass  # Do nothing.

    return output_grid