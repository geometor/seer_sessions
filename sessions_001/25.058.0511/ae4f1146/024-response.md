# ae4f1146 • 024 • refine_coder

---
```python
"""
The transformation rule extracts the minimum bounding box that contains all blue (1) and azure (8) pixels from the input grid and copies it to the output grid. The output grid has the same dimensions as this bounding box, and all pixels within the bounding box, including blue and azure ones, are copied to the output grid in their original relative positions.
"""

import numpy as np

def extract_subgrid(grid, row_start, row_end, col_start, col_end):
    """Extracts a subgrid from the given grid."""
    return grid[row_start:row_end, col_start:col_end]

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # find all blue and azure cells
    blue_azure_indices = np.where((input_grid == 1) | (input_grid == 8))
    
    # compute the minimum bounding box
    min_row = np.min(blue_azure_indices[0])
    max_row = np.max(blue_azure_indices[0])
    min_col = np.min(blue_azure_indices[1])
    max_col = np.max(blue_azure_indices[1])    

    # create output grid of the proper size
    output_grid = np.zeros((max_row-min_row+1, max_col-min_col+1),dtype=int)
    
    # copy all elements inside the bounding box
    for r in range(min_row, max_row+1):
        for c in range(min_col, max_col+1):
            output_grid[r-min_row,c-min_col] = input_grid[r,c]

    return output_grid
```
