"""
1. Identify the layers: Recognize the different colored regions in the input grid: the outer green border, the red inner square, and the central white square.
2. Remove the center: Eliminate the central white square (color 0).
3. Shift Inwards: Move the colors from surrounding to the place previous occupied by the central white square.
4. Blank the perimeter: Set all pixels on the grid's outermost border to white (0).
"""

import numpy as np

def get_layer(grid, color):
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Get layers
    green_layer = get_layer(input_grid, 3)
    red_layer = get_layer(input_grid, 2)
    #white_layer = get_layer(input_grid, 0) #Not needed, we remove

    # Find Center to fill:
    center_coords = np.argwhere(input_grid == 0)
        
    # Shift inwards - move red to position of former white
    for coord in center_coords:
        output_grid[coord[0], coord[1]] = input_grid[coord[0]-1,coord[1]]  if input_grid[coord[0]-1, coord[1]] != 0 else input_grid[coord[0] + 1, coord[1] ]

    # Blank the perimeter.
    rows, cols = output_grid.shape
    for i in range(rows):
        for j in range(cols):
          if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                output_grid[i,j] = 0
          

    return output_grid