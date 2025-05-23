"""
1.  **Identify Seeds:** Locate all existing red (2) pixels in the input grid.

2.  **Expansion:** For each red pixel:
    *   Examine its eight neighboring pixels (horizontal, vertical, and diagonal).
    *   If a neighboring pixel is gray (5), change it to red (2).

3.  **Iteration**: Repeat Step 2 until it no longer changes anything. One thing I am unsure is the amount of iterations this expansion happens, but in the second iteration it includes gray that was converted to red, so at the least it is until no more changes can be made.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the coordinates of the eight neighbors of a pixel."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row = row + i
            neighbor_col = col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def transform(input_grid):
    """Transforms the input grid by expanding red pixels into adjacent gray areas."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    changed = True
    while changed:
        changed = False
        red_pixels = []
        # find current red pixels. Has to be inside loop because the locations change
        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] == 2:
                    red_pixels.append((r, c))
        
        for r, c in red_pixels:
            neighbors = get_neighbors(output_grid, r, c)
            for nr, nc in neighbors:
                if output_grid[nr, nc] == 5:
                    output_grid[nr, nc] = 2
                    changed = True # flag to continue looping if we made changes

    return output_grid