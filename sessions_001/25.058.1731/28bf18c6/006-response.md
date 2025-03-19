# 28bf18c6 • 006 • refine_coder

---
```python
"""
The transformation extracts the shape of the azure object from the input, and uses this as instructions for building the output.

1.  **Identify the Azure Object:** Locate all pixels with the value '8' (azure) in the input grid. This defines the "object" of interest.

2.  **Determine Output Dimensions:**
    *   The output grid's height is equal to the number of rows in the input grid that contain at least one azure pixel.
    *   The output grid's width is equal to the number of columns in the input grid that contain at least one azure pixel.

3. **Populate the Output Grid:** Iterate through each cell of the *potential* output grid (using the dimensions determined in step 2).
   *   Get the corresponding row index (`r`) from the input grid, skipping rows with all non-azure pixels.
   *   Get the corresponding column index (`c`) from the input grid, skipping columns with all non-azure pixels.
   *   If the input grid cell at `input_grid[r][c]` contains an azure pixel, the output cell will also be azure. Otherwise the output cell will be white (0).
"""

import numpy as np

def get_object_indices(grid, object_color=8):
    rows, cols = np.where(grid == object_color)
    return rows, cols

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify the Azure Object
    object_rows, object_cols = get_object_indices(input_grid)
    
    if len(object_rows) == 0:  # Handle cases with no object
      return np.zeros((0, 0), dtype=int)

    # 2. Determine Output Dimensions
    rows_with_object = np.unique(object_rows)
    cols_with_object = np.unique(object_cols)
    output_height = len(rows_with_object)
    output_width = len(cols_with_object)

    # initialize output_grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 3. Populate the Output Grid
    for i in range(output_height):
        for j in range(output_width):
            # check corresponding input cell
            if input_grid[rows_with_object[i], cols_with_object[j]] == 8:
                output_grid[i, j] = 8

    return output_grid
```
