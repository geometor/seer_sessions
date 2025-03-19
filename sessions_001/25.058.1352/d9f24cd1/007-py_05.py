import numpy as np

def transform(input_grid):
    output_grid = np.full(input_grid.shape, 2)
    rows, cols = output_grid.shape
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 5:
          output_grid[r,c] = 5

    return output_grid