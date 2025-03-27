```python
"""
1.  **Identify** all rows in the input grid that contain green (3) pixels.
2.  **For each** of these identified rows:
    *   **Insert** an orange (7) pixel to the immediate left of the leftmost green (3) pixel in that row.
    *   **Insert** an orange (7) pixel to the immediate right of the rightmost green (3) pixel in that row.
3. **All other** rows of the output grid are the same as in the input grid.
"""

import numpy as np

def get_green_rows(grid):
    # returns rows containing green pixels
    green_rows = []
    for i, row in enumerate(grid):
        if 3 in row:
            green_rows.append(i)
    return green_rows
            
def transform(input_grid):
    """Transforms the input grid by wrapping green blocks with orange pixels."""

    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows_with_green = get_green_rows(input_grid)

    # Iterate through rows that have green pixels
    for row_index in rows_with_green:
        row = input_grid[row_index]
        
        # Find the indices of the green pixels
        green_indices = np.where(row == 3)[0]

        # find the leftmost and rightmost
        leftmost_green_index = green_indices[0]
        rightmost_green_index = green_indices[-1]
        
        # bounds check and set left pixel to orange (7)
        if leftmost_green_index > 0:
            output_grid[row_index, leftmost_green_index - 1] = 7
        # bounds check and set right pixel to orange (7)
        if rightmost_green_index < len(row) - 1:
            output_grid[row_index, rightmost_green_index + 1] = 7

    return output_grid.tolist()
```