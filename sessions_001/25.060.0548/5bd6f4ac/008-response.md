# 5bd6f4ac • 008 • refine_coder

---
```python
"""
1.  **Identify Enclosed Areas:** Examine the input grid to find any 3x3 areas where a single color completely surrounds a single, different-colored, center pixel. "Surrounds" means all eight neighboring pixels of the center pixel have the same color.

2.  **Prioritize by Input Position:** If one enclosed area is found, extract the 3x3 grid with that area's center as the output. If no enclosed areas are found, the output grid is at the top left of the input grid.

3. **Output 3x3 Subgrid**
"""

import numpy as np

def find_enclosed_area(input_grid):
    """
    Finds the coordinates of a 1x1 area enclosed by a single color.
    """
    input_grid = np.array(input_grid)
    in_height, in_width = input_grid.shape

    for row in range(1, in_height - 1):
        for col in range(1, in_width - 1):
            center_pixel = input_grid[row, col]
            surrounding_pixels = [
                input_grid[row - 1, col - 1],
                input_grid[row - 1, col],
                input_grid[row - 1, col + 1],
                input_grid[row, col - 1],
                input_grid[row, col + 1],
                input_grid[row + 1, col - 1],
                input_grid[row + 1, col],
                input_grid[row + 1, col + 1],
            ]
            # Check if all surrounding pixels are the same color and different from the center.
            if len(set(surrounding_pixels)) == 1 and surrounding_pixels[0] != center_pixel:
                return (row, col)
    return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find enclosed area
    enclosed_coords = find_enclosed_area(input_grid)

    # If enclosed area is found, extract the 3x3 subgrid
    if enclosed_coords:
        row, col = enclosed_coords
        output_grid = input_grid[row-1:row+2, col-1:col+2]
    else:
    # use top left corner
        output_grid = input_grid[0:3, 0:3]

    return output_grid.tolist()
```
