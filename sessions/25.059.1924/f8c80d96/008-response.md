# f8c80d96 • 008 • example_2 • investigate_coder

---
```python
"""
1. **Preserve Blue:** Copy all blue (1) pixels from the input grid to the output grid, maintaining their exact positions.
2. **Conditional Gray Replacement (Left):** For every white (0) pixel in the input grid, if it is to the *left* of any blue (1) pixel within the same row, and if the row is *not* the last or the second to last row, replace it with gray (5) in the output grid.
3. **Conditional Blue Replacement (Below/Bottom two rows):** White Pixels directly below blue pixels in the bottom two rows are replaced with 1.
4. **Default Gray:** All remaining white(0) pixels in that were not colored blue in the previous step should be changed to gray (5).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""

    output_grid = np.full(input_grid.shape, 5, dtype=int)  # Initialize with gray (5)
    rows, cols = input_grid.shape

    # Preserve blue pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                output_grid[r, c] = 1

    # Conditional gray replacement (left)
    for r in range(rows - 2):  # Iterate up to the second-to-last row
        for c in range(cols):
            if input_grid[r, c] == 0:  # Check if white
                for c2 in range(c + 1, cols):  # check pixels on right
                    if input_grid[r, c2] == 1:  # check for blue
                        output_grid[r, c] = 5  # fill as grey
                        break  # move onto the next white cell

    #Conditional Blue Replacement, last two rows.
    for r in range(rows -2, rows):
        for c in range(cols):
            if input_grid[r,c] == 0:
                if r > 0 and input_grid[r-1,c] == 1:
                    output_grid[r,c] = 1

    return output_grid
```
