```python
"""
1.  **Identify all non-zero pixels:** Find all pixels within the input grid that have a value other than zero.
2.  **Determine Bounding Box:** Create a bounding box that encompasses *all* non-zero pixels. The bounding box's edges should be parallel to the input grid's edges, and it should be the smallest possible rectangle containing all non-zero pixels.
3.  **Construct Output Grid:** Create a 2x2 output grid.
4.  **Populate Output:** Fill the output grid with values from the input grid, sampled from the corners of the bounding box determined in step 2:
    *   Output[0, 0] = Input[min_row, min_col] (Top-left corner)
    *   Output[0, 1] = Input[min_row, max_col] (Top-right corner)
    *   Output[1, 0] = Input[max_row, min_col] (Bottom-left corner)
    *   Output[1, 1] = Input[max_row, max_col] (Bottom-right corner)
"""

import numpy as np

def find_bounding_box(grid):
    """Finds the bounding box of all non-zero pixels."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle the case where there are no non-zero pixels
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the bounding box of all non-zero pixels
    bounding_box = find_bounding_box(input_grid)

    if bounding_box is None:
        return [[]]

    min_row, min_col, max_row, max_col = bounding_box

    # Construct 2x2 output array
    output_grid = np.zeros((2, 2), dtype=int)

    # Sample from the corners
    output_grid[0, 0] = input_grid[min_row, min_col]
    output_grid[0, 1] = input_grid[min_row, max_col]
    output_grid[1, 0] = input_grid[max_row, min_col]
    output_grid[1, 1] = input_grid[max_row, max_col]

    return output_grid.tolist()
```