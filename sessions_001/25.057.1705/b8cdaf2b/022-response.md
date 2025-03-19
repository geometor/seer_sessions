# b8cdaf2b • 022 • refine_coder

---
```python
"""
1.  **Initialize:** Create an output grid same size of the input grid and filled with 0.
2.  **Iterate:** Examine the bottom two rows of the input grid.
3.  **Identify:** Locate yellow (4) pixels.
4.  **Check Adjacency**: For each yellow pixel, check if it has at least one red (2) neighbor (horizontally or vertically).
5. **Create:** if there is red neighbor, create new yellow pixel two rows above the location of the original yellow pixel.
6.  **Ignore:** If there is no red neighbor or if the location two rows above will be out of boundary, no yellow pixel will be created for the original yellow pixel.
7. **Output:** The modified grid will be the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the bottom two rows
    for r in range(rows - 2, rows):
        for c in range(cols):
            # Identify yellow pixels
            if input_grid[r, c] == 4:
                # Check for red neighbors
                has_red_neighbor = False
                if r > 0 and input_grid[r-1, c] == 2: # Up
                    has_red_neighbor = True
                if r < rows - 1 and input_grid[r + 1, c] == 2: # Down
                    has_red_neighbor = True
                if c > 0 and input_grid[r, c-1] == 2:       #Left
                    has_red_neighbor = True
                if c < cols - 1 and input_grid[r, c+1] == 2: #Right
                    has_red_neighbor = True
                
                # Create new yellow pixel two rows above if condition is met
                if has_red_neighbor:
                    if r - 2 >= 0:
                        output_grid[r - 2, c] = 4

    return output_grid
```
