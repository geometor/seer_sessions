```python
"""
Transforms an input grid containing mostly 0s (white) and a few 8s (azure) into an output grid with a significantly larger number of 8s. The 8s in the input act as "seeds" that expand outwards to direct neighbors (up, down, left, right) in iterative steps.
"""

import numpy as np

def get_direct_neighbors(grid, row, col):
    """Gets the direct neighbors (up, down, left, right) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor_row, neighbor_col = row + i, col + j
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
            neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the expansion rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    changed = True
    while changed:
        changed = False
        new_grid = np.copy(output_grid)  # Work on a copy for each iteration
        for row in range(rows):
            for col in range(cols):
                if output_grid[row, col] == 0:  # Consider only white pixels
                    neighbors = get_direct_neighbors(output_grid, row, col)
                    for n_row, n_col in neighbors:
                        if output_grid[n_row, n_col] == 8:  # If any direct neighbor is 8
                            new_grid[row, col] = 8  # Change the pixel to 8
                            changed = True
                            break  # Once a pixel is changed, move on
        output_grid = new_grid  # Update the output_grid for the next iteration

    return output_grid
```