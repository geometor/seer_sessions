```python
"""
Iterate through each pixel of the input grid. If the pixel value is '0' (white), keep it unchanged in the output grid.
If the pixel value is '8' (azure), replace it based on the following rule:
  - Check if '8' is part of the left half or right half of each row.
  - If the '8' pixel is in the left half, replace it with '2'(red).
  - If the '8' pixel is in the right half, replace it with '5'(gray).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Preserve '0'
            if input_grid[i, j] == 0:
                continue  # Do nothing, keep '0' as is
            # Conditional Substitution for '8'
            elif input_grid[i, j] == 8:
                # Check if in left or right half
                if j < cols / 2:
                    output_grid[i, j] = 2  # Replace with '2' (red)
                else:
                    output_grid[i, j] = 5  # Replace with '5' (gray)

    return output_grid
```