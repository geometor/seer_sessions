"""
1.  **Find the Seed:** Identify the "seed" cell. This is the rightmost, lowest, non-zero cell within the top two rows of the input grid.

2.  **Propagate Down and Right:**
    *   Start at the seed cell.
    *   **Downward Filling:** If the cell directly below the current cell (either the seed cell or a previously filled cell) has a value of 0, replace it with the seed cell's value.
    *   **Rightward Filling:** If any cell changed, copy its value to all the cells on the right in the same row.
    *   **Combined downward + rightward filling.** If a cell is not 0 in the row above the current cell, copy the cell from above and also propagate to the right.

3. Repeat Step 2 until the bottom of the grid is reached, propagating values downwards.
"""

import numpy as np

def find_seed_cell(grid):
    # Iterate through the top two rows from bottom to top, right to left
    for r in range(min(1, len(grid) - 1), -1, -1):
        for c in range(len(grid[0]) - 1, -1, -1):
            if grid[r][c] != 0:
                return (r, c)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Find the "seed" cell
    seed_coords = find_seed_cell(input_grid)
    if seed_coords is None:
        return output_grid

    seed_value = input_grid[seed_coords[0], seed_coords[1]]
    seed_row, seed_col = seed_coords
    
    # Fill downwards and to the right
    for r in range(seed_row, len(output_grid)):
        for c in range(0, len(output_grid[0])):
            if r == seed_row: # seed row, keep original
                continue
            elif output_grid[r-1,c] == 0: # downward filling if above is 0
                if c == 0:  # Check if we have a valid seed
                    if seed_row == r-1:
                        output_grid[r,c] = seed_value
                    else:
                        continue
                elif output_grid[r, c-1] != 0:
                  output_grid[r,c] = output_grid[r, c-1]

            else:   # copy directly from above.
              output_grid[r,c] = output_grid[r-1,c]
    return output_grid