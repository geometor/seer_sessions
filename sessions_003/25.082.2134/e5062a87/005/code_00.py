"""
The transformation identifies distinct red regions in the input grid and expands them iteratively. Gray pixels adjacent to each red region are converted to red in each step. The expansion is performed independently for each connected red region, preventing them from merging. The process continues until no more gray pixels can be converted.
"""

import numpy as np
from scipy.ndimage import label

def get_red_regions(grid):
    """
    Identifies distinct connected regions of red pixels (value 2) in the grid.

    Args:
        grid: A 2D numpy array.

    Returns:
        A list of boolean masks, one for each connected red region.
        Each mask has the same shape as the input grid, with 'True'
        indicating membership in the region.
    """
    red_pixels = (grid == 2)
    labeled_array, num_features = label(red_pixels)
    regions = []
    for i in range(1, num_features + 1):  # Iterate through each labeled region
        regions.append(labeled_array == i)
    return regions

def expand_region(grid, region_mask):
    """
    Expands a single red region by converting adjacent gray pixels to red.

    Args:
        grid: The 2D numpy array representing the entire grid.
        region_mask: A boolean mask representing the red region to expand.

    Returns:
        A new boolean mask representing the expanded region, and
        a numpy array representing the grid including the new red pixels.
    """
    rows, cols = grid.shape
    expanded_mask = np.copy(region_mask)
    new_grid = np.copy(grid)

    # Iterate through all pixels in the region mask.
    for i in range(rows):
        for j in range(cols):
            if region_mask[i, j]:
                # Check all 8 neighbors (horizontal, vertical, diagonal).
                for x in range(max(0, i - 1), min(rows, i + 2)):
                    for y in range(max(0, j - 1), min(cols, j + 2)):
                        if (x != i or y != j) and grid[x, y] == 5: # if gray
                            expanded_mask[x,y] = True # add to the region
                            new_grid[x, y] = 2 # change the gray pixel to red

    return expanded_mask, new_grid

def transform(input_grid):
    """
    Transforms the input grid by iteratively expanding connected red regions.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    output_grid = np.copy(input_grid)
    red_regions = get_red_regions(output_grid)
    changes_made = True

    while changes_made:
        changes_made = False
        new_red_regions = []
        
        for region_mask in red_regions:
            expanded_mask, output_grid = expand_region(output_grid, region_mask)
            
            # if expanded mask is different than original mask
            if not np.array_equal(expanded_mask, region_mask):
                changes_made = True
            new_red_regions.append(expanded_mask)  # Use updated mask for next iteration
        
        # use the collected expanded masks for the next iteration    
        red_regions = new_red_regions

    return output_grid