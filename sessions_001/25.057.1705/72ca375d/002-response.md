# 72ca375d • 002 • example_1 • investigate_coder

---
```python
"""
1. Identify the largest contiguous region of magenta (color 6) pixels within the input grid.
2. Determine the bounding box of this magenta region.
3. Crop the input grid to the bounding box.
4. Replace surrounding white space (0) with magenta.
"""

import numpy as np

def find_largest_magenta_region(grid):
    # Find the largest connected component of magenta pixels (value 6).
    magenta_pixels = (grid == 6)
    if not np.any(magenta_pixels):
      return None, None

    labeled_grid, num_labels = scipy.ndimage.label(magenta_pixels)
    largest_label = np.argmax(np.bincount(labeled_grid.flat)[1:]) + 1
    largest_region = (labeled_grid == largest_label)
    return largest_region, np.where(largest_region)
    
import scipy.ndimage

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the largest magenta region and its bounding box coordinates.
    largest_region, magenta_coords = find_largest_magenta_region(input_grid)
    
    if largest_region is None:
        return []

    min_row, min_col = np.min(magenta_coords[0]), np.min(magenta_coords[1])
    max_row, max_col = np.max(magenta_coords[0]), np.max(magenta_coords[1])

    # Crop the input grid to the bounding box.
    cropped_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    # Create output grid and fill the cropped portion with 6
    output_grid = np.zeros_like(cropped_grid)
    output_grid[cropped_grid == 6] = 6
    output_grid[(cropped_grid != 6) & (cropped_grid != 0)] = 6

    # remove all colors that are not 6 inside
    output_grid[output_grid != 6] = 0
    
    #fill non-6 with 6
    output_grid[output_grid == 0] = 6

    
    return output_grid.tolist()
```
