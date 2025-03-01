# 67a423a3 • 012 • refine_coder

---
```python
"""
1.  **Identify the Magenta Line:** Find the vertical line composed entirely of magenta (6) pixels. This line remains unchanged in the output.
2.  **Identify the Azure Line:** Find the horizontal line composed entirely of azure (8) pixels.
3.  **Find the Intersection:** Determine the single pixel where the magenta and azure lines intersect.
4.  **Create Centered Yellow Square:** Create a 3x3 square of yellow (4) pixels. The center of this square is the intersection point found in the previous step.
5. **Replace parts of the azure line:** The yellow square replaces elements of the input, parts of the azure line will be overwritten. The magenta line persists.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find the column indices where all elements are equal to the specified color
    rows, cols = grid.shape
    for col in range(cols):
        if np.all(grid[:, col] == color):
            return col
    return -1  # Return -1 if not found

def find_horizontal_line(grid, color):
    # Find the row indices where all elements are equal to the specified color
     rows, cols = grid.shape
     for row in range(rows):
        if np.all(grid[row, :] == color):
            return row
     return -1


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the vertical magenta line
    magenta_col = find_vertical_line(output_grid, 6)

    # Find the horizontal azure line
    azure_row = find_horizontal_line(output_grid, 8)
    
    # if we can't find lines exit
    if magenta_col == -1 or azure_row == -1:
        return output_grid

    # Calculate the bounding box around the intersection
    # create range for rows and cols, not exceeding the matrix boundaries
    row_start = max(0, azure_row - 1)
    row_end = min(rows, azure_row + 2)
    col_start = max(0, magenta_col - 1)
    col_end = min(cols, magenta_col + 2)

    # Create the yellow bounding box.  Iterate over the range and set the output
    # color.
    for i in range(row_start, row_end):
        for j in range(col_start, col_end):
            output_grid[i, j] = 4

    return output_grid
```
