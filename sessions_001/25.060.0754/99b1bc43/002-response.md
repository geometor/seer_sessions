# 99b1bc43 • 002 • example_4 • investigate_coder

---
```python
"""
Transforms an input grid of various colors and sizes into a 4x4 output grid where
blue, red, and yellow pixels are converted to green, and white pixels remain white.
The transformation focuses on the top-left quadrant of the input grid if it can
be evenly divided, otherwise a 4x4 section from top-left.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    
    # Initialize a 4x4 output grid filled with white (0)
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the relevant section of the input grid (up to 4x4)
    for i in range(min(4, input_grid.shape[0])):
        for j in range(min(4, input_grid.shape[1])):
            # Check if the pixel is blue (1), red (2), or yellow (4)
            if input_grid[i, j] in (1, 2, 4):
                output_grid[i, j] = 3  # Change to green (3)
            elif input_grid[i, j] == 0:
                output_grid[i,j] = 0 # white remains

    return output_grid.tolist()
```
