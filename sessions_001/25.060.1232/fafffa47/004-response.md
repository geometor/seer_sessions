# fafffa47 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Sub-Objects:** Within the input grid, identify two distinct 3x3 rectangular regions: a top rectangle and a bottom rectangle.
2.  **Extract top rectangle:** Copy the top rectangle and place it to form the output grid
3.  **Recolor:** Change all maroon(9) pixels in the selected region to red (2).
4.  **Recolor:** Change all white pixels in the original top rectangle in the input grid to also zero(0).
"""

import numpy as np

def get_top_rectangle(grid):
    """Helper function to extract the top 3x3 rectangle."""
    return grid[:3, :3]

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Initialize output grid as a copy of the top 3x3 rectangle of the input.
    output_grid = get_top_rectangle(input_grid).copy()

    # Recolor maroon (9) to red (2) and white(0) to white(0) - or do nothing
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 9:
                output_grid[i, j] = 2
            #elif output_grid[i,j] == 0:
            #    output_grid[i,j] = 0

    return output_grid
```
