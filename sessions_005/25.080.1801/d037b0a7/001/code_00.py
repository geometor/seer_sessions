"""
1.  **Identify the "seed" cell**: Find the rightmost, lowest, non-zero cell in the top 2 rows.
2.  **Fill downwards**: If there are any zeros directly below the "seed" cell, replace them with the "seed" cell's value.
3.  **Fill to the right.** Copy any cells to right that are next to any cells that were changed.
"""

import numpy as np

def find_seed_cell(grid):
    # Iterate through the top two rows from bottom to top, right to left
    for r in range(1, -1, -1):
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
          if r == seed_row:
             if input_grid[r,c] != 0:
                output_grid[r,c] = input_grid[r,c]
          elif r == seed_row + 1 and c >= seed_col:
            if input_grid[r-1,c] != 0:
              output_grid[r,c] = seed_value
          elif r > seed_row and c >=0 :
            if output_grid[r-1,c] != 0:
              output_grid[r,c] = output_grid[r-1,c]
    return output_grid