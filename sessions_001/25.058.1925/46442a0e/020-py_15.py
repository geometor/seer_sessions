"""
Expands a 2x2 yellow core of an input grid, adding a row and a column on each side of the core, and copies the adjacent rows and columns of the input grid to the corresponding positions around the expanded core in the output grid. The output grid size is always one larger than the input in each dimension.
"""

import numpy as np

def find_core(grid):
    # Find the 2x2 yellow (4) core in the input grid.  Assumes it exists and is unique.
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 4 and grid[r + 1, c] == 4 and grid[r, c + 1] == 4 and grid[r + 1, c + 1] == 4:
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows + 1, cols + 1), dtype=int)

    core_row, core_col = find_core(input_grid)

    # Expand Core: Place the 2x2 core into the output grid, making it expanded.
    # Determine output core position based on input core position
    output_core_row = core_row
    output_core_col = core_col

    # fill core area in output
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 4:
          output_grid[r,c] = 4
          output_grid[r+1,c] = 4
          output_grid[r,c+1] = 4
          output_grid[r+1,c+1] = 4

    # Copy Adjacent Rows:
    if core_row > 0:  # Check if there's a row above
      output_grid[output_core_row - 1, output_core_col:output_core_col+4] = input_grid[core_row - 1, core_col:core_col+2]

    if core_row + 1 < rows:  # Check if there is a row below the core in input
        output_grid[output_core_row + 4, output_core_col:output_core_col+4] = input_grid[core_row+2, core_col:core_col+2]
        
    # Copy Adjacent Columns:
    if core_col > 0:
      output_grid[output_core_row:output_core_row + 4, output_core_col-1] = input_grid[core_row:core_row + 2, core_col-1]

    if core_col+1 < cols:
      output_grid[output_core_row:output_core_row + 4, output_core_col+4] = input_grid[core_row:core_row + 2, core_col+2]      

    # fill the rest of the output grid
    for r in range(rows):
      for c in range(cols):
          output_grid[r,c] = input_grid[r,c]
          output_grid[r+1,c] = input_grid[r,c]
          output_grid[r,c+1] = input_grid[r,c]
          output_grid[r+1,c+1] = input_grid[r,c]
    
    return output_grid