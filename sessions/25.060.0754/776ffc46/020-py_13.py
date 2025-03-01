"""
Identifies a color swap rule from the input and output grids and applies it. It copies the input grid and then changes the colors of objects according to the identified color swap.
"""

import numpy as np

def find_color_swap(input_grid, output_grid):
    # Find the color swap rule by comparing input and output grids.
    changed_colors_in = set()
    changed_colors_out = set()

    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r,c] != output_grid[r,c]:
                changed_colors_in.add(input_grid[r,c])
                changed_colors_out.add(output_grid[r,c])

    if len(changed_colors_in) == 1 and len(changed_colors_out) == 1:
        return list(changed_colors_in)[0], list(changed_colors_out)[0]
    else:
        return None, None  # No consistent color swap found

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the color swap rule
    input_color, output_color = find_color_swap(input_grid, output_grid) # added output_grid
    
    if input_color is not None and output_color is not None: # check before the loop
      # Apply the color swap
      for r in range(output_grid.shape[0]):
          for c in range(output_grid.shape[1]):
              if output_grid[r, c] == input_color:
                  output_grid[r, c] = output_color

    return output_grid