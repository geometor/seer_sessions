# a699fb00 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Blue Pixels:** Locate all pixels in the input grid with a value of 1 (blue).
2.  **Check for Horizontal Adjacency:** For each blue pixel, check if it has a horizontally adjacent blue pixel (immediately to the left or right).
3.  **Transform to Red:** If a blue pixel has a horizontally adjacent blue pixel, change the *rightmost* blue pixel of the adjacency to a value of 2 (red) in the output grid, otherwise, leave them the same.
4. All non-blue pixels keep their original values.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: Change blue pixels to red if they
    are part of a horizontally adjacent pair of blue pixels, otherwise leave alone.
    """
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell
    for i in range(rows):
        for j in range(cols):
            # Check if current cell is blue
            if input_grid[i][j] == 1:
                # Check for horizontal adjacency (right neighbor)
                if j + 1 < cols and input_grid[i][j + 1] == 1:
                    output_grid[i][j+1] = 2  #change the right neighbor to red
                elif j > 0 and input_grid[i][j-1] == 1:
                    continue # we changed the neighbor, skip.
                else:
                  output_grid[i][j] = 1
    return output_grid
```
