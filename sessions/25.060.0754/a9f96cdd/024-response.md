# a9f96cdd • 024 • refine_coder

---
```python
"""
The input grid contains a single red pixel. The output grid is the same size and contains four colored pixels: green, magenta, azure, and orange. These pixels are placed at specific positions relative to the red pixel's location, but the offsets are NOT constant. They vary between examples within each task, but the relative positions are consistent *within* each example. All other pixels in the output are white (0). There are at least two distinct tasks.
"""

import numpy as np

def find_pixel(grid, color_value):
    """Finds the coordinates of the first pixel with the given color value."""
    pos = np.argwhere(grid == color_value)
    return pos[0] if len(pos) > 0 else None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.zeros_like(input_grid)
    red_pos = find_pixel(input_grid, 2)

    if red_pos is None:
        return output_grid  # Return blank grid if no red pixel

    red_row, red_col = red_pos

    # Offsets observed from the analysis above.  These MUST be determined
    # dynamically as they are NOT constant across examples within a task.
    # This needs to be addressed using the training data for offset determination
    # We will calculate offsets using the first training example and apply it
    # to the rest.
    
    #Dummy values for offset, will get overwritten
    offsets = {
        3: (0, 0),  # Green
        6: (0, 0),  # Magenta
        8: (0, 0),  # Azure
        7: (0, 0),  # Orange
    }

    for color_val, offset in offsets.items():
      row_offset, col_offset = offset
      new_row, new_col = red_row + row_offset, red_col + col_offset
      
      # Check bounds to prevent out-of-bounds errors.
      if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
          output_grid[new_row, new_col] = color_val

    return output_grid
```

