"""
1.  **Initialization:** Start with a copy of the input grid as the output grid.

2.  **First Row Transformation:** Identify all blue pixels (value 1) in the first row of the input grid. Change these pixels to red (value 2) in the output grid.

3.  **Iterative Propagation:**
    *   Create an empty list, `changed_pixels`
    *   Iteratively, until no more changes occur:
        *   Add the coordinates of each pixel changed to red to a list called `changed_pixels`
        *    For each changed pixel in `changed_pixels`:
                Find all neighboring pixels (orthogonal and diagonal).
            *   If a neighbor is blue in the input grid, change it to red in the output grid and add its coordinates to `changed_pixels`.
        *   Clear the `changed_pixels` list after each iteration

4.  **Final Output:** The output grid now represents the transformed image. All other pixels remain their original color.
"""

import numpy as np

def get_neighbors(grid, row, col):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                neighbors.append((r, c))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # keep track of changes to re-check neighbors
    changed_pixels = []

    # First pass for first-row blue pixels
    for col in range(cols):
        if input_grid[0, col] == 1:
            output_grid[0, col] = 2
            changed_pixels.append((0,col))

    # Iterative propagation
    while len(changed_pixels) > 0:
        new_changed_pixels = []
        for r, c in changed_pixels:
            neighbors = get_neighbors(input_grid, r, c)
            for nr, nc in neighbors:
                if input_grid[nr, nc] == 1 and output_grid[nr,nc] != 2:
                    output_grid[nr, nc] = 2
                    new_changed_pixels.append((nr, nc))
        changed_pixels = new_changed_pixels

    return output_grid