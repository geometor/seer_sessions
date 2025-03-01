"""
Expands colored regions in a grid. Green (3) pixels expand downwards, and also one pixel to the right of each expanded pixel. Orange (7) pixels expand rightwards, until they reach the edge of the grid or another non-zero pixel. The expansions happen iteratively, one pixel at a time.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    changed = True

    while changed:
        changed = False
        new_grid = np.copy(output_grid)

        for r in range(rows):
            for c in range(cols):
                # Orange (7) Expansion
                if output_grid[r, c] == 7:
                    if c + 1 < cols and output_grid[r, c + 1] == 0:
                        new_grid[r, c + 1] = 7
                        changed = True
                # Green (3) Expansion
                elif output_grid[r, c] == 3:
                    if r + 1 < rows and output_grid[r + 1, c] == 0:
                        new_grid[r + 1, c] = 3
                        changed = True
                    if r + 1 < rows and c + 1 < cols and output_grid[r + 1, c + 1] == 0:
                        new_grid[r + 1, c + 1] = 3
                        changed = True
        output_grid = new_grid

    return output_grid