# ce602527 • 024 • refine_coder

---
```python
"""
The output is constructed by finding the single green pixel in the input grid, then extracting a vertical segment from the input grid, starting at the green pixel and going down, including all contiguous blue pixels directly below the green pixel. This segment forms the output grid, with a white background.
"""

import numpy as np

def find_green_pixel(grid):
    # Find coordinates of the green pixel (color 3).
    coords = np.argwhere(grid == 3)
    if coords.size == 0:
        return None  # Green pixel not found
    elif coords.shape[0] > 1:
        return None # More than one green pixel
    return coords[0]

def extract_vertical_segment(grid, start_row, col):
    # Extract a vertical segment downwards from (start_row, col).
    segment = []
    row = start_row
    while row < grid.shape[0] and (grid[row, col] == 3 or grid[row, col] == 1):
        segment.append(grid[row, col])
        row += 1
    return segment

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # 1. Find the Green Pixel
    green_pixel_coords = find_green_pixel(input_grid)
    if green_pixel_coords is None:
      return []

    row, col = green_pixel_coords

    # 2. Extract Vertical Segment
    vertical_segment = extract_vertical_segment(input_grid, row, col)

    # 3. Construct Output
    height = len(vertical_segment)
    output_grid = np.zeros((height, 1), dtype=int)  # Initialize with white background (0)
    for i, value in enumerate(vertical_segment):
        output_grid[i, 0] = value

    return output_grid.tolist()
```
