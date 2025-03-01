# 67385a82 • 002 • example_4 • investigate_coder

---
```python
"""
Change green (3) to azure (8) if and only if the green pixel is adjacent to another green pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: Change green (3) to azure (8)
    if and only if the green pixel is adjacent to another green pixel.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of input_grid
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # Identify pixels with the value '3' (green)
            if input_grid[r, c] == 3:
                # Check Adjacency: Check neighbors (up, down, left, right)
                adjacent_to_green = False
                # Check up
                if r > 0 and input_grid[r-1, c] == 3:
                    adjacent_to_green = True
                # Check down
                if r < rows - 1 and input_grid[r+1, c] == 3:
                    adjacent_to_green = True
                # Check left
                if c > 0 and input_grid[r, c-1] == 3:
                    adjacent_to_green = True
                # Check right
                if c < cols - 1 and input_grid[r, c+1] == 3:
                    adjacent_to_green = True

                # Conditional Change: If adjacent to another green pixel, change to 8
                if adjacent_to_green:
                    output_grid[r, c] = 8

    return output_grid
```
