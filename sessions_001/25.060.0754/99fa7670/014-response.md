# 99fa7670 • 014 • refine_coder

---
```python
"""
1.  **Preserve Dimensions:** The output grid has the same dimensions as the input grid.
2.  **Iterate Through Input:** Examine each pixel in the input grid.
3.  **Expand Non-Zero Pixels:** If a pixel is non-zero:
    *   Copy its color value.
    *   Create a 2x2 block in the output grid, starting at the same coordinates as the input pixel. Fill all four cells of this 2x2 block with the copied color.
4.  **Preserve Zero Pixels:** If a pixel is zero (white), the corresponding pixel (and any potential 2x2 block overlaps) in the output grid remains zero. This ensures we don't overwrite previous expansions if non-zero pixels are adjacent.
"""

import numpy as np

def transform(input_grid):
    # Create an output grid with the same dimensions and data type as the input grid,
    # initialized with zeros.  This ensures the dimensions match.
    output_grid = np.zeros_like(input_grid)

    # Iterate through each pixel of the input grid using nested loops.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Check if the current pixel is non-zero.
            if input_grid[i, j] != 0:
                # Get the color of the non-zero pixel.
                color = input_grid[i, j]

                # Create the 2x2 block, handling potential boundary issues.
                # We use min() to ensure we don't go beyond the grid's boundaries.
                for row_offset in range(2):
                    for col_offset in range(2):
                        new_row = i + row_offset
                        new_col = j + col_offset
                        if new_row < output_grid.shape[0] and new_col < output_grid.shape[1]:
                          output_grid[new_row, new_col] = color

    return output_grid
```

