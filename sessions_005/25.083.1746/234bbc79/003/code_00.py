"""
Transforms an input grid based on vertical and horizontal color propagation rules,
triggered by the interaction of red, gray, and other colored pixels.
"""

import numpy as np

def get_vertical_groups(grid):
    """
    Groups vertically adjacent pixels of non-white colors.
    """
    groups = []
    for j in range(grid.shape[1]):
        current_group = []
        for i in range(grid.shape[0]):
            if grid[i, j] != 0:  # Non-white pixel
                current_group.append((i, j, grid[i, j]))
            else:
                if current_group:
                    groups.append(current_group)
                    current_group = []
        if current_group:  # Add any remaining group in the column
            groups.append(current_group)
    return groups

def get_horizontal_groups(grid):
    """
    Groups horizontally adjacent pixels of non-white colors.
    """
    groups = []
    for i in range(grid.shape[0]):
        current_group = []
        for j in range(grid.shape[1]):
            if grid[i,j] != 0:
                current_group.append((i,j, grid[i,j]))
            else:
                if current_group:
                    groups.append(current_group)
                    current_group = []
        if current_group:
            groups.append(current_group)

    return groups

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    # 1. Vertical Propagation
    vertical_groups = get_vertical_groups(input_grid)
    for group in vertical_groups:
        for i, (row, col, color) in enumerate(group):
            if color == 2:  # Red pixel
                gray_above = False
                trigger_pixel = None

                for i_above in range(i):
                    row_above, col_above, color_above = group[i_above]
                    if color_above == 5:  # Gray pixel above
                        gray_above = True
                        for i_trigger in range(i_above):
                            row_trigger, col_trigger, color_trigger = group[i_trigger]
                            if color_trigger not in [0, 2, 5]:  # Trigger pixel found
                                trigger_pixel = (row_trigger, col_trigger, color_trigger)
                                break
                        if trigger_pixel:
                          break #found trigger, don't check for other grey

                if gray_above and trigger_pixel:
                    output_grid[row, col] = trigger_pixel[2]  # Propagate color down
                    output_grid[trigger_pixel[0], trigger_pixel[1]] = 0 #clear trigger
                    #clear grey pixels
                    for i_clear in range(i):
                      row_clear, col_clear, color_clear = group[i_clear]
                      if(color_clear == 5):
                        output_grid[row_clear, col_clear] = 0
    
    #horizontal propagation
    horizontal_groups = get_horizontal_groups(output_grid)
    grey_group_indices = []
    color_group_indices = []

    for i, group in enumerate(horizontal_groups):
      has_grey = False
      has_color = False
      for row, col, color in group:
        if color == 5:
          has_grey = True
        elif color != 0 and color != 2:
          has_color = True

      if has_grey and not has_color:
        grey_group_indices.append(i)
      if has_color:
        color_group_indices.append(i)
      
    if len(grey_group_indices) > 0 and len(color_group_indices) > 0:
      for color_index in color_group_indices:
        colored_pixels = horizontal_groups[color_index]
        for row, col, color in colored_pixels:
            output_grid[row,col] = color #copy color pixels
        for i in range(output_grid.shape[0]):
          for j in range(output_grid.shape[1]):
            if output_grid[i,j] == 2:
              output_grid[i,j] = colored_pixels[0][2] # use first color
    
    return output_grid