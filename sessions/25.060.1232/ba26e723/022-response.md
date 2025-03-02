# ba26e723 • 022 • example_4 • investigate_coder

---
```python
"""
Replaces specific yellow (4) pixels with magenta (6) pixels in a grid. The replacement pattern depends on the position of yellow pixels.
- Corner yellow pixels in the first and third rows are changed to magenta.
- Every other yellow pixel in the first and third rows is changed to magenta.
- Yellow pixels in the second row with yellow neighbors on both sides are changed to magenta.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through rows
    for i in range(rows):
        # Magenta Replacement (Corners): First and Third Rows
        if i == 0 or i == rows -1:
            if output_grid[i, 0] == 4:
                output_grid[i, 0] = 6
            if output_grid[i, cols - 1] == 4:
                output_grid[i, cols - 1] = 6

            # Magenta Replacement (Pattern):  Every other yellow, starting from the second yellow if present
            yellow_indices = np.where(output_grid[i] == 4)[0]
            for j in range(1, len(yellow_indices), 2):
                 output_grid[i, yellow_indices[j]] = 6
                
        # Magenta Replacement (Middle Row)
        elif i == 1:
            for j in range(1, cols - 1):
                if output_grid[i, j] == 4 and output_grid[i, j-1] == 4 and output_grid[i, j+1] == 4:
                    output_grid[i, j] = 6

    return output_grid
```
