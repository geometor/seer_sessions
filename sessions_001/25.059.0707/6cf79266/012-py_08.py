"""
1. Identify the Target Region: Find the largest contiguous region of a single color within the input grid, *excluding* black (0) and blue (1). If multiple regions of the same size, select the region that is closest to the top-left.
2. Determine the dimensions: Determine the height and width of the target region.
3. Replace with Blue: Replace all pixels within the identified region with blue pixels (color code 1).
4. Copy Unchanged Pixels: All other pixels in the input grid should be copied to the output grid without modification.
"""

import numpy as np
from scipy.ndimage import measurements

def find_largest_region(grid, exclude_colors=[0, 1]):
    """
    Finds the largest contiguous region of a single color in the grid,
    excluding specified colors.
    """
    max_size = 0
    max_region = None
    max_label = -1

    for color in np.unique(grid):
        if color in exclude_colors:
            continue

        # Create a binary mask for the current color
        binary_mask = (grid == color)

        # Find connected components (regions)
        labeled_array, num_features = measurements.label(binary_mask)

        if num_features == 0:
            continue

        # Calculate the size of each region
        sizes = measurements.sum(binary_mask, labeled_array, range(1, num_features + 1))

        # Find the largest region for the current color
        largest_region_index = np.argmax(sizes)
        largest_region_size = sizes[largest_region_index]

        if largest_region_size > max_size:
            max_size = largest_region_size
            max_region = (labeled_array == (largest_region_index + 1))  # +1 because labels start at 1
            max_label = color


    return max_region, max_label

def get_region_dimensions(region_mask):
    """
    Calculates the dimensions (height, width) and top-left corner of a region.
    """
    rows, cols = np.where(region_mask)
    if rows.size == 0:
        return 0, 0, 0, 0 # handle no region case
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return height, width, min_row, min_col

def transform(input_grid):
    """
    Transforms the input grid by replacing the largest contiguous region
    (excluding black and blue) with blue pixels.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the largest region and its color
    largest_region_mask, region_color = find_largest_region(input_grid)

    if largest_region_mask is not None:
      # Get the region dimensions and location
      height, width, row_start, col_start = get_region_dimensions(largest_region_mask)

      # Replace the identified region with blue (1)
      output_grid[row_start:row_start + height, col_start:col_start + width] = 1

    return output_grid