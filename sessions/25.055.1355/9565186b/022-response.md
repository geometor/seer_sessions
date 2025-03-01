# 9565186b • 022 • refine_coder

---
```python
"""
1. Identify the middle row of the input grid.
2. Copy this row to a new grid, which will become the output.
3. In the copied row, change any pixel that is not yellow to grey.
4. Copy this modified row to all rows of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid, ensuring it has the same dimensions
    output_grid = np.copy(input_grid)
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Identify the middle row index
    middle_row_index = input_height // 2

    # Create a temporary row to store the transformed middle row
    temp_row = np.copy(input_grid[middle_row_index])

    # change output pixels
    # Iterate through the temporary row and change non-yellow pixels to grey
    for j in range(input_width):
        if temp_row[j] != 4:  # Check if the pixel is NOT yellow (4)
            temp_row[j] = 5  # Change the pixel to grey (5)

    # Copy the modified temporary row to all rows of the output grid
    for i in range(input_height):
        output_grid[i] = temp_row

    return output_grid
```
