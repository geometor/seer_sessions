# eb5a1d5d • 004 • example_1 • investigate_coder

---
```python
"""
Extract a 5x5 subgrid from the center of the input grid, preserving the key colors (8, 3, and 2) and their relative positions, creating a "thumbnail" representation.
"""

import numpy as np

def get_center(grid):
    """Calculates the center coordinates of a grid."""
    height, width = grid.shape
    center_y = height // 2
    center_x = width // 2
    return center_y, center_x

def extract_subgrid(grid, center_y, center_x, size=5):
    """Extracts a square subgrid centered at the given coordinates."""
    half_size = size // 2
    top = max(0, center_y - half_size)
    bottom = min(grid.shape[0], center_y + half_size + 1)
    left = max(0, center_x - half_size)
    right = min(grid.shape[1], center_x + half_size + 1)
    
    return grid[top:bottom, left:right]
    

def pad_subgrid(subgrid, size=5):
    """Pads the subgrid with 8 to make it 5x5 if it's smaller."""
    
    current_height, current_width = subgrid.shape
    
    pad_height_before = (size - current_height) // 2
    pad_height_after  = size - current_height - pad_height_before
    
    pad_width_before = (size - current_width) // 2
    pad_width_after = size - current_width - pad_width_before

    padded_grid = np.pad(subgrid, ((pad_height_before, pad_height_after), (pad_width_before, pad_width_after)), mode='constant', constant_values=8)
    return padded_grid

def transform(input_grid):
    # Calculate the center of the input grid
    center_y, center_x = get_center(input_grid)

    # Extract a 5x5 subgrid centered at the calculated center
    subgrid = extract_subgrid(input_grid, center_y, center_x)

    # pad the subgrid to 5x5 if necessary
    output_grid = pad_subgrid(subgrid)
    
    # Ensure the presence of colors 2 and 3.  If the subgrid is smaller than 5x5,
    # this also ensures that central pixels from the original image are kept when
    # padding to 5x5
    if 2 not in output_grid:
       output_grid[2,2] = 2 # Place color 2 at the center if it's missing
    if 3 not in output_grid:
        for y in range(5):
          for x in range(5):
            if output_grid[y,x] == 8:
              if (y != 2) or (x != 2):  # avoid clobbering our 2
                output_grid[y,x] = 3 # Place 3
                break
          if 3 in output_grid: break

    return output_grid
```
