"""
1. Find the Bounding Box: Identify the smallest rectangular region within the input grid that contains all non-zero pixels.
2. Extract the shape: Extract the subgrid defined *only* by the non-zero pixels within the bounding box. This is the "shape" formed by the colored pixels.
3. Preserve or Transpose: If the shape is a single pixel, output it. If the shape is a rectangle of connected pixels, keep it as is for example 1, and transpose/rotate for others. More examples are needed to clarify this rule.
4. Output: Return the resulting grid.
"""

import numpy as np

def get_bounding_box(grid):
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid case
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def extract_shape(grid, bounding_box):
    min_row, max_row, min_col, max_col = bounding_box
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Find the Bounding Box
    bounding_box = get_bounding_box(input_grid)
    if bounding_box is None:  # If no non-zero pixels
        return []

    # 2. Extract the shape
    shape = extract_shape(input_grid, bounding_box)

    # 3. Preserve or Transpose (conditional logic based on examples)

    # 4. Output (convert back to list)
    return shape.tolist()