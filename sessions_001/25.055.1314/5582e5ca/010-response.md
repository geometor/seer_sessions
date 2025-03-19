# 5582e5ca • 010 • refine_coder

---
```python
"""
Transforms an input grid into an output grid of the same dimensions. 
If the number 9 exists in the input grid, the output grid is filled entirely with 9s.
If there is only one color other than white(0) in the input grid, fill the output with the one color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on the presence of 9 or a single unique color.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Check if 9 exists in the input grid.
    if 9 in input_grid:
        output_grid[:] = 9
        return output_grid.tolist()

    # Find unique colors excluding 0 (white).
    unique_colors = np.unique(input_grid)
    unique_colors_without_zero = unique_colors[unique_colors != 0]

    # If only one unique color (besides 0) exists, fill the grid with it.
    if len(unique_colors_without_zero) == 1:
        output_grid[:] = unique_colors_without_zero[0]

    return output_grid.tolist()
```
