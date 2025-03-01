"""
1.  **Copy Grid:** Create a copy of the input grid to serve as the output grid.
2.  **Iterative Expansion:** Repeat the following steps until no changes occur:
    *   Iterate through *every* cell in the *output* grid.
    *   If a cell is blue (1), or was colored in a previous iteration:
        *   Examine its four immediate neighbors (Up, Down, Left, Right) in that order.
        *   If a neighbor is white (0) in the *output grid*:
            *   Change the white neighbor's color based on its direction relative to the current cell:
                *   Up: Change to 2 (red).
                *   Down: Change to 6 (magenta).
                *   Left: Change to 7 (orange).
                *   Right: Change to 8 (azure).
            *   Mark that a change has occurred during this iteration.
3. Return the final output grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right) in order."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col, "Up"))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col, "Down"))  # Down
    if col > 0:
        neighbors.append((row, col - 1, "Left"))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1, "Right"))  # Right
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Color map for expansion
    color_map = {
        "Up": 2,
        "Down": 6,
        "Left": 7,
        "Right": 8
    }

    changed = True
    while changed:
        changed = False
        new_grid = np.copy(output_grid) # work on a copy during each iteration
        for r in range(rows):
            for c in range(cols):
                # If the cell is NOT white (it is either blue or colored)
                if output_grid[r,c] != 0:
                    neighbors = get_neighbors(output_grid, r, c)
                    for nr, nc, direction in neighbors:
                        if output_grid[nr, nc] == 0:  # Check if neighbor is white in output
                            new_grid[nr, nc] = color_map[direction]  # Apply color
                            changed = True  # Mark that a change occurred
        output_grid = new_grid

    return output_grid