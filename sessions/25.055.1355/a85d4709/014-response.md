# a85d4709 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify all gray (5) pixels in the input grid.
2. Check if a gray pixel is located at the center of the grid (row 1, column 1 - zero indexed, the second row and second column).
3. If it is the central pixel, replace it with a yellow (4) pixel.
4. If it not the centeral pixel, replace all other gray pixels with red (2)
5. Identify all white (0) pixels.
6. Replace all white pixels with red (2).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the center coordinates
    center_row = rows // 2
    center_col = cols // 2

    for r in range(rows):
        for c in range(cols):
            # Replace gray (5) pixels
            if output_grid[r, c] == 5:
                if r == center_row and c == center_col:
                    output_grid[r, c] = 4  # Center gray becomes yellow
                else:
                    output_grid[r, c] = 2  # Other grays become red

            # Replace white (0) pixels
            elif output_grid[r, c] == 0:
                output_grid[r, c] = 2  # White becomes red

    return output_grid
```
