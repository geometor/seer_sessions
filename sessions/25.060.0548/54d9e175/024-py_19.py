"""
1.  **Background:** Initialize the output grid with a white background.
2.  **Gray Line:** Copy the horizontal gray line at row index 3 from the input grid to the output grid.
3.  **Identify Regions:** Find all connected regions (contiguous blocks of pixels) of the same color in the input grid, *excluding* gray and white pixels.
4.  **Transform Regions:** For each identified region:
    *   Find its bounding box (the smallest rectangle containing all pixels of the region).
    *   Determine the output color based on the region's color: blue becomes azure, red becomes maroon, green becomes orange, yellow becomes magenta.
    *   In the output grid, replace the entire bounding box area with the corresponding output color.
5. **Output:** Return the modified output grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects

COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

OUTPUT_COLOR_MAPPING = {
    1: 8,  # blue -> azure
    2: 9,  # red -> maroon
    3: 7,  # green -> orange
    4: 6,  # yellow -> magenta
}

def get_connected_regions(grid):
    """
    Finds connected regions (blobs) of the same color, excluding gray and white.
    Returns a list of bounding box tuples: (row_start, row_end, col_start, col_end, color)
    """
    # Create a mask for non-gray and non-white pixels
    filtered_grid = np.where((grid != 5) & (grid != 0), grid, 0)
    # Label connected regions in the filtered grid
    labeled_grid, num_labels = label(filtered_grid)
    # Find the bounding boxes of the labeled regions
    regions = find_objects(labeled_grid)

    region_data = []
    for i, region_slice in enumerate(regions):
        if region_slice is not None:
            # Extract bounding box coordinates
            row_start, row_end = region_slice[0].start, region_slice[0].stop
            col_start, col_end = region_slice[1].start, region_slice[1].stop
            # Extract a representative color from the region (assuming homogeneity)
            color = grid[row_start, col_start]
            region_data.append((row_start, row_end, col_start, col_end, color))

    return region_data

def transform(input_grid):
    # Initialize output_grid with white background
    output_grid = np.full_like(input_grid, 0)

    # Preserve the gray line
    output_grid[3, :] = input_grid[3, :]

    # Get connected regions
    regions = get_connected_regions(input_grid)

    # Transform each region
    for row_start, row_end, col_start, col_end, color in regions:
        output_color = OUTPUT_COLOR_MAPPING.get(color)
        if output_color:
            # Fill the bounding box with the transformed color
            output_grid[row_start:row_end, col_start:col_end] = output_color

    return output_grid