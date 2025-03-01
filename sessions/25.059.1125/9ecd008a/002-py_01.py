"""
Transforms a large input grid with a central white cross into a 3x3 output grid.
The output grid's colors are determined by sampling colors from specific locations
within the input grid, relative to the central cross.
"""

import numpy as np

def get_center(input_grid):
    # Find the center coordinates of the input grid.
    rows, cols = input_grid.shape
    center_row = rows // 2
    center_col = cols // 2
    return center_row, center_col

def get_representative_color(input_grid, region, center_row, center_col):
    # Get the representative color for a given region of the input grid.
    rows, cols = input_grid.shape

    if region == "top-left":
        for r in range(center_row):
            if input_grid[r,center_col] != 0:
                return input_grid[r, center_col]
    elif region == "top-center":
        for r in range(center_row):
            if input_grid[r,center_col] != 0:
                return input_grid[r, center_col]            
    elif region == "top-right":
        for r in range(center_row):
            if input_grid[r,center_col] != 0:
                return input_grid[r, center_col] 
    elif region == "middle-left":
        for c in range(center_col):
           if input_grid[center_row, c] != 0:
               return input_grid[center_row, c]
    elif region == "middle-center":
        for c in range(center_col):
           if input_grid[center_row, c] != 0:
               return input_grid[center_row, c] # Will overwrite, effectively taking left-most
    elif region == "middle-right":
        for c in range(center_col + 1, cols):
            if input_grid[center_row, c] != 0:
                return input_grid[center_row, c]
    elif region == "bottom-left":
        for r in range(center_row + 1, rows):
            if input_grid[r, center_col] != 0:
                return input_grid[r, center_col]
    elif region == "bottom-center":
        for r in range(center_row + 1, rows):
            if input_grid[r, center_col] != 0:
                return input_grid[r, center_col]
    elif region == "bottom-right":
        for r in range(center_row + 1, rows):
            if input_grid[r, center_col] != 0:
                return input_grid[r, center_col]

    return 0  # Default to 0 if no color is found


def transform(input_grid):
    """
    Transforms the input grid into a 3x3 output grid based on the central cross.
    """
    # Initialize the 3x3 output grid.
    output_grid = np.zeros((3, 3), dtype=int)

    # Get the center coordinates of the input grid.
    center_row, center_col = get_center(input_grid)

    # Define the regions.
    regions = [
        "top-left", "top-center", "top-right",
        "middle-left", "middle-center", "middle-right",
        "bottom-left", "bottom-center", "bottom-right"
    ]

    # Populate the output grid.
    row_idx = 0
    col_idx = 0
    for region in regions:
        color = get_representative_color(input_grid, region, center_row, center_col)
        output_grid[row_idx, col_idx] = color
        col_idx += 1
        if col_idx == 3:
            col_idx = 0
            row_idx += 1

    return output_grid