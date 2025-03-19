# b8825c91 • 024 • refine_coder

---
```python
"""
1.  **Identify Contiguous Regions:** Find all contiguous regions of yellow (4) pixels and blue (1) pixels in the input grid. Consider pixels to be part of the same contiguous region if they are directly adjacent horizontally or vertically, but not only diagonally.

2.  **Green Pixel:** Change all green(3) pixel to black(0).

3. **Yellow and Blue Pixel Group:** Iterate through all yellow pixels. For each one, see if the pixel is inside of the blue pixel group. If so, change the color of the pixel to gray(5).
"""

import numpy as np
from scipy.ndimage import measurements

def get_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    labeled_array, num_features = measurements.label(grid == color)
    regions = []
    for i in range(1, num_features + 1):
        region_coords = np.where(labeled_array == i)
        regions.append(list(zip(region_coords[0], region_coords[1])))
    return regions

def is_inside_blue_region(yellow_pixel, blue_regions):
    """Checks if a yellow pixel is inside any of the blue regions."""
    row, col = yellow_pixel
    for blue_region in blue_regions:
        # Check if the pixel's neighbors are in the blue region
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for neighbor in neighbors:
          if neighbor in blue_region:
            return True;
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find contiguous regions of yellow and blue
    yellow_regions = get_contiguous_regions(input_grid, 4)
    blue_regions = get_contiguous_regions(input_grid, 1)

    # change green(3) pixels to black(0)
    for i in range(rows):
        for j in range(cols):
            if input_grid[i,j] == 3:
                output_grid[i,j] = 0

    # Iterate through yellow pixels and check if they're inside a blue region
    for yellow_region in yellow_regions:
      for yellow_pixel in yellow_region:
          if is_inside_blue_region(yellow_pixel, blue_regions):
              row, col = yellow_pixel
              output_grid[row, col] = 5

    return output_grid
```
