# 99b1bc43 • 004 • refine_coder

---
```python
"""
1. Determine Output Grid Size: The output grid is always 4x4, based on the examples.
2. Locate Bottom-Right 2x2 Block: Identify the 2x2 block at the bottom-right corner of the *output* grid.
3. Set to Green: Regardless of the input, set all pixels within the located 2x2 block in the *output* grid to green (color code 3).
4. Fill Remaining: fill the remaining cells in the *output* grid to white (color code 0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as all zeros with size 4x4
    output_grid = np.zeros((4, 4), dtype=int)

    # Set the bottom-right 2x2 block to green
    output_grid[2:4, 2:4] = 3
   
    return output_grid
```

