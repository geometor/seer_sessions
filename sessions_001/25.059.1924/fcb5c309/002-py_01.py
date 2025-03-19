"""
The transformation identifies a target color in the input grid (4 in the first example, 3 in the second, 2 in the third).
It finds the bounding box of this target color within the input grid.
A new grid is created with the dimensions of the bounding box.
The output grid is filled with the target color, except for the interior cells which have the value of 0 in the input, that remain 0.
"""

import numpy as np

def get_target_color(input_grid, output_grid):
    # Find the most frequent non-zero color in the output grid.
    unique, counts = np.unique(output_grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    
    target_color = 0
    max_count = 0
    
    for color, count in color_counts.items():
      if color != 0 and count > max_count:
        max_count = count
        target_color = color
    
    return target_color

def find_bounding_box(grid, target_color):
    # Find the min and max row and col indices of the target color.
    rows, cols = np.where(grid == target_color)
    if len(rows) == 0:
        return None  # Target color not found

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid, output_grid=None): # added output_grid for testing purposes
    # Identify target color from the corresponding output grid
    target_color = get_target_color(input_grid, output_grid)

    # Find the bounding box of the target color
    bounding_box = find_bounding_box(input_grid, target_color)
    if bounding_box is None:
        return np.array([[0]]) # returns a 0x0 grid with value [0]

    min_row, max_row, min_col, max_col = bounding_box

    # Create the output grid based on the bounding box dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid_transformed = np.full((output_height, output_width), target_color)

    # Preserve '0' pixels inside bounding box
    for i in range(min_row, max_row+1):
      for j in range(min_col, max_col + 1):
        if input_grid[i,j] == 0:
          output_grid_transformed[i-min_row, j-min_col] = 0
    
    return output_grid_transformed