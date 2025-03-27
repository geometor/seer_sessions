```python
"""
1.  **Identify Key Rows:** Find all rows containing at least one red (2) pixel (called "red_rows") and all rows containing at least one azure (8) pixel ("azure_rows").

2.  **Duplicate Azure Rows:** For each "red_row" in the input grid, duplicate all "azure_rows" immediately below the "red_row" in the output grid. The order of the azure rows should be maintained.

3.  **Transform Red Row:** In the original "red_row" position within the output grid, modify the "red_row" as follows:
    *   Find the leftmost red pixel and the rightmost azure pixel in the grid.
    *   Change all pixels from the leftmost red pixel *on the red row* to yellow (4) up to, and including, the column containing the rightmost azure.
    *   Any red pixels to the right of the rightmost azure's column position remain red.

4.  All other rows remain unchanged.
"""

import numpy as np

def find_rows_by_color(grid, color):
    """Finds the indices of rows containing at least one pixel of the specified color."""
    rows_with_color = []
    for i, row in enumerate(grid):
        if np.any(row == color):
            rows_with_color.append(i)
    return rows_with_color

def find_leftmost_pixel(row, color):
    """Finds the column index of the leftmost pixel of a specified color in a row."""
    for i, pixel in enumerate(row):
        if pixel == color:
            return i
    return -1  # Should not happen if the row is known to contain the color

def find_rightmost_pixel_in_grid(grid, color):
    """Finds the column index of the rightmost pixel of specified color in grid"""
    rightmost_col = -1
    for row in grid:
        for i in range(len(row)-1, -1, -1): # reverse
            if row[i] == color:
                rightmost_col = max(rightmost_col, i)
                break # next row
    return rightmost_col

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = []

    # Identify key rows
    red_rows = find_rows_by_color(input_grid, 2)
    azure_rows = find_rows_by_color(input_grid, 8)

    # Build the output grid row by row
    for row_index in range(rows):
        if row_index not in red_rows:
            # Keep non-red rows unchanged
            output_grid.append(input_grid[row_index].copy())
        else:
            # Transform the red row
            transformed_row = input_grid[row_index].copy()
            leftmost_red_col = find_leftmost_pixel(transformed_row, 2)
            rightmost_azure_col = find_rightmost_pixel_in_grid(input_grid, 8)

            if leftmost_red_col != -1 and rightmost_azure_col != -1:
                for col_index in range(leftmost_red_col, min(rightmost_azure_col + 1, cols)):
                  transformed_row[col_index] = 4

            output_grid.append(transformed_row)


            # Duplicate azure rows below the transformed red row
            for azure_row_index in azure_rows:
                output_grid.append(input_grid[azure_row_index].copy())

    return np.array(output_grid)
```