"""
Identify a vertical green line and a horizontal red line intersecting it.
Remove the green pixels from the horizontal line where it intersects the vertical line, keeping the red pixels.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find the column index of the vertical line of the specified color.
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                # Check if this is part of a vertical line
                if i + 1 < rows and grid[i+1, j] == color:
                    return j
    return -1

def find_horizontal_line(grid, color):
    # Find the row index of the horizontal line of the specified color.
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == color:
                # Check if part of horizontal line
                if j + 1 < cols and grid[i,j+1] == color:
                    return i
                
    return -1

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Find the vertical green line.
    green_col = find_vertical_line(input_grid, 3)
    
    # Find the horizontal red line.
    red_row = find_horizontal_line(input_grid, 2)
    
    if green_col != -1 and red_row != -1:
        # Iterate through the horizontal line and apply the change.
      for j in range(cols):
            if output_grid[red_row,j] == 3:
                output_grid[red_row,j] = 0
                

    return output_grid