"""
1.  **Preservation:** Identify all yellow pixels. These pixels will remain unchanged in the output grid.

2.  **Azure Region Identification:** Locate all contiguous regions of azure pixels. A contiguous region is defined as a group of azure pixels that are directly adjacent (up, down, left, or right - not diagonal).

3.  **Bounding Box Filling**: For *each* identified azure region:
    - Determine the bounding box of that region. The bounding box is the smallest rectangle that encompasses all pixels in the region.
    - Iterate over every cell within that bounding box, changing the color to azure if it is not yellow.

4.  **Output:** The final output grid consists of the preserved yellow pixels and the filled azure bounding boxes, with any other pixels unchanged.
"""

import numpy as np
from scipy.ndimage import label

def get_bounding_box(grid):
    # Find coordinates of the non-zero pixels
    pixels = np.argwhere(grid)

    # If no pixels, return None
    if len(pixels) == 0:
        return None

    # Find min and max row and col
    min_row = np.min(pixels[:, 0])
    max_row = np.max(pixels[:, 0])
    min_col = np.min(pixels[:, 1])
    max_col = np.max(pixels[:, 1])

    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # identify yellow pixels - these will be preserved
    yellow_pixels = (input_grid == 4)

    # find contiguous regions of azure pixels
    azure_regions, num_regions = label(input_grid == 8)

    # iterate through each azure region
    for region_id in range(1, num_regions + 1):
        # get the region
        region_mask = (azure_regions == region_id)
        region_pixels = np.where(region_mask)
        region_grid = np.zeros_like(input_grid)
        region_grid[region_pixels] = 8 # Fill with azure to calculate bounding box
        
        # get bounding box of current region
        bounding_box = get_bounding_box(region_grid)

        if bounding_box:
            min_row, max_row, min_col, max_col = bounding_box
            # fill bounding box, preserving yellow
            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    if not yellow_pixels[row, col]:  # Check if NOT yellow
                        output_grid[row, col] = 8

    return output_grid