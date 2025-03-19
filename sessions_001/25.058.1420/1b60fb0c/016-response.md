# 1b60fb0c • 016 • example_3 • investigate_coder

---
```python
"""
1. Preserve Blue: Copy all blue pixels (value 1) from the input grid to the output grid, maintaining their exact positions.
2. Identify Target Whites: Locate white pixels (value 0) in the input grid.  Specifically, white pixels to the immediate left of a blue pixel, considering only horizontal adjacency.
3. Fill with Red: Change the color of identified target white pixels to red (value 2).
4. All other pixels remain white.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)  # Start with a copy to preserve blues

    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Find white pixels (0)
            if input_grid[r, c] == 0:
                # Check for blue pixel to the right (within bounds)
                if c + 1 < cols and input_grid[r, c + 1] == 1:
                    output_grid[r,c] = 2
                
                # more general way to find left-most
                # this checks all the way to the end -- need to optimize
                #found_blue = False
                #for i in range(c + 1, cols) :
                #    if input_grid[r,i] == 1:
                #        found_blue = True
                #        break
                #if found_blue:
                #    output_grid[r, c] = 2
    
    return output_grid
```
