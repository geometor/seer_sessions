"""
Transforms an input grid based on the interaction between red (2), gray (5) and other colored pixels.
Other colored pixels (not 0, 2, or 5) vertically above red pixels, propagate their value downwards, replacing the red, 
mediated by the position and existence of gray pixels.
"""

import numpy as np

def get_pixel_groups(grid):
    """
    Groups vertically adjacent pixels.
    """
    groups = []
    for j in range(grid.shape[1]):
        current_group = []
        for i in range(grid.shape[0]):
            if grid[i, j] != 0:  # Consider non-black pixels
                current_group.append((i, j, grid[i, j]))
            else:
                if current_group:
                    groups.append(current_group)
                    current_group = []
        if current_group:  # Add any remaining group in the column
            groups.append(current_group)
    return groups

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    pixel_groups = get_pixel_groups(input_grid)

    for group in pixel_groups:
        for i, (row, col, color) in enumerate(group):
            if color == 2:  # Red pixel found
                trigger_gray_above = False
                other_color_above_gray = None
                
                #Look for vertically adjacent gray
                for i_above in range(i):
                  row_above, col_above, color_above = group[i_above]
                  if(color_above == 5):
                    trigger_gray_above = True
                    
                    #look for other color pixel
                    for i_other in range(i_above):
                      row_other, col_other, color_other = group[i_other]
                      if color_other != 0 and color_other !=2 and color_other !=5:
                        other_color_above_gray = color_other
                        other_color_row = row_other
                        other_color_col = col_other
                        break

                  if trigger_gray_above:
                    break
                
                if trigger_gray_above and other_color_above_gray != None:
                  output_grid[row,col] = other_color_above_gray
                  output_grid[other_color_row, other_color_col] = 0

                  #clear grey - note, this needs to be generalized, not just 1 pixel
                  output_grid[row_above, col_above] = 0
                    
    return output_grid