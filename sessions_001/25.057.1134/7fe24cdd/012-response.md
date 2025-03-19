# 7fe24cdd • 012 • refine_coder

---
```python
"""
The output grid is constructed as a 2x2 arrangement, where each section (quadrant) is a reflected version of the input grid.

1.  **Top-Left Quadrant:** This quadrant is identical to the input grid. No transformation is applied.

2.  **Top-Right Quadrant:** This quadrant is a horizontally reflected copy of the input grid. The input is mirrored along its vertical axis.

3.  **Bottom-Left Quadrant:** This quadrant is a vertically reflected copy of the input grid. The input is mirrored along its horizontal axis.

4.  **Bottom-Right Quadrant:** This quadrant is both horizontally and vertically reflected, which is equivalent to a 180-degree rotation of the input grid. The input is mirrored along both its vertical and horizontal axes.

The output grid's dimensions are always double the input grid's dimensions in both height and width.
"""

import numpy as np

def reflect_horizontal(grid):
    """Reflects a grid horizontally."""
    return np.fliplr(grid)

def reflect_vertical(grid):
    """Reflects a grid vertically."""
    return np.flipud(grid)

def transform(input_grid):
    """Transforms the input grid into a 2x2 reflected pattern."""
    # Convert the input grid to a NumPy array for easier manipulation.
    input_np = np.array(input_grid)
    
    # Get dimensions of the input grid.
    rows, cols = input_np.shape
    
    # Initialize the output grid with double the dimensions of the input grid.
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)
    
    # Top-Left Quadrant: Copy the input grid as is.
    output_grid[:rows, :cols] = input_np
    
    # Top-Right Quadrant: Horizontally reflected copy.
    output_grid[:rows, cols:] = reflect_horizontal(input_np)
    
    # Bottom-Left Quadrant: Vertically reflected copy.
    output_grid[rows:, :cols] = reflect_vertical(input_np)
    
    # Bottom-Right Quadrant: Horizontally and vertically reflected copy.
    output_grid[rows:, cols:] = reflect_horizontal(reflect_vertical(input_np))
    
    return output_grid.tolist()
```
