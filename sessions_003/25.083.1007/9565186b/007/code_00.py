"""
1.  **Identify Yellow Boundaries:** Locate all pixels with color 4 (yellow). These pixels form potential boundaries.
2.  **Closed Loop Check:** Determine if the yellow pixels form one or more *closed, contiguous loops*. A closed loop means that if you trace along adjacent yellow pixels, you return to your starting point without lifting your "finger" and without crossing any non-yellow pixels. The yellow loop must be complete and unbroken.
3.  **Interior Transformation:** Identify regions of connected pixels of color 1, 2, 3, or 8 that are *completely contained* within a closed loop of yellow pixels. "Completely contained" means that the region is entirely inside the yellow loop, and there's no path from any pixel in the region to the edge of the grid without crossing a yellow pixel.
4.  **Change Color:** Change the color of all pixels within these completely contained regions to color 5 (gray).
5. **Preserve Boundaries**: The yellow pixels (color 4) themselves do *not* change.
"""

import numpy as np
from scipy.ndimage import label

def find_yellow_loops(grid):
    """
    Finds closed loops of yellow (color 4) pixels in the grid.
    Returns a mask where loop pixels are True, and others are False.
    """
    rows, cols = grid.shape
    yellow_pixels = (grid == 4)
    labeled_array, num_features = label(yellow_pixels)

    loop_mask = np.zeros_like(yellow_pixels, dtype=bool)

    for feature_label in range(1, num_features + 1):  # Iterate through each labeled region
        feature_pixels = (labeled_array == feature_label)
        # Create a padded array to check for boundary conditions
        padded_feature = np.pad(feature_pixels, pad_width=1, mode='constant', constant_values=0)

        # Find coordinates of the feature pixels in the padded array
        coords = np.argwhere(padded_feature)
        min_row, min_col = np.min(coords, axis=0)
        max_row, max_col = np.max(coords, axis=0)

        # Check if the feature touches the edge of the padded array
        if not (min_row == 0 or min_col == 0 or max_row == padded_feature.shape[0] - 1 or max_col == padded_feature.shape[1] - 1):
            loop_mask[feature_pixels] = True # Closed loop
    return loop_mask

def is_completely_contained(grid, region_mask, yellow_loop_mask):
    """Checks if a region is completely contained within a yellow loop."""
    # Expand the region mask slightly to check for adjacency to yellow pixels.
    expanded_region = np.copy(region_mask)
    rows, cols = grid.shape
    for r, c in np.argwhere(region_mask):
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                expanded_region[nr, nc] = True

    # Check if the expanded region intersects with the yellow loop.
    # If it *doesn't* intersect, it means it is completely inside the loop.
    return not np.any(expanded_region & ~yellow_loop_mask & (grid != 4) )



def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find yellow loops
    yellow_loop_mask = find_yellow_loops(input_grid)

    # Identify regions to transform
    for color in [1, 2, 3, 8]:
        color_regions = (input_grid == color)
        labeled_regions, num_regions = label(color_regions)

        for region_label in range(1, num_regions + 1):
            region_mask = (labeled_regions == region_label)

            # Check if the region is completely contained within a yellow loop
            if is_completely_contained(input_grid, region_mask, yellow_loop_mask):
                #change color
                output_grid[region_mask] = 5

    return output_grid