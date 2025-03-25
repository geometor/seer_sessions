```python
"""
The input grid is divided into two sections.  The height and width ratios
between input and output grids are calculated. A source subgrid is taken
from the top-left of each section, and then expanded based on the height and
width ratio to form two sections of the final output grid.
"""

import numpy as np

def expand_subgrid(subgrid, height_ratio, width_ratio):
    # Calculate dimensions of the expanded subgrid
    expanded_height = int(subgrid.shape[0] * height_ratio)
    expanded_width = int(subgrid.shape[1] * width_ratio)
    expanded_subgrid = np.zeros((expanded_height, expanded_width), dtype=int)

    # Fill the expanded subgrid
    for row in range(expanded_height):
        for col in range(expanded_width):
            original_row = int(row // height_ratio)
            original_col = int(col // width_ratio)
            expanded_subgrid[row, col] = subgrid[original_row, original_col]

    return expanded_subgrid

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Determine height and width ratios, swap if needed
    # Example 1: 6x4 -> 12x12 (2,3), Example 2: 4x6 -> 12x12 (3,2)
    if input_height > input_width:
        height_ratio = 2.0
        width_ratio = 3.0
        output_grid = np.zeros((int(input_height * height_ratio), int(input_width * width_ratio)),dtype=int)

        # Divide input into top and bottom sections
        top_section = input_grid[:input_height // 2, :]
        bottom_section = input_grid[input_height // 2:, :]

        # Define top-left subgrids
        top_left_subgrid = top_section[: , :input_width]
        bottom_left_subgrid = bottom_section[: , :input_width]
        
        # Expand subgrids
        expanded_top = expand_subgrid(top_left_subgrid, height_ratio, width_ratio)
        expanded_bottom = expand_subgrid(bottom_left_subgrid, height_ratio, width_ratio)

        # Fill output grid
        output_grid[:expanded_top.shape[0], :] = expanded_top
        output_grid[expanded_top.shape[0]:, :] = expanded_bottom
    
    else:
        height_ratio = 3.0
        width_ratio = 2.0
        output_grid = np.zeros((int(input_height * height_ratio), int(input_width * width_ratio)),dtype=int)

        # Divide input into left and right sections
        left_section = input_grid[:, :input_width // 2]
        right_section = input_grid[:, input_width // 2:]

        # Define top-left subgrids
        top_left_subgrid = left_section[:left_section.shape[0], :]
        bottom_left_subgrid = right_section[:right_section.shape[0], :]
        
        # Expand subgrids
        expanded_top = expand_subgrid(top_left_subgrid, height_ratio, width_ratio)
        expanded_bottom = expand_subgrid(bottom_left_subgrid, height_ratio, width_ratio)
        
        # Fill output grid
        output_grid[:expanded_top.shape[0], :] = expanded_top
        output_grid[expanded_top.shape[0]:, :] = expanded_bottom


    return output_grid
```