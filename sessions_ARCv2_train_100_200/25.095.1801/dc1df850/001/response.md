```python
"""
Initialize the output grid as a copy of the input grid. Iterate through each cell
(r, c) of the *input* grid. If the input cell's value at (r, c) is 2, identify its
8 neighbors (Moore neighborhood). For each neighbor (nr, nc) within grid
boundaries, if the *input* cell at (nr, nc) has a value of 0, set the corresponding
cell's value in the *output* grid to 1. Non-zero cells from the input (including
the 2s) and zero cells not adjacent to a 2 retain their original values in the
output grid.
"""

import copy
import numpy as np # Although not strictly needed for this logic, numpy is often useful for grid tasks

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling the neighbors of '2' cells.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Get grid dimensions
    if not input_grid:
        return []
    rows = len(input_grid)
    if rows == 0:
        return [[]]
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input grid
    # This ensures non-'2' cells and original '2's are preserved unless overwritten later
    # and prevents modifying the input grid directly during iteration.
    output_grid = copy.deepcopy(input_grid)

    # Define the 8 neighbor offsets (Moore neighborhood)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Iterate through each cell of the *input* grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the *input* grid contains a '2'
            if input_grid[r][c] == 2:
                # Iterate through the 8 neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor cell in the *input* grid is '0'
                        if input_grid[nr][nc] == 0:
                            # Set the corresponding cell in the *output* grid to '1'
                            output_grid[nr][nc] = 1

    # Return the modified output grid
    return output_grid
```