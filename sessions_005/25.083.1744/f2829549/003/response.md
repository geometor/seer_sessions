```python
"""
1.  **Identify Input Sub-grid:** Define a region of interest within the input grid consisting of all columns to the *left* of column index 3. That is, columns 0, 1, and 2.
2.  **Create Output Grid:** Create an output grid with the same dimensions as the identified input sub-grid.
3.  **Transform Pixels:** Iterate through the input sub-grid:
    *   If a pixel's value is 7 (orange), set the corresponding pixel in the output grid to 3 (green).
    *   If a pixel's value is not 7, set the corresponding pixel in the output grid to 0 (white).
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input sub-grid (columns 0, 1, and 2)
    rows = input_grid.shape[0]
    cols = 3  # Consider only columns 0, 1, and 2

    # Create output grid with the same dimensions as the sub-grid
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through the input sub-grid
    for r in range(rows):
        for c in range(cols):
            # Transform pixels based on their value
            if input_grid[r, c] == 7:
                output_grid[r, c] = 3
            else:
                output_grid[r, c] = 0

    return output_grid
```
