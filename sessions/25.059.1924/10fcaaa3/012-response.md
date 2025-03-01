# 10fcaaa3 • 012 • example_3 • investigate_coder

---
```python
"""
Expands the input grid into a larger output grid. A 2x2 pattern is replicated: 
- If the input grid pixel is 4 (yellow), it remains the same in the output.
- If the input is 0 (white), the 2x2 block becomes: 8, 0, 0, 8 (azure, white, white, azure) 
  placed at the correct location in the output grid.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Find the yellow (4) pixel coordinates
    yellow_coords = np.argwhere(input_grid == 4)

    # Determine output grid size
    output_rows = 2 * rows + 2 * len(yellow_coords)
    output_cols = 2 * cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through the input grid and build the 2x2 blocks
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 4:  # Yellow pixel
                #duplicate the position relative the number of yellow pixels before this one.
                num_yellows_above = np.sum(yellow_coords[:, 0] < i)
                output_grid[2*i + num_yellows_above*2, 2*j] = 4
                output_grid[2*i + num_yellows_above*2, 2*j + 1] = 4
                output_grid[2*i+1 + num_yellows_above*2, 2*j] = 4
                output_grid[2*i+1 + num_yellows_above*2, 2*j + 1] = 4

            elif input_grid[i, j] == 0:  # White pixel
                num_yellows_above = np.sum(yellow_coords[:, 0] < i)

                output_grid[2*i + num_yellows_above*2, 2*j] = 8
                output_grid[2*i + num_yellows_above*2, 2*j + 1] = 0
                output_grid[2*i + 1 + num_yellows_above*2, 2*j] = 0
                output_grid[2*i + 1 + num_yellows_above*2, 2*j+1] = 8

    return output_grid
```
