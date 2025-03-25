"""
1. **Identify the Target Color:** Find the single non-zero color (pixel value) present in the input grid.
2. **Locate Color positions on top and side:**
    - find instances of the color on the top row.
    - find instances of the color on the leftmost column.
3. **Determine output dimensions**: Determine the number of instances of the color on the top row and left columns
4. **Construct the Output Grid:** Create a new grid. If count from top row is N and count from left is M:
    * If both M and N are zero, do not create any grid
    * if M = 0, the output grid dimensions is  N x N and fill it with the target color.
    * if N = 0, the output grid dimensions is M x M and fill it with the target color.
    * if neither M nor N = 0, the output grid dimension is N x M and fill it with the target color
"""

import numpy as np

def get_target_color(grid):
    # Find the unique non-zero color in the grid
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    return 0

def count_top_side(grid, target_color):
    # Count target color along top and side
    top_count = 0
    for x in grid[0]:
        if x == target_color:
            top_count+=1
    
    side_count = 0
    for row in grid:
       if row[0] == target_color:
           side_count += 1
    return top_count, side_count

def transform(input_grid):
    # initialize output_grid

    # Find the target (non-zero) color
    target_color = get_target_color(input_grid)

    if target_color == 0:
        return []
       
    top_count, side_count = count_top_side(input_grid, target_color)
    
    # Determine output dimensions
    if top_count == 0 and side_count == 0:
        width = 0
        height = 0
    elif top_count == 0:
        width = side_count
        height = side_count
    elif side_count == 0:
        width = top_count
        height = top_count
    else:
        width = top_count
        height = side_count
        
    # Construct the output grid and fill with the target color
    output_grid = np.full((height, width), target_color)


    return output_grid