"""
Identifies an "L" shape in the input grid, extends it to form a rectangle, 
filling the newly occupied space with a color determined by the input's top-right cell,
and "connecting" the gap created by the "L" extension with the corner color.
"""

import numpy as np

def find_l_shape(grid):
    # Find the contiguous non-zero pixels forming an "L" shape.
    rows, cols = grid.shape
    non_zero_indices = np.argwhere(grid != 0)
    if len(non_zero_indices) < 2:
        return None, None, None

    # Find top-right element
    top_right = grid[0, cols-1]

    # Determine corner and orientation
    first = non_zero_indices[0]
    last = non_zero_indices[-1]

    if first[0] == last[0]:  # Horizontal L
        corner_row, corner_col = first[0], last[1]
        corner_color = grid[corner_row, corner_col]
        orientation = 'horizontal'
        
    elif first[1] == last[1]:  # Vertical L
        corner_row, corner_col = last[0], first[1]
        corner_color = grid[corner_row, corner_col]
        orientation = 'vertical'
    else:
        # check if its 2 points creating a diagonal
        if(len(non_zero_indices)==2):
            if first[1] < last[1]:
                 corner_row, corner_col = first[0],last[1]
            else:
                corner_row, corner_col = last[0],first[1]
           
            corner_color = grid[corner_row, corner_col]
            orientation = 'horizontal'

        else:
            return None, None, None # Not a clear L
    
    return (corner_row, corner_col), corner_color, orientation, top_right


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Find the L shape and its properties.
    l_shape_info = find_l_shape(input_grid)
    if l_shape_info is None:
        return output_grid  # No L shape found, return original grid

    corner, corner_color, orientation, extension_color = l_shape_info

    # Extend the "L" and fill.
    if orientation == 'horizontal':
        # Extend downwards
        for i in range(corner[0] + 1, rows):
            for j in range(0, corner[1] + 1):
                if j < corner[1]:
                  output_grid[i, j] = output_grid[corner[0],j] # fill same color as top row of "L" until hitting corner column
                else:
                  output_grid[i,j] = extension_color # use extension_color for corner and beyond
            
        output_grid[0,cols-1] = extension_color

    elif orientation == 'vertical':
        # Extend rightwards
        for i in range(corner[0], rows):
           for j in range(corner[1] + 1, cols):
                if i > corner[0]:
                    output_grid[i, j] = output_grid[i,0] # fill from "L" column
                else:
                    output_grid[i,j] = extension_color
        output_grid[0,cols-1] = extension_color
    
      

    return output_grid