# 6455b5f5 • 020 • refine_coder

---
```python
"""
1.  **Locate Red Lines:** Identify the single, contiguous, vertical red line and the single, contiguous, horizontal red line in the input grid. Either or both might not exist.

2.  **Background Fill:** Change all white (0) background pixels to blue (1).

3.  **Azure Fill (Conditional):**
    *   If *both* a vertical and a horizontal red line exist:
        *   Define an exclusion zone: This is a rectangular region whose width is defined as three columns to each side of the vertical red line and all rows making up the horizontal red line.
        *   Fill the areas three columns to the left and three columns to the right of the vertical red line with azure (8), *excluding* any pixels within the exclusion zone.
    *   If *only* a vertical red line exists:
        *    Fill the areas three columns to the left and three columns to the right of the vertical red line with azure.
    *   If *only* a horizontal red line exists:
        *  Do *not* perform any azure fill.
    *   If *neither* a vertical or horizontal line exist:
        *    Do *not* perform azure fill

4. Prioritize contiguous red lines.
"""

import numpy as np

def get_vertical_red_line(grid):
    """Finds the single vertical red line in the grid."""
    red_pixels_per_column = np.sum(grid == 2, axis=0)
    potential_line_columns = np.where(red_pixels_per_column > 0)[0]
    
    if potential_line_columns.size == 0:
        return None, None

    # Check for contiguity and single line
    if np.all(np.diff(potential_line_columns) == 1) and np.sum(red_pixels_per_column == np.max(red_pixels_per_column)) == 1 :
        start_col = potential_line_columns[0]
        return start_col, 'vertical'
    return None, None

def get_horizontal_red_line(grid):
    """Finds the single horizontal red line in the grid."""
    red_pixels_per_row = np.sum(grid == 2, axis=1)
    potential_line_rows = np.where(red_pixels_per_row > 0)[0]
     
    if potential_line_rows.size == 0:
        return None, None

    # Check for contiguity and single line
    if np.all(np.diff(potential_line_rows) == 1) and np.sum(red_pixels_per_row == np.max(red_pixels_per_row)) == 1:
        start_row = potential_line_rows[0]
        return start_row, 'horizontal'
    return None, None

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)

    # Find vertical and horizontal red lines
    vertical_line_col, _ = get_vertical_red_line(input_grid)
    horizontal_line_row, _ = get_horizontal_red_line(input_grid)
    
    horizontal_line_rows = []
    if horizontal_line_row is not None:
      red_pixels_per_row = np.sum(input_grid == 2, axis=1)
      horizontal_line_rows = np.where(red_pixels_per_row > 0)[0].tolist()

    # Background Fill
    output_grid[output_grid == 0] = 1

    # Azure Fill (Conditional)
    if vertical_line_col is not None:
        for col_offset in range(1, 4):
            # Left side
            left_col = vertical_line_col - col_offset
            if left_col >= 0:
                for row_index in range(output_grid.shape[0]):
                    if horizontal_line_row is None or row_index not in horizontal_line_rows:
                        output_grid[row_index, left_col] = 8

            # Right side
            right_col = vertical_line_col + col_offset
            if right_col < output_grid.shape[1]:
                for row_index in range(output_grid.shape[0]):
                    if horizontal_line_row is None or row_index not in horizontal_line_rows:
                        output_grid[row_index, right_col] = 8
    return output_grid
```
