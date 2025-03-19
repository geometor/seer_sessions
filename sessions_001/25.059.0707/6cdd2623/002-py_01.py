"""
1.  **Identify the Target Color:** Examine the input grid and determine the "target color".
    - In example 1, the target color is 3 (green).
    - In example 2, the target color is 2 (red).
    - In example 3, the target color is 8 (azure).

2. **Overwrite with target color** Using the target color, draw lines on the grid to create a specific pattern
      - overwrite the entire row that contains the target color in the input, filling it with the target color
      - overwrite the entire column where the target color first appears, filling it with the target color.
3. Maintain the zeros: Ensure any cells that are 0 in input remain 0 in the output grid.

In Summary, find a special color in the input, use its first appearance row/col coordinates to completely fill in the respective row and column with that color, and maintain 0 values.
"""

import numpy as np

def find_target_color(grid):
    # Find unique colors in the grid, excluding 0
    unique_colors = np.unique(grid)
    unique_colors = unique_colors[unique_colors != 0]

    #For this problem the target color seems to be the last color in the
    #shortened unique color array
    if len(unique_colors) > 0:
        return unique_colors[-1]
    else:
      return 0
    

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    target_color = find_target_color(input_grid)
    
    if target_color == 0:
       return output_grid.tolist()

    # Find the first occurrence of the target color
    first_occurrence = np.where(input_grid == target_color)
    if len(first_occurrence[0]) > 0:
      first_row = first_occurrence[0][0]
      first_col = first_occurrence[1][0]

      # change output pixels 

      # Fill the row
      output_grid[first_row, :] = target_color
      # Fill the column
      output_grid[:, first_col] = target_color

      #reset 0 cells
      output_grid = np.where(input_grid == 0, 0, output_grid)
    
    return output_grid.tolist()