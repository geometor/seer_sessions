# ba26e723 • 018 • refine_coder

---
```python
"""
Replace specific yellow (4) pixels with magenta (6) pixels based on their horizontal neighbors in the top row only. If a yellow pixel in the top row has yellow neighbors on both sides (left and right), it changes to magenta. If a yellow pixel in the top row has white neighbors on both sides, it changes to magenta. Otherwise, the pixel remains unchanged. Pixels in other rows are not modified.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    rows, cols = input_grid.shape
    output_grid = input_grid.copy()

    # Iterate through each pixel in the top row (row 0)
    for c in range(cols):
        # Check if the current pixel is yellow (4)
        if input_grid[0, c] == 4:
            # Check neighbors for yellow pixels
            left_neighbor_yellow = (c > 0 and input_grid[0, c-1] == 4)
            right_neighbor_yellow = (c < cols - 1 and input_grid[0, c+1] == 4)

            # Check neighbors for white pixels
            left_neighbor_white = (c > 0 and input_grid[0, c-1] == 0)
            right_neighbor_white = (c < cols - 1 and input_grid[0, c+1] == 0)
            
            # Apply the transformation rule
            if (left_neighbor_yellow and right_neighbor_yellow) or (left_neighbor_white and right_neighbor_white):
                output_grid[0, c] = 6

    return output_grid
```

