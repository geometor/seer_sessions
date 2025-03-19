# 50846271 • 010 • refine_coder

---
```python
"""
A red pixel is changed to azure if and only if the four pixels directly above, below, to the left, and to the right of it are all the same color. The surrounding pixels can be any color, but they must all be the *same* color. Pixels that are not red, or red pixels that do not meet this condition remain unchanged.
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
                # Get the colors of the neighbors (up, down, left, right)
                neighbors = []
                if r > 0:
                    neighbors.append(input_grid[r - 1, c])  # Up
                if r < rows - 1:
                    neighbors.append(input_grid[r + 1, c])  # Down
                if c > 0:
                    neighbors.append(input_grid[r, c - 1])  # Left
                if c < cols - 1:
                    neighbors.append(input_grid[r, c + 1])  # Right

                # Check if all neighbors are the same color and there are four of them.
                if len(neighbors) == 4 and all(color == neighbors[0] for color in neighbors):
                    output_grid[r, c] = 8

    return output_grid
```
