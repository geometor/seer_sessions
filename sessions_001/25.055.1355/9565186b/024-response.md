# 9565186b • 024 • refine_coder

---
```python
"""
1. Identify the middle row of the input grid.
2. Create a copy of this middle row.
3. Modify the copied row: Iterate through each pixel in this row. If a pixel is *not* yellow (color value 4), change it to grey (color value 5).
4. Copy the modified row to *all* rows of the output grid. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Identify the middle row index
    middle_row_index = input_height // 2

    # Create a temporary row, which is a copy of the middle row
    temp_row = np.copy(input_grid[middle_row_index])

    # Modify the temporary row
    for j in range(input_width):
        if temp_row[j] != 4:  # Check if the pixel is NOT yellow (4)
            temp_row[j] = 5  # Change the pixel to grey (5)

    # Copy the modified temporary row to all rows of the output grid
    for i in range(input_height):
        output_grid[i] = temp_row

    return output_grid
```

