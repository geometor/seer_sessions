# ec883f72 • 018 • example_3 • investigate_coder

---
```python
"""
1. **Identify Existing Objects:** Locate the existing yellow (4) structure and the red (2) square within it.
2. **Preserve:** Keep the yellow structure and red square to the output.
3. **Determine New Pixel Locations:**
    *   Find the highest row (minimum y-coordinate) occupied by the yellow structure.
    *   Place the first new red pixel two row above the highest row of the yellow structure, and at the very beginning of that row (index 0).
    *   Place the second new red pixel two rows above the highest row of the yellow structure, and one row before the very last entry of that row.
4. **Add New Pixels:** Create two new red (2) pixels at the calculated locations.
"""

import numpy as np

def find_object_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    coords = np.argwhere(grid == color)
    return coords

def find_highest_row(coords):
    """Finds the highest row (minimum y-coordinate) among a set of coordinates."""
    if len(coords) == 0:
        return None
    return np.min(coords[:, 0])


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    
    # Find yellow structure coordinates
    yellow_coords = find_object_by_color(input_grid, 4)

    
    # Find the highest row of the yellow structure
    highest_yellow_row = find_highest_row(yellow_coords)

    # Determine new pixel locations
    if highest_yellow_row is not None:
      new_row = max(0, highest_yellow_row - 2)  # Ensure it's not negative
      new_col1 = 0
      new_col2 = output_grid.shape[1] - 2
      new_col2 = max(0, new_col2) # Ensure at least 0.

      # Add new red pixels
      output_grid[new_row, new_col1] = 2
      output_grid[new_row, new_col2] = 2

    return output_grid
```
