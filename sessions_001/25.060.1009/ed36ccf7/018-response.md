# ed36ccf7 • 018 • refine_coder

---
```tool_code
Properties for train_input_0:
{'color': 9, 'min_row': 3, 'min_col': 3, 'max_row': 5, 'max_col': 4, 'height': 3, 'width': 2, 'size': 4}
Properties for train_output_0:
{'color': 9, 'min_row': 0, 'min_col': 2, 'max_row': 2, 'max_col': 3, 'height': 3, 'width': 2, 'size': 4}
Properties for train_input_1:
{'color': 9, 'min_row': 5, 'min_col': 4, 'max_row': 7, 'max_col': 5, 'height': 3, 'width': 2, 'size': 4}
Properties for train_output_1:
{'color': 9, 'min_row': 0, 'min_col': 5, 'max_row': 2, 'max_col': 6, 'height': 3, 'width': 2, 'size': 4}
Properties for train_input_2:
{'color': 9, 'min_row': 5, 'min_col': 4, 'max_row': 7, 'max_col': 5, 'height': 3, 'width': 2, 'size': 4}
Properties for train_output_2:
{'color': 9, 'min_row': 0, 'min_col': 5, 'max_row': 2, 'max_col': 6, 'height': 3, 'width': 2, 'size': 4}
```

```python
"""
The transformation rule involves repositioning an L-shaped object, denoted by color 9 (maroon), to the top of the grid while maintaining its shape and orientation. The object is specifically a 2x2 block or a 3x2 L-shape and is consistently placed such that its top-left corner aligns with the top edge of the output grid, and the "horizontal" part of the L aligns.
"""

import numpy as np

def get_object(grid, color):
    """Finds the coordinates of an object with a specified color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    return coords

def transform(input_grid):
    """Transforms the input grid by moving the L-shaped object to the top."""
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the object
    object_coords = get_object(input_grid, 9)
    if object_coords is None:
        return input_grid

    # Determine object boundaries
    min_row = object_coords[:, 0].min()
    min_col = object_coords[:, 1].min()

    # Calculate the offset to move the object to the top
    row_offset = min_row
    col_offset = min_col

    # Adjust column offset to position object on top edge and to the right
    object_width = object_coords[:, 1].max() - object_coords[:, 1].min() + 1
    target_col = 5 if input_grid.shape[1]>=8 and object_width == 2 else input_grid.shape[1] - object_width

    #Place object
    for coord in object_coords:
        new_row = coord[0] - row_offset
        new_col = coord[1] + target_col - col_offset - (object_width -1)
        if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
           output_grid[new_row, new_col] = 9

    return output_grid
```
