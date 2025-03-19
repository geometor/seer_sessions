# 28bf18c6 • 008 • refine_coder

---
```python
"""
The transformation constructs the output by selectively copying a region of the input grid. The region is determined by identifying rows and columns that contain azure (8) pixels.

1.  **Identify Azure Pixels:** Locate all pixels with the value '8' (azure) in the input grid.
2.  **Determine Relevant Rows and Columns:** Find the unique row indices and unique column indices where azure pixels are present. These define the rows and columns of interest within the input grid.
3. **Determine Output Dimensions:** The output is defined by number of rows with azure pixels, and number of columns with azure pixels.
4.  **Construct Output Grid:** Create an output grid with dimensions determined by relevant rows x relevant cols
5. **Populate Output:** Iterate through cells of the output grid, corresponding to the input sub-grid defined by relevant rows and columns. Copy each corresponding value in the input subgrid to the current output cell.
"""

import numpy as np

def get_object_indices(grid, object_color=8):
    rows, cols = np.where(grid == object_color)
    return rows, cols

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Azure Pixels
    object_rows, object_cols = get_object_indices(input_grid)
    
    # 2. Determine Relevant Rows and Columns
    rows_with_object = np.unique(object_rows)
    cols_with_object = np.unique(object_cols)

    # 3. Determine Output Dimensions
    output_height = len(rows_with_object)
    output_width = len(cols_with_object)

    # 4. Construct Output Grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 5. Populate output
    for i in range(output_height):
        for j in range(output_width):
            # Copy corresponding values from input subgrid to output
            output_grid[i, j] = input_grid[rows_with_object[i], cols_with_object[j]]

    return output_grid
```
