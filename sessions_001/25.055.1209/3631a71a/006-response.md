# 3631a71a • 006 • refine_coder

---
```python
"""
1. Identify Contiguous Regions: Locate all contiguous regions (groups of adjacent pixels of the same color) within the input grid.
2. Isolate Blue Regions: From the identified regions, focus solely on those with a blue color (value 1).
3. Determine Removal Target:
    *   If there's only one blue region, remove it.
    *   If there are multiple blue regions, remove the *smallest* blue region.
4. Construct Output: Create the output grid by copying the input grid and setting the pixel values within the bounding box of the targeted blue region to black (value 0).
"""

import numpy as np
from scipy.ndimage import label

def get_contiguous_regions(grid):
    """
    Identifies contiguous regions of the same color in the grid.

    Args:
        grid: The input grid (2D numpy array).

    Returns:
        A list of lists, where each inner list contains the (row, col) coordinates of pixels in a region.
        labeled_grid for debugging and region_props for later.
    """
    labeled_grid, num_labels = label(grid)
    regions = []
    region_props = {}  # Store region properties keyed by label

    for i in range(1, num_labels + 1):  # Label 0 is background
        region_pixels = np.where(labeled_grid == i)
        region_coords = list(zip(region_pixels[0], region_pixels[1]))
        regions.append(region_coords)
        
        # Calculate and store properties
        region_color = grid[region_pixels[0][0], region_pixels[1][0]] # color of the first pixel
        region_size = len(region_coords)
        
        #get bounding box
        min_row, min_col = np.min(region_pixels, axis=1)
        max_row, max_col = np.max(region_pixels, axis=1)
        
        region_props[i] = {
            'color' : region_color,
            'size' : region_size,
            'min_row': int(min_row),
            'min_col': int(min_col),
            'max_row': int(max_row),
            'max_col': int(max_col)
        }

    return regions, labeled_grid, region_props

def transform(input_grid):
    # Convert to numpy array
    grid = np.array(input_grid)
    output_grid = np.copy(grid)

    # Identify contiguous regions and their properties
    regions, labeled_grid, region_props = get_contiguous_regions(grid)

    # Find blue (1) regions
    blue_regions = {}
    for label, props in region_props.items():
        if props['color'] == 1:
            blue_regions[label] = props

    # Determine which blue region to remove
    region_to_remove = None
    if len(blue_regions) == 1:
        region_to_remove = list(blue_regions.keys())[0]
    elif len(blue_regions) > 1:
        smallest_size = float('inf')
        for label, props in blue_regions.items():
            if props['size'] < smallest_size:
                smallest_size = props['size']
                region_to_remove = label

    # Remove the selected blue region if it exists
    if region_to_remove is not None:
        props = blue_regions[region_to_remove]
        for row in range(props['min_row'], props['max_row'] + 1):
            for col in range(props['min_col'], props['max_col'] + 1):
                output_grid[row, col] = 0  # Set to black (0)

    return output_grid.tolist()
```
