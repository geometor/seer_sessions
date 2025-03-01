# 10fcaaa3 • 017 • refine_coder

---
```python
"""
The transformation rule involves expanding the width of the grid by a factor of two while keeping the height constant. 
During this horizontal expansion, white(0) pixels are transformed to azure(8), and yellow(4) pixels remain yellow.
Each column is duplicated to the right with the original replaced by 8's
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((input_height, input_width * 2), dtype=int)

    # change output pixels 
    for row in range(input_height):
        for col in range(input_width):
            # Duplicate each column by inserting to the right.
            output_grid[row, col * 2] = 8 # Every original value becomes 8
            if input_grid[row,col] == 4:
                output_grid[row, col * 2 + 1] = input_grid[row,col]  # Copy the yellow
            else:
                output_grid[row, col * 2 + 1] = 8

    return output_grid
```
