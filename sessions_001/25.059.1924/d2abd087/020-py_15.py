"""
1.  **Identify Connected Gray Regions:** Find all gray (value 5) pixels in the input grid. Group these pixels into distinct regions based on 4-connectivity (up, down, left, right neighbors).
2. **Count Regions:** Determine the number of connected gray regions found.
3. **Recolor based on Region Count and Position.**

    *   If there is only one gray region, recolor all its pixels to red (value 2).
    *   If there are two gray regions, recolor the pixels in the region with the largest x coordinate of the center of mass to red (value 2), the other to blue(value 1).
    *   If there are three gray regions: recolor the region that is horizontally in the middle (comparing x coordinate of its center of mass) to red(value 2), and the other two to blue.

4.  **Preserve Non-Gray Pixels:** All pixels that are not part of a gray region should remain unchanged.
"""

import numpy as np
from scipy.ndimage import label

def get_connected_regions(grid, value):
    """Finds connected regions of a specific value in a grid."""
    mask = (grid == value)
    labeled_array, num_features = label(mask)
    return labeled_array, num_features

def get_region_properties(labeled_array, num_features):
    """Calculates properties of each region (center of mass)."""
    region_properties = []
    for i in range(1, num_features + 1):
        region_pixels = labeled_array == i
        coords = np.where(region_pixels)
        center_of_mass_row = np.mean(coords[0])
        center_of_mass_col = np.mean(coords[1])
        region_properties.append({
            "region_index": i,
            "center_of_mass_row": center_of_mass_row,
            "center_of_mass_col": center_of_mass_col
        })
    return region_properties

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    labeled_array, num_features = get_connected_regions(input_grid, 5) # Find gray regions
    region_props = get_region_properties(labeled_array, num_features) # and their properties

    if num_features == 1:
        # Recolor the single region to red
        output_grid[labeled_array == region_props[0]["region_index"]] = 2
    elif num_features == 2:
        # Recolor based on rightmost center of mass
        if region_props[0]["center_of_mass_col"] > region_props[1]["center_of_mass_col"]:
          red_region_index =  region_props[0]["region_index"]
          blue_region_index = region_props[1]["region_index"]

        else:
          red_region_index =  region_props[1]["region_index"]
          blue_region_index = region_props[0]["region_index"]
        output_grid[labeled_array == red_region_index] = 2
        output_grid[labeled_array == blue_region_index] = 1
    elif num_features == 3:
        #recolor based on horizontal position
        sorted_regions = sorted(region_props, key=lambda x: x["center_of_mass_col"])
        output_grid[labeled_array == sorted_regions[0]["region_index"]] = 1 #leftmost
        output_grid[labeled_array == sorted_regions[1]["region_index"]] = 2 #middle
        output_grid[labeled_array == sorted_regions[2]["region_index"]] = 1 #rightmost

    return output_grid