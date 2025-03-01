"""
Extracts the top 3x3 sub-grid from the input. 
Then, in the extracted sub-grid, it changes the color maroon (9) to red (2) in the second column.
The rest of the pixels in the extracted subgrid become white (0).
"""

import numpy as np

def transform(input_grid):
    # Extract the top 3x3 sub-grid.
    sub_grid = input_grid[:3, :3]

    # Create an output grid initialized with white (0).
    output_grid = np.zeros_like(sub_grid)

    # Find the positions of maroon (9) pixels in the sub-grid.
    maroon_positions = np.where(sub_grid == 9)

    # Iterate through maroon positions and change them to red (2) in the output if they are in the center column.
    for r, c in zip(maroon_positions[0], maroon_positions[1]):
        if c == 1:
          output_grid[r,c] = 2
        else:
          output_grid[r,c] = 0

    # Fill any non-red cells with 0 in the center colum.
    for r in range(3):
      if output_grid[r,1] != 2:
        output_grid[r,1] = 0


    return output_grid