"""
1.  **Identify Red Regions:** Find all contiguous regions of red (2) pixels. These regions can be of any shape (not just squares).

2.  **Analyze Interior of Red Regions:** For each identified red region, examine its interior pixels (those completely surrounded by red pixels).
3.  **Check Interior Colors:** If the interior contains any white (0) pixels, fill all of the red region's interior pixels to red (2).

4. **Preserve 1x1 Red Pixels:** Leave any isolated 1x1 red (2) pixels unchanged.

5.  **Other Pixels:** All other pixels in the input grid that are *not* part of the interior of a red region remain unchanged in the output grid.
"""

import numpy as np
from scipy.ndimage import label

def find_red_regions(grid):
    """Finds contiguous regions of red pixels."""
    red_pixels = (grid == 2)
    labeled_regions, num_regions = label(red_pixels)
    return labeled_regions, num_regions

def get_interior_pixels(grid, labeled_regions, region_label):
    """Gets the interior pixels of a labeled region."""
    region_mask = (labeled_regions == region_label)
    # Erode the region mask by one layer to find the border
    eroded_mask = np.copy(region_mask)
    rows, cols = np.where(region_mask)
    for r, c in zip(rows, cols):
      if r == 0 or r == grid.shape[0] - 1 or c == 0 or c == grid.shape[1] - 1:
        eroded_mask[r,c] = False
      else:
        neighbors = [
              grid[r-1,c],
              grid[r+1,c],
              grid[r,c-1],
              grid[r,c+1]
        ]
        if any(neighbor != 2 for neighbor in neighbors):
          eroded_mask[r,c] = False
            
    interior_mask = region_mask & ~eroded_mask
    return interior_mask

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all contiguous red regions
    labeled_regions, num_regions = find_red_regions(output_grid)

    # Iterate through each red region
    for region_label in range(1, num_regions + 1):
        # Get the interior pixels
        interior_mask = get_interior_pixels(output_grid, labeled_regions, region_label)

        # Check if the interior contains any white pixels
        if np.any(output_grid[interior_mask] == 0):
            # Fill the interior with red
            output_grid[interior_mask] = 2

    return output_grid