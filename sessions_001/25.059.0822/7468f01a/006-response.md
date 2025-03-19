# 7468f01a • 006 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions of red and azure pixels in the input grid.
2.  **Bounding Box:** Determine the smallest bounding box that encompasses *all* red and azure pixels.
3. **Output Dimensions**: The output is a cropped version of the original
   bounding box. The output dimensions are determined by the extent of the
   non-background colors.
4.  **Red Pixel Block:**
    -   Locate the largest contiguous block of red pixels.
    -   The placement of this block defines an anchor.
5.  **Azure Pixel Placement:** Place the azure pixels relative to the red
    pixel block, maintaining the original relative positions of other non-background colors.
6. **Output background:** the background color of the output is red.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def find_contiguous_regions(grid, color):
    """Finds all contiguous regions of a specific color."""
    colored_pixels = (grid == color)
    labeled_array, num_features = label(colored_pixels)
    return labeled_array, num_features

def get_bounding_box(grid):
    """Determine the smallest bounding box encompassing all non-zero pixels."""
    non_zero_pixels = np.argwhere(grid != 0)
    if non_zero_pixels.size == 0:
        return None  # Handle empty grids
    min_row = np.min(non_zero_pixels[:, 0])
    max_row = np.max(non_zero_pixels[:, 0])
    min_col = np.min(non_zero_pixels[:, 1])
    max_col = np.max(non_zero_pixels[:, 1])
    return (min_row, max_row, min_col, max_col)

def find_largest_red_block(grid):
    """Finds the largest contiguous block of red pixels and returns its bounding box."""
    red_regions, num_red_regions = find_contiguous_regions(grid, 2)
    if num_red_regions == 0:
        return None
    
    slices = find_objects(red_regions)
    largest_region_size = 0
    largest_region_slice = None

    for s in slices:
        region_size = (s[0].stop - s[0].start) * (s[1].stop - s[1].start)
        if region_size > largest_region_size:
            largest_region_size = region_size
            largest_region_slice = s

    if largest_region_slice is None:
      return None
    return largest_region_slice


def transform(input_grid):
    # Identify Objects and Bounding Box
    bbox = get_bounding_box(input_grid)
    if bbox is None:
      return np.array([])
    min_row, max_row, min_col, max_col = bbox
    cropped_input = input_grid[min_row:max_row+1, min_col:max_col+1]

    # Find largest red block within the cropped region
    red_block_slice = find_largest_red_block(cropped_input)
    
    # Output Dimensions (same as cropped input)
    output_height = cropped_input.shape[0]
    output_width = cropped_input.shape[1]   

    # Initialize output grid with red background
    output_grid = np.full((output_height, output_width), 2, dtype=int)
    
    # if there aren't any red pixels, return the background
    if red_block_slice is None:
      return output_grid

    # Calculate offset for placing the cropped input into output
    row_offset = red_block_slice[0].start
    col_offset = red_block_slice[1].start
    
    # place azure pixels
    for r in range(output_height):
      for c in range(output_width):
        if cropped_input[r,c] == 8:
          output_grid[r,c] = 8


    return output_grid
```
