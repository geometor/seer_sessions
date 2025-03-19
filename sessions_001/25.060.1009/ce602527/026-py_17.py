"""
1.  Locate Green Pixel: Scan the input grid to find a green pixel (color 3). If no green pixel is found, the transformation might result in an empty output (although this isn't explicitly tested in the provided examples). If multiple green pixels exist, use only the first encountered (using standard NumPy indexing, row-major order).
2.  Extract Vertical Segment: Starting from the location of the identified green pixel, extract a vertical segment by moving downwards in the same column. Include the starting green pixel and all contiguous blue pixels (color 1) directly below it. Stop when a non-blue pixel or the bottom edge of the grid is encountered.
3. Construct the output: Construct an output that only includes the found vertical segment.
"""

import numpy as np

def find_green_pixel(grid):
    # Find coordinates of the green pixel (color 3).
    coords = np.argwhere(grid == 3)
    if coords.size == 0:
        return None  # Green pixel not found
    elif coords.shape[0] > 1:
        return None # More than one green pixel
    return coords[0]

def extract_vertical_segment(grid, start_row, col):
    # Extract a vertical segment downwards from (start_row, col).
    segment = []
    row = start_row
    while row < grid.shape[0] and (grid[row, col] == 3 or grid[row, col] == 1):
        segment.append(grid[row, col])
        row += 1
    return segment

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # 1. Find the Green Pixel
    green_pixel_coords = find_green_pixel(input_grid)
    if green_pixel_coords is None:
      return []

    row, col = green_pixel_coords

    # 2. Extract Vertical Segment
    vertical_segment = extract_vertical_segment(input_grid, row, col)

    # 3. Construct Output
    height = len(vertical_segment)
    output_grid = np.zeros((height, 1), dtype=int)  # Initialize with white background (0)
    for i, value in enumerate(vertical_segment):
        output_grid[i, 0] = value

    return output_grid.tolist()