# 7447852a • 016 • refine_coder

---
```python
"""
Identifies all red pixels in the input grid. Then, for each white pixel, checks for horizontal or vertical adjacency to any red pixel. If a white pixel is adjacent to any red pixel, it's changed to yellow in the output grid. All red pixels are copied, and others are unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy of input

    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:  # Check for white pixels
                # Check for adjacency to red pixels
                is_adjacent = False
                # Check above
                if r > 0 and input_grid[r - 1, c] == 2:
                    is_adjacent = True
                # Check below
                if r < rows - 1 and input_grid[r + 1, c] == 2:
                    is_adjacent = True
                # Check left
                if c > 0 and input_grid[r, c - 1] == 2:
                    is_adjacent = True
                # Check right
                if c < cols - 1 and input_grid[r, c + 1] == 2:
                    is_adjacent = True

                if is_adjacent:
                    output_grid[r, c] = 4  # Change to yellow

    return output_grid
```

