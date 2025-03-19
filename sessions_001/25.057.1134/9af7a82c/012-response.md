# 9af7a82c • 012 • refine_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Create a New Row:** A new row is created at the top of the output grid.
2.  **Fill with Red:** All cells in this new row are filled with the color 2 (red).
3. **Duplicate Grid**: The input grid is copied to the output starting at row index 1 (the row immediately after the new red row).
4. **Duplicate Input**: The input grid is repeated, meaning its stacked below itself one time. The output grid height will equal the original input grid height doubled.

In essence, the output grid consists of a new red row at the top, followed by the original input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_height = input_grid.shape[0] * 2  # Double the height of the input grid
    output_grid = np.zeros((output_height, input_grid.shape[1]), dtype=int)

    # change output pixels
    # Fill the first row with color 2 (red)
    output_grid[0, :] = 2

    # Copy the input grid to the output grid, starting from the second row
    output_grid[1:input_grid.shape[0]+1, :] = input_grid
    
    # Copy the input grid again, below the first copy, completing the duplication.
    output_grid[input_grid.shape[0]+1:, :] = input_grid

    return output_grid
```

