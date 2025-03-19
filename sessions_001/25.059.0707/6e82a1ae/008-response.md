# 6e82a1ae • 008 • refine_coder

---
```python
"""
Transforms an input grid by replacing gray (5) pixels with blue (1), red (2), or green (3) based on the presence of orange (7) or yellow (4) blocks, or their position within the grid if neither orange nor yellow is present. White (0), yellow (4), and orange (7) pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Check for the presence of orange (7) and yellow (4) pixels.
    has_orange = 7 in input_grid
    has_yellow = 4 in input_grid

    # Iterate through each cell of the input grid.
    for i in range(rows):
        for j in range(cols):
            # Preserve white (0), yellow (4), and orange (7) pixels.
            if output_grid[i, j] in (0, 4, 7):
                continue
            # Identify cells with the value 5 (gray).
            elif output_grid[i, j] == 5:
                # Transformation Rule (Gray Pixels):
                if has_orange:
                    output_grid[i, j] = 1  # Blue
                elif has_yellow:
                    output_grid[i, j] = 2  # Red
                else:
                    # Replace based on location (refined spatial conditions)
                    if i < rows / 2:  # Top half
                        output_grid[i, j] = 1  # Blue
                    else:  # Bottom half
                        output_grid[i,j] = 2 # Red
                        if j+1 < cols and output_grid[i,j+1] == 2 and j == cols -2 : #adjacent right and one from edge
                            output_grid[i,cols-1] = 3 # Green the right most



    return output_grid
```
