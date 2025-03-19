# ba97ae07 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to maintain the position and shape of the colored regions.
Specifically, the azure rectangle and the green rectangle remain unchanged.
The background, consisting of white pixels, also remains unchanged.
"""

import numpy as np

def get_object(grid, color):
    # get indices where the grid matches the specified color
    coords = np.where(grid == color)
    if len(coords[0]) == 0: # no matching colors
        return None, None

    # bounding box top left and bottom right
    min_row, min_col = np.min(coords[0]), np.min(coords[1])
    max_row, max_col = np.max(coords[0]), np.max(coords[1])
    return (min_row, min_col), (max_row, max_col)
    

def transform(input_grid):
    """
    Transforms the input grid by maintaining the azure and green rectangles.
    """

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get bounding boxes for azure (8) object
    azure_top_left, azure_bottom_right = get_object(input_grid, 8)
    
    # Get bounding boxes for green (3) object
    green_top_left, green_bottom_right = get_object(input_grid, 3)
    
    # Maintain the shapes and the rest of the grid will remain unchanged
    #   because output_grid starts as a copy

    return output_grid
```
