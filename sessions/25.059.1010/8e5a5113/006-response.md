# 8e5a5113 • 006 • refine_coder

---
```python
"""
1. **Divide:** Mentally divide the input grid into two vertical halves. The left half contains colored pixels (blue, red, yellow), and the right half consists of grey and white pixels.

2.  **Mirror/Shift & Replace:** The right half of the *output* grid appears to take its structure of gray (5) pixels from the *input*, but with colors from left half replacing them based on the following:

    *   Locate all of the gray pixels. For any gray pixel in the input grid, the pixel will either be yellow, blue, or stay grey.
    *   Locate the white pixels. The white pixels will all be replaced with either the red or blue value.
    *   The left side colors are transposed onto the right side based on their original positions.

3. The overall shape of the gray color in the right side of the input remain the same and fixed.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    midpoint = cols // 2

    # Iterate through the right half of the grid
    for r in range(rows):
        for c in range(midpoint, cols):
            # Determine corresponding column on the left side
            left_col = midpoint - (c - midpoint) - 1

            if input_grid[r, c] == 5:  # If gray
                if left_col >= 0:
                    output_grid[r, c] = input_grid[r, left_col]

            elif input_grid[r, c] == 0:  # If white
                if left_col >= 0 and left_col < midpoint:
                    # Check the mirrored position directly
                    if input_grid[r, left_col] != 5:
                        output_grid[r, c] = input_grid[r, left_col]
                    else:
                        # Find the first non-gray pixel in the row on the left side
                        for i in range(midpoint):
                            if input_grid[r, i] != 5:
                                output_grid[r, c] = input_grid[r, i]
                                break

    return output_grid
```
