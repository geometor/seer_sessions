"""
The transformation rule is as follows:

1. Identify contiguous regions: Scan the input grid to identify all contiguous regions of pixels that share the same color. A contiguous region is defined as a group of pixels of the same color that are directly adjacent to each other (horizontally or vertically).
2. Calculate region sizes and bounding boxes: For each identified contiguous region, calculate its size (the number of pixels it contains) and its bounding box (min_row, min_col, max_row, max_col).
3. Identify the largest region of color blue (1): Find the contiguous region with the largest size among all regions that have the color blue (1). If no blue regions are found, no changes are made.
4. Remove the largest blue region: If a largest blue region is found, remove all pixels within its bounding box from the output grid by setting those pixels to black (0).
5. Construct output: Create the output grid by keeping only the pixels that were not part of the removed region or are within smaller blue regions.
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

    # Find the largest blue (1) region
    largest_blue_region = None
    largest_blue_size = 0
    for label, props in region_props.items():
        if props['color'] == 1 and props['size'] > largest_blue_size:
            largest_blue_size = props['size']
            largest_blue_region = label

    # Remove the largest blue region if it exists
    if largest_blue_region is not None:
        props = region_props[largest_blue_region]
        for row in range(props['min_row'], props['max_row'] + 1):
            for col in range(props['min_col'], props['max_col'] + 1):
                output_grid[row, col] = 0  # Set to black (0)

    return output_grid.tolist()