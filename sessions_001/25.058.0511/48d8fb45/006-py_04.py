"""
Identify the Blue Object: Find the contiguous block of blue (1) pixels that form a rectangular shape in the input grid.
Extract the Rectangle: Extract the identified blue rectangle. The output grid should be the same size as this rectangle and contain *only* the blue pixels, maintaining their relative positions within the rectangle. All other pixels in the original image are discarded.
"""

import numpy as np

def find_blue_rectangle(grid):
    # Find the top-left and bottom-right coordinates of the blue rectangle.
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:
        return None  # No blue pixels found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounding box of the blue rectangle.
    bounding_box = find_blue_rectangle(input_grid)
    if bounding_box is None:
        return np.array([[]]) # return empty array if no blue

    min_row, max_row, min_col, max_col = bounding_box

    # Extract the rectangle.
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    # ensure that the shape found is a rectangle
    if np.all(output_grid==1):
        return output_grid
    else:
        return np.array([[]])
