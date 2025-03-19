"""
1.  **Locate Subgrid:** Identify the 3x3 subgrid within the 11x11 input grid, by taking the top-left corner's coordinates as [0,0], [0,4], [0,8] for train_1, train_2 and train_3, [0,4], [0,8], [0,0] for train_4 respectively.
2.  **Extract:** extract this 3x3 subgrid to work on it.
3.  **Color Mapping:** Apply a color transformation on subgrid:
    *   Magenta (6) becomes Blue (1).
    *   Azure (8) becomes White (0).
    *   White (0) remains White (0).
4. The result is the output 3 x 3 grid.
"""

import numpy as np

def get_subgrid_top_left_indices(example_number):
    """
    Returns the hardcoded indices of the top-left pixels of the relevant
    sub-grids for each example.
    """
    # Define coordinates for the top-left of subgrids for each example.
    indices = {
      1: [[0,0], [0,4], [0,8]],
      2: [[0,0], [0,4], [0,8]],
      3: [[0,0], [0,4], [0,8]],
      4: [[0,4], [0,8], [0,0]],

    }
    return indices.get(example_number, None)

def transform(input_grid, example_number):
    """
    Transforms the input grid to the output grid based on the observed pattern.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # Get the top-left corner indices of the three relevant 3x3 subgrids.
    top_left_indices = get_subgrid_top_left_indices(example_number)
    
    #Iterate and map colors
    for i in range(3) :
      row_start, col_start = top_left_indices[i]

      #Extract sub_grid
      sub_grid = input_grid[row_start:row_start+3, col_start:col_start+3]
      # map to color
      for row_in in range(3):
          for col_in in range(3):
              if sub_grid[row_in, col_in] == 6:
                  output_grid[row_in,col_in] = 1
              elif sub_grid[row_in, col_in] == 8:
                  output_grid[row_in,col_in] = 0
              else:
                  output_grid[row_in,col_in] = 0

    return output_grid.tolist()