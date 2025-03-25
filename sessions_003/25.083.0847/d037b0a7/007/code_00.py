"""
1.  **Identify the Bounding Box:** Determine the smallest rectangle encompassing all non-zero pixels in the input grid. This defines the active region for the transformation.
2.  **Iterative Filling:** Within the bounding box, locate zero-valued cells.
3.  **Neighbor Propagation:** For each zero-valued cell, check its non-zero neighbors (up, down, left, and right).
    *   If a zero has non-zero neighbor to the up or left: copy the value.
    *   If a zero has non-zero neighbor to the right or below, copy the value
4. If there is any changes in the grid, repeat the process.
5. **Repeat:** Iterate steps 2 and 3 until the entire region within the bounding box is filled, with all original objects being merged into one.
"""

import numpy as np

def find_bounding_box(grid):
    """Finds the smallest rectangular bounding box for non-zero pixels."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None  # Empty grid
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the bounding box
    bounding_box = find_bounding_box(output_grid)
    if bounding_box is None:
        return output_grid  # Nothing to do if the grid is all zeros

    (min_row, min_col), (max_row, max_col) = bounding_box

    changed = True
    while changed:
        changed = False
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                #Iterative filling, find zero cells
                if output_grid[r, c] == 0:
                    # Neighbor Propagation: up, down, left, right
                    
                    # Check up
                    if r > 0 and output_grid[r - 1, c] != 0:
                        output_grid[r, c] = output_grid[r - 1, c]
                        changed = True
                        continue #check the others only if not set
                    # Check left
                    if c > 0 and output_grid[r, c - 1] != 0:
                        output_grid[r, c] = output_grid[r, c - 1]
                        changed = True
                        continue #check the others only if not set
                    # Check down
                    if r + 1 < rows and output_grid[r + 1, c] != 0:
                        output_grid[r, c] = output_grid[r + 1, c]
                        changed = True
                        continue
                    # Check right
                    if c + 1 < cols and output_grid[r, c + 1] != 0:
                        output_grid[r, c] = output_grid[r, c + 1]
                        changed = True

    return output_grid