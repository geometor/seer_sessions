# 46442a0e • 002 • example_3 • investigate_coder

---
```python
"""
The input grid is expanded into a larger output grid. The elements of the input grid are arranged to form 
a 2x2 larger grid where:
- the top-left quadrant is a copy of the original input.
- The input grid is transformed by rotating 90 degrees clockwise and mirroring horizontally.
- the top-right and the bottom-left quadrants is filled with the the transformed input grid.
- the bottom-right quadrant is filled with the transformed version of the transformed input grid.
"""

import numpy as np

def rotate_and_mirror(grid):
    """Rotates the grid 90 degrees clockwise and then mirrors it horizontally."""
    rotated_grid = np.rot90(grid, k=-1)  # Rotate 90 degrees clockwise
    mirrored_grid = np.fliplr(rotated_grid)  # Mirror horizontally
    return mirrored_grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Transform input
    transformed_grid = rotate_and_mirror(input_grid)
    transformed_grid_2 = rotate_and_mirror(transformed_grid)

    # Create output grid shell
    output_rows, output_cols = transformed_grid.shape
    output_rows = output_rows * 2
    output_cols = output_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Fill the output grid
    output_grid[:rows, :cols] = input_grid
    output_grid[:rows, cols:2*cols] = transformed_grid
    output_grid[rows:2*rows, :cols] = transformed_grid
    output_grid[rows:2*rows, cols:2*cols] = transformed_grid_2
    
    return output_grid.tolist()
```
