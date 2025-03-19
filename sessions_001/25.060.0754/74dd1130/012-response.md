# 74dd1130 • 012 • refine_coder

---
```python
"""
Iterate through each pixel in the input grid. For each pixel, check if any horizontally adjacent neighbor (left or right) has a different color. If the current pixel is red (2) and a horizontally adjacent neighbor is magenta (6), or if the current pixel is magenta (6) and a horizontally adjacent neighbor is red (2), then swap the colors of the two pixels. Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check the left neighbor
            if c > 0:
                if (output_grid[r, c] == 2 and output_grid[r, c - 1] == 6) or \
                   (output_grid[r, c] == 6 and output_grid[r, c - 1] == 2):
                    temp = output_grid[r, c]
                    output_grid[r, c] = output_grid[r, c - 1]
                    output_grid[r, c - 1] = temp

            # Check the right neighbor, no need to double swap
            if c < cols - 1:
                if (output_grid[r, c] == 2 and output_grid[r, c + 1] == 6) or \
                   (output_grid[r, c] == 6 and output_grid[r, c + 1] == 2):
                    temp = output_grid[r, c]
                    output_grid[r, c] = output_grid[r, c+1]
                    output_grid[r,c+1] = temp
    return output_grid
```
