"""
The transformation extracts the shape of the azure object from the input, and uses this as instructions for building the output.

1.  **Identify the foreground object:** Locate all pixels with the value '8' (azure) in the input grid.
2.  **Isolate Object rows and columns** create subset of rows and columns that contain the object.
3.  **Condense and potentially reorient:** it will look like three rows
    *   The first row of output will contain all columns with at least one azure pixel, a azure pixel in the output row if the input column contains any object pixels, otherwise white.
    *   The second row skips columns with azure pixels only in the first row of the original.
    *   the third row contains azure pixels if the input row had an azure pixel, otherwise white.
"""

import numpy as np

def get_object_indices(grid, object_color=8):
    rows, cols = np.where(grid == object_color)
    return rows, cols
def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify the foreground object (azure pixels)
    object_rows, object_cols = get_object_indices(input_grid)
    
    if len(object_rows) == 0:  # Handle cases with no object
      return np.zeros((3, 6), dtype=int)


    # 2. Isolate Object rows and columns
    min_row, max_row = np.min(object_rows), np.max(object_rows)
    min_col, max_col = np.min(object_cols), np.max(object_cols)

    # Initialize output grid (3x6)
    output_grid = np.zeros((3, 6), dtype=int)
    
    # Condense:

    # row 1: all cols with azure
    j = 0
    for c in range(input_grid.shape[1]):
      if np.any(input_grid[:,c] == 8):
        output_grid[0,j] = 8
        j += 1

    # row 2: skips cols with azure only on first row
    j = 0
    for c in range(input_grid.shape[1]):
      col = input_grid[:,c]
      if np.any(col[np.where(object_rows > min_row)] == 8):
        output_grid[1,j] = 8
        j += 1
      
    # row 3: all rows with azure
    j = 0
    for r in range(input_grid.shape[0]):
      if np.any(input_grid[r,:] == 8):
        output_grid[2,j] = 8
        j += 1

    return output_grid