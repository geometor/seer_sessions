"""
1. **Initialization:** Start with the output grid being a copy of the input grid.
2. **Conditional Expansion:** Iterate through every pixel of the *input* grid.
3. **Expansion Rule:**  If a pixel in the input grid is NOT blue (1), check its neighbors (up, down, left, right).
    - If ANY neighbor is blue (1), change the *corresponding* pixel in the *output* grid to blue (1).
4. **Additional Rule (Black Background):** If a non-blue pixel in the *input* grid is surrounded by black pixels (0) on all four sides, it *remains unchanged* in the output grid. This rule prevents blue from "leaking" into regions completely enclosed by black.  This takes precedence over the expansion rule.
5. **Stopping criterion:** The iteration through the input grid is completed.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid neighbors (up, down, left, right) for a given cell.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def is_surrounded_by_black(grid, row, col):
    """
    Checks if a cell is surrounded by black (0) pixels on all four sides.
    """
    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r, c] != 0:
            return False
    return True

def transform(input_grid):
    # initialize output_grid as copy of input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # loop for pixels in input and apply expansion rule
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] != 1:
                # Check Black Background rule first
                if is_surrounded_by_black(input_grid, r, c):
                    continue # Remain unchanged

                neighbors = get_neighbors(input_grid, r, c)
                for nr, nc in neighbors:
                    if input_grid[nr, nc] == 1:
                        output_grid[r, c] = 1
                        break  # expand only once

    return output_grid