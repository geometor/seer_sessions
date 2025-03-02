# be94b721 • 024 • refine_coder

---
```python
"""
1.  **Identify Target Color:** Locate all pixels of color 2 (red) in the input grid.
2. **Locate Target Area**: We are only interested in the right most group of red.
3. **Determine the height and width:** The output subgrid size should have the same dimensions as the height and width of the rightmost red region.
4.  **Extract Subgrid:** Extract a subgrid from the input grid, using the dimensions of the target area found in the previous step, centered around the right-most and vertically middle red pixel from the target area. If the centering would extend beyond input boundaries, include only the region within the original boundary.
5. Return the subgrid.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def extract_subgrid(grid, center_row, center_col, height, width):
    """Extracts a subgrid centered at the given coordinates with specified dimensions."""
    start_row = max(0, center_row - height // 2)
    end_row = min(grid.shape[0], center_row + (height + 1) // 2)  #integer division and handle odd height
    start_col = max(0, center_col - width // 2)
    end_col = min(grid.shape[1], center_col + (width + 1) // 2) #integer division and handle odd width
    return grid[start_row:end_row, start_col:end_col]

def get_rightmost_red_region_dimensions(input_grid, red_pixels):
    """Calculates the dimensions of the right-most red region."""
    if len(red_pixels) == 0:  # handle cases with no red
       return 0,0

    rightmost_col = np.max(red_pixels[:, 1])
    rightmost_pixels = red_pixels[red_pixels[:, 1] == rightmost_col]

    min_row = np.min(rightmost_pixels[:, 0])
    max_row = np.max(rightmost_pixels[:, 0])
    min_col = np.min(rightmost_pixels[:, 1])
    max_col = np.max(rightmost_pixels[:, 1])

    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return height, width

def transform(input_grid):
    # Find all red pixels
    red_pixels = find_pixels_by_color(input_grid, 2)

    # Calculate dimensions of right-most red region
    height, width = get_rightmost_red_region_dimensions(input_grid, red_pixels)
    if height==0 or width==0:
      return input_grid.copy()

    # Locate right-most red region and find center
    rightmost_col = np.max(red_pixels[:, 1])
    rightmost_pixels = red_pixels[red_pixels[:, 1] == rightmost_col]
    center_row_index = len(rightmost_pixels) // 2 #integer division to handle odd or even lengths
    center_row, center_col = rightmost_pixels[center_row_index]

    # Extract the subgrid
    output_grid = extract_subgrid(input_grid, center_row, center_col, height, width)

    return output_grid
```
