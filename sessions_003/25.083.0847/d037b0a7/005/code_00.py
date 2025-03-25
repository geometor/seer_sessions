"""
1. Iterative Zero Filling: Scan the grid. If a cell is *not* zero, check its neighbors (directly below and to the right).
2. Conditional Propagation: If a neighboring cell (down or right) is zero, copy the non-zero cell's value into the zero cell.
3. Repeat: Continue scanning and propagating until no more changes can be made, i.e. perform steps 1 and 2 until a complete scan of the grid results in zero changes.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    changed = True

    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] != 0:
                    # Check below
                    if r + 1 < rows and output_grid[r + 1, c] == 0:
                        output_grid[r + 1, c] = output_grid[r, c]
                        changed = True
                    # Check right
                    if c + 1 < cols and output_grid[r, c + 1] == 0:
                        output_grid[r, c + 1] = output_grid[r, c]
                        changed = True
    return output_grid