```python
"""
1.  **Identify Azure Region:** Find the rectangular region of azure (8) pixels within the input grid. This region is implicitly bounded by gray (5) pixels, and black(0) pixels around that.
2.  **Create Output Grid:** Create a 3x3 output grid filled with black (0) pixels.
3. **Iterate and select:** Traverse through the *original* locations of azure pixels of the *input* grid starting from the top-left most azure pixel, going right, and then to the start of the next row.
4. **Fill output grid**: Fill cells in the output grid with azure (8) from top-left, going right.
5.  **Stop copying**: If you reach the end of a row in the output, move to the next row. If there are no more azure input pixels, or the output is filled, stop copying and return the current output.
"""

import numpy as np

def find_azure_pixels(grid):
    """Finds the coordinates of all azure (8) pixels."""
    rows, cols = np.where(grid == 8)
    return list(zip(rows, cols))

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)

    # 1. Identify Azure Region (get all azure pixel coordinates)
    azure_pixels = find_azure_pixels(input_grid)

    # 2. Create Output Grid
    output_grid = np.zeros((3, 3), dtype=int)

    # 3. Iterate and select, 4. Fill, and 5. Stop
    output_row = 0
    output_col = 0
    for row, col in azure_pixels:
        if output_row >= 3:  # Stop if output grid is full
            break

        output_grid[output_row, output_col] = 8
        output_col += 1
        if output_col == 3:  # Move to the next row if the current row is full
            output_col = 0
            output_row += 1

    return output_grid
```