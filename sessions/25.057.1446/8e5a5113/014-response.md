# 8e5a5113 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation involves a specific type of reflection where the left side of the input is mirrored onto the right and left sides of the output grid, using the gray and white pixels as a central pivot area, with specific ordering on the left hand side of the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # 1. & 2. Identify and Extend Pivot: Find the vertical line of gray (5) pixels and
    # extend to the left in the output.  This doesn't involve modification
    # because gray (5) is already present on input in those locations.
    
    # 3. Reflect Left Side: Reflect columns 0-3 of the input to columns 7-10 of the output.
    for i in range(3):
        output_grid[i, 7:11] = input_grid[i, 0:4]

    # 4. & 5. Mirror to Left Side. columns 4-6 = columns 3-1, and columns 0-2 are 7-9 on input.
    for row_index in range(3):
       output_grid[row_index, 6] = input_grid[row_index, 3]
       output_grid[row_index, 5] = input_grid[row_index, 2]
       output_grid[row_index, 4] = input_grid[row_index, 1]    
       output_grid[row_index, 3] = input_grid[row_index, 0]
       output_grid[row_index, 0] = input_grid[row_index, 7]    
       output_grid[row_index, 1] = input_grid[row_index, 8]   
       output_grid[row_index, 2] = input_grid[row_index, 9]    
       
    return output_grid
```
