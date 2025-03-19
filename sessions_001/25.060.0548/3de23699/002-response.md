# 3de23699 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule identifies two distinct non-zero colors in the input grid. It selects one of these colors (the first one encountered when reading left-to-right, top-to-bottom) as the target color.  It then finds all instances of the *other* color and uses those locations to place 2x2 blocks of the target color pixels in the output grid.
"""

import numpy as np

def find_target_colors(grid):
    """Finds the two distinct non-zero colors in the grid."""
    unique_colors = np.unique(grid)
    non_zero_colors = unique_colors[unique_colors != 0]
    # return both non-zero colors
    return non_zero_colors[0], non_zero_colors[1] if len(non_zero_colors) > 1 else (non_zero_colors[0], non_zero_colors[0])

def find_color_instances(grid, color):
    """Finds all instances of a specific color in the grid."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)
    
    # 1. Identify Target Colors
    target_color, other_color = find_target_colors(input_grid)
        
    # 2. find instances of other_color
    other_color_instances = find_color_instances(input_grid, other_color)

    # find instances of the target_color
    target_color_instances = find_color_instances(input_grid, target_color)

    # 3. Create Output Grid
    if (len(other_color_instances) > 0):
        # find the bounding box that will fit all other_color
        min_row = other_color_instances[:, 0].min()
        max_row = other_color_instances[:, 0].max()
        min_col = other_color_instances[:, 1].min()
        max_col = other_color_instances[:, 1].max()

        output_height = (max_row - min_row + 1) * 2
        output_width = (max_col - min_col + 1) * 2

        output_grid = np.zeros((output_height, output_width), dtype=int)
    
       # 4. Populate Output Grid
        for instance in other_color_instances:
            row_offset = (instance[0] - min_row) * 2
            col_offset = (instance[1] - min_col) * 2
            
            output_grid[row_offset:row_offset+2, col_offset:col_offset+2] = target_color
    else:
        # special handling if no "other_color" is found
        # find target color location
        # create a 2x2 output from that location
       min_row = target_color_instances[:, 0].min()
       max_row = target_color_instances[:, 0].max()
       min_col = target_color_instances[:, 1].min()
       max_col = target_color_instances[:, 1].max()

       output_height = (max_row - min_row + 1) * 2
       output_width = (max_col - min_col + 1) * 2
    
       output_grid = np.zeros((output_height, output_width), dtype=int)


       for instance in target_color_instances:
           row_offset = (instance[0] - min_row) * 2
           col_offset = (instance[1] - min_col) * 2

           output_grid[row_offset:row_offset + 2, col_offset:col_offset + 2] = target_color
    
    return output_grid.tolist()
```
