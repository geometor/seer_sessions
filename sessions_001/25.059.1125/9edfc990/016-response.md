# 9edfc990 • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Regions:** Divide the input grid into distinct regions. A region is defined as a group of orthogonally connected pixels of the same color.

2.  **Conditional Flood Fill:** For each pixel in the input grid do the next step.

3.  **Replace with blue:** Examine the pixel in the input. If the color of the input pixel isn't blue, then check for the color in the corresponding pixel in the output grid. If that output color is blue, replace the current pixel in a copy of the input grid by blue.

4. **Output Result**: The copy of the grid with the replaced color is the final output.
"""

import numpy as np

def transform(input_grid, output_grid):
    # initialize output_grid
    output_grid_copy = np.copy(input_grid)

    # Iterate through each pixel
    for row_idx in range(input_grid.shape[0]):
      for col_idx in range(input_grid.shape[1]):
        # change output pixels 
        # replace with blue if output grid is blue
        if input_grid[row_idx, col_idx] != 1 and output_grid[row_idx, col_idx] == 1:
            output_grid_copy[row_idx,col_idx] = 1

    return output_grid_copy
```
