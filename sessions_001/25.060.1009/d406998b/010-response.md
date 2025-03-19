# d406998b • 010 • example_2 • investigate_coder

---
```python
"""
Iterate through each pixel of the input grid.
Identify gray (5) pixels.
Check location of gray pixel against this pattern
    *   If the gray pixel is in the first row and it's the second or fourth gray pixel of the row, change it to green (3).
    *   If the gray pixel is in the second row, and it's the third gray pixel of the row, change it to green (3).
    *   If the gray pixel is in the third row, and it's the second or fourth gray pixel of the row, change it to green (3).
Leave all other pixels (white or already green) unchanged.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        gray_count = 0
        for c in range(cols):
            if input_grid[r, c] == 5:
                gray_count += 1
                if r == 0 or r == 2:  # First and third rows
                    if gray_count == 2 or gray_count == 4:
                        output_grid[r, c] = 3
                elif r == 1:  # Second row
                    if gray_count == 3:
                        output_grid[r, c] = 3
    return output_grid
```
