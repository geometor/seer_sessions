# b0c4d837 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Key Structures:** Locate the two vertical grey (5) columns in the input grid.
2.  **Locate Azure Rectangle:** Find the azure (8) rectangle within the input grid.
3.  **Identify Intersection:** Determine where azure rectangle intersects with vertical lines.
4. Downsize: create an output by taking the top line of intersecting rectangle, then make the 2nd row below this to be zeros.
5.  **Reduce:** Shrink the grid by a factor of 3 in both dimensions (9x9 to 3x3).
6. clear below: make zeros below the top line of output
"""

import numpy as np

def find_columns_by_color(grid, color):
    """Finds the indices of columns that are entirely a specific color."""
    column_indices = []
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == color):
            column_indices.append(j)
    return column_indices

def find_rectangle_by_color(grid, color):
    """Finds the top-left and bottom-right coordinates of a rectangle of a specific color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No rectangle found
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def transform(input_grid):
    # Find grey columns
    grey_columns = find_columns_by_color(input_grid, 5)

    # Find azure rectangle
    azure_rectangle = find_rectangle_by_color(input_grid, 8)

    # Initialize output grid (3x3) with all zeros
    output_grid = np.zeros((3, 3), dtype=int)

    if azure_rectangle and len(grey_columns)>=2:

      # Extract intersection information (top row of azure rectangle within grey column bounds)
      top_row_azure = azure_rectangle[0][0]
      left_col_azure = azure_rectangle[0][1]
      right_col_azure = azure_rectangle[1][1]

      #check intersection with first two grey columns
      if grey_columns[0] <= left_col_azure and grey_columns[1] >= right_col_azure:
        # Populate the output grid with the intersecting azure pixels
        output_row = 0
        output_col_start = 0

        for col in range(left_col_azure, right_col_azure + 1):

          if (col - left_col_azure)//3 < 3:
            output_grid[output_row, (col - left_col_azure)//3 ] = 8

    return output_grid
```
