# 9ecd008a • 020 • refine_coder

---
```python
"""
The transformation rule identifies the single pixel with color 7 (orange) in the input grid.
It constructs a 3x3 grid centered on the coordinates of the pixel with color 7.
If a pixel with color 7 does not exist, or is located to close to the edge of the grid,
the behavior of the transformation is undefined.
"""

import numpy as np

def find_color_pixel(grid, color):
    """Helper function to find the coordinates of a specific color pixel."""
    # Convert grid to numpy array for efficient searching.
    grid_np = np.array(grid)
    # Find the coordinates where the grid equals the specified color.
    coords = np.argwhere(grid_np == color)
    # Return the first coordinate if found, otherwise return None.
    if coords.size > 0:
        return coords[0]
    else:
        return None

def get_center(grid, center_row, center_col, size=3):
    """Helper function to extract a subgrid of given size from center of grid"""
    grid_rows, grid_cols = grid.shape
    
    start_row = center_row - size // 2
    end_row = center_row + size // 2 + 1  # Include the center row
    start_col = center_col - size // 2
    end_col = center_col + size // 2 + 1 # Include the center col    

    # Check for out-of-bounds access
    if start_row < 0 or start_col < 0 or end_row > grid_rows or end_col > grid_cols:
        return None  # Or handle the edge case appropriately

    return grid[start_row:end_row, start_col:end_col]

def transform(input_grid):
    # Find the coordinates of the pixel with color 7.
    center_coords = find_color_pixel(input_grid, 7)
    
    # If no pixel of color 7 is found, return None or handle undefined behavior.
    if center_coords is None:
        return None  # Or some other appropriate default behavior

    # Convert the input grid to a NumPy array
    input_np = np.array(input_grid)

    # Get the 3x3 subgrid centered at the found coordinates.
    output_grid = get_center(input_np, center_coords[0], center_coords[1], 3)

    # Handle the case where a 3x3 subgrid cannot be extracted.
    if output_grid is None:
      return None

    return output_grid.tolist()
```
