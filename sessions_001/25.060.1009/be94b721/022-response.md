# be94b721 • 022 • example_4 • investigate_coder

---
```python
"""
1.  **Identify the Target Color:** Find all pixels of color 2 (red) in the input grid.

2.  **Locate Target Area:** We are only interested in the right most block of red.

3.  **Extract Subgrid:** Extract a 3x3 subgrid from the input grid, centered around the right-most and vertically middle red pixel from the target area found previously. If the centering would extend beyond input boundaries, include only the region within the original boundary

4. return the subgrid
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def extract_subgrid(grid, center_row, center_col, size=3):
    """Extracts a subgrid centered at the given coordinates."""
    half_size = size // 2
    start_row = max(0, center_row - half_size)
    end_row = min(grid.shape[0], center_row + half_size + 1)
    start_col = max(0, center_col - half_size)
    end_col = min(grid.shape[1], center_col + half_size + 1)
    return grid[start_row:end_row, start_col:end_col]

def transform(input_grid):
    # Find all red pixels
    red_pixels = find_pixels_by_color(input_grid, 2)

    # Locate right-most red region and find center
    rightmost_col = np.max(red_pixels[:, 1])
    rightmost_pixels = red_pixels[red_pixels[:, 1] == rightmost_col]
    center_row_index = len(rightmost_pixels) // 2 #integer division to handle odd or even lengths
    center_row, center_col = rightmost_pixels[center_row_index]
    

    # Extract the 3x3 subgrid
    output_grid = extract_subgrid(input_grid, center_row, center_col)

    return output_grid
```
