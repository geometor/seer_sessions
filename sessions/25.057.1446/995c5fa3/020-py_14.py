"""
Transforms a 14x4 input grid containing a 'cross-like' shape made of white (0) pixels within a gray (5) background into a 3x3 output grid. The output grid represents the cross with yellow (4) pixels for the center and red (2) pixels for the arms.
"""

import numpy as np

def get_region(input_grid, row_index, col_index):
    """Divides the input grid into 9 regions and returns one based on row/col index."""
    rows, cols = input_grid.shape
    region_height = rows // 3
    region_width = cols // 3

    row_start = row_index * region_height
    col_start = col_index * region_width

    # Adjust for the remaining rows and cols that don't perfectly divide
    row_end = row_start + region_height + (rows % 3 if row_index == 2 else 0)
    col_end = col_start + region_width + (cols % 3 if col_index == 2 else 0)

    return input_grid[row_start:row_end, col_start:col_end]
    

def has_vertical_bar(region):
    """Checks if a region contains a part of the central vertical bar of the cross, unbroken."""
    rows, _ = region.shape
    for col in range(region.shape[1]):
        white_count = 0
        for row in range(rows):
          if region[row, col] == 0:
            white_count += 1
        if white_count == rows:
            return True
    return False

def has_horizontal_bar(region):
    """Checks if region has white pixels and might be part of horizontal bar."""
    return np.any(region == 0)


def transform(input_grid):
    """Transforms the input grid into a 3x3 output grid based on cross shape."""
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize a 3x3 output grid with zeros

    for row_index in range(3):
        for col_index in range(3):
            region = get_region(input_grid, row_index, col_index)

            if has_vertical_bar(region):
                output_grid[row_index, col_index] = 4  # Yellow for center
            elif has_horizontal_bar(region):
              output_grid[row_index, col_index] = 2  # red for horizontal part
            # if no part, region remains white

    return output_grid