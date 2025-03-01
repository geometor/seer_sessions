# d037b0a7 • 012 • refine_coder

---
```python
"""
1. Copy the first row of the input grid to the first row of the output grid.
2. Copy the second row of the input grid to the second row of the output grid.
3. Find the central pixel(s) of the second row of the output grid. If the grid width is even, there will be two central pixels; if odd, there will be one.
4. Replace the color(s) of the central pixel(s) of the second row of the output grid with the color(s) of the central pixel(s) of the *first* row.
5. Copy the modified second row of the output grid to the third row of the output grid.
6. For rows beyond the third:
    *   The fourth row should be a copy of the second row (before modification).
    *   The fifth row should be a copy of the first row.
    *   This pattern (second row, first row) repeats for subsequent rows. If the output would become bigger than the input, stop.
"""

import numpy as np

def get_center_pixel_indices(width):
    # Helper function to calculate the index/indices of the center pixel(s)
    if width % 2 == 0:  # Even width
        return [width // 2 - 1, width // 2]
    else:  # Odd width
        return [width // 2]

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Copy the first row
    output_grid[0] = input_grid[0]

    # 2. Copy the second row
    output_grid[1] = input_grid[1]
    original_second_row = np.copy(input_grid[1]) # Store original for later use


    # 3. & 4. Find and replace central pixel(s)
    width = input_grid.shape[1]
    center_indices = get_center_pixel_indices(width)
    for i in center_indices:
        output_grid[1, i] = input_grid[0, i]


    # 5. Copy the modified second row to the third row
    if input_grid.shape[0] > 2:
        output_grid[2] = output_grid[1]

    # 6. Handle subsequent rows
    for row_index in range(3, input_grid.shape[0]):
        if (row_index - 3) % 2 == 0:  # Even rows after the third (4, 6, ...)
            output_grid[row_index] = original_second_row
        else:  # Odd rows after the third (5, 7, ...)
            output_grid[row_index] = input_grid[0]
    

    return output_grid
```
