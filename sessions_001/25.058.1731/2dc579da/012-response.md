# 2dc579da • 012 • refine_coder

---
```python
"""
1.  **Locate the Blue Pixel:** Find the single blue (1) pixel within the input grid.

2.  **Conditional Transformation:**
    *   **If** the blue pixel's location allows for a full 3x3 subgrid extraction *without going out of bounds*, extract the 3x3 region centered on the blue pixel.
    *  **Else, if** extracting a 3x3 grid would go out of bounds on input, the output is identical to input.

3.  **Output:** The output is either the extracted 3x3 region or a copy of the input grid based on step 2.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    # Find coordinates of a pixel with the specified color
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return first occurrence
    return None

def transform(input_grid):
    """
    Transforms the input grid based on the location of the blue pixel.
    """
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # Locate the blue pixel
    blue_pixel_coords = find_pixel_by_color(input_grid, 1)

    if blue_pixel_coords is None:
        return input_grid.tolist() # if no blue pixel return the original.

    # Define the region (3x3 window)
    row, col = blue_pixel_coords
    row_start = row - 1
    row_end = row + 2
    col_start = col - 1
    col_end = col + 2

    # Check for out-of-bounds
    if row_start >= 0 and row_end <= input_grid.shape[0] and col_start >= 0 and col_end <= input_grid.shape[1]:
        # Extract the 3x3 region
        output_grid = input_grid[row_start:row_end, col_start:col_end]
        return output_grid.tolist()
    else:
        # Return the original input grid
        return input_grid.tolist()
```
