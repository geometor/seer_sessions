# 50846271 • 008 • example_1 • investigate_coder

---
```python
"""
Replaces red (2) pixels with azure (8) pixels if the red pixel is surrounded by exactly four gray (5) pixels (up, down, left, and right).
Other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Create a copy to modify
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is red (2)
            if input_grid[r, c] == 2:
                # Count gray neighbors (up, down, left, right)
                gray_neighbors = 0
                if r > 0 and input_grid[r - 1, c] == 5:  # Up
                    gray_neighbors += 1
                if r < rows - 1 and input_grid[r + 1, c] == 5:  # Down
                    gray_neighbors += 1
                if c > 0 and input_grid[r, c - 1] == 5:  # Left
                    gray_neighbors += 1
                if c < cols - 1 and input_grid[r, c + 1] == 5:  # Right
                    gray_neighbors += 1

                # If exactly four gray neighbors, change to azure (8)
                if gray_neighbors == 4:
                    output_grid[r, c] = 8

    return output_grid
```

