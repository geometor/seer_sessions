```python
"""
1.  **Identify the Central Object:** Find the smallest rectangular region in the input grid that contains all non-background (non-zero) pixels. This rectangle defines the "central object".
2.  **Determine Border and Inner Colors:** The color of the corner pixel of this rectangle is the "border color." If the rectangle has a width and height greater than 2, the color of the pixel one step inward from the top-left corner is the "inner color." Otherwise the "inner color" and "border color" are the same.
3. **Expand the Object:**
    * increase the size of the rectangle by one layer of pixels on all four sides (up, down, left, right). The dimensions increase by two in each direction (height +2, width +2)
    * The pixels in the expanded layer take the border color where the border of the input rectangle was.
    * The new pixels within the expanded inner region should all have the same color as the inner color of the input object.
4.  **Preserve Unchanged Pixels:** All pixels outside the expanded central object remain unchanged from their original values in the input grid.
"""

import numpy as np

def find_central_object(grid):
    # Find the bounding box of the non-zero pixels
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid
        return None, None, None, None, None, None

    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)

    # Get border and inner colors
    border_color = grid[min_row, min_col]
    if (max_row - min_row + 1) > 2 and (max_col - min_col + 1) > 2:
        inner_color = grid[min_row + 1, min_col + 1]
    else:
        inner_color = border_color

    return min_row, max_row, min_col, max_col, border_color, inner_color

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    # Find the central object
    min_row, max_row, min_col, max_col, border_color, inner_color = find_central_object(input_grid)

    if min_row is None:  # Handle case where no object is found
        return output_grid

    # Calculate expanded dimensions
    new_min_row = max(0, min_row - 1)
    new_max_row = min(output_grid.shape[0] - 1, max_row + 1)
    new_min_col = max(0, min_col - 1)
    new_max_col = min(output_grid.shape[1] - 1, max_col + 1)

    # Fill the expanded region
    for i in range(new_min_row, new_max_row + 1):
        for j in range(new_min_col, new_max_col + 1):
            # Fill with inner color by default
            output_grid[i, j] = inner_color

    # Apply border color to the new border
    for i in range(new_min_row, new_max_row + 1):
      for j in range(new_min_col, new_max_col+1):
        if (i == new_min_row or i == new_max_row) or (j == new_min_col or j == new_max_col):
          if (new_min_row <= i < new_min_row + (min_row - new_min_row)
            or new_max_row - (new_max_row-max_row) <= i <= new_max_row
            or new_min_col <= j < new_min_col + (min_col-new_min_col)
            or new_max_col - (new_max_col - max_col) <= j <= new_max_col):
                output_grid[i,j] = border_color

    return output_grid
```