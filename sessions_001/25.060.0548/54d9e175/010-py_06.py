"""
Transforms the input grid by replacing non-zero and non-five values with specific colors in 3x3 blocks, while keeping the value 5 unchanged.
The first encountered non-zero, non-five value is replaced by orange (7), the second by azure (8), and the third by magenta (6).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Create a list to track the dynamic values found
    dynamic_values_found = []

    # Replace dynamic numbers with color blocks starting from 0,0.
    k=0
    for i in range(rows):
      for j in range(cols):
        if input_grid[i,j] != 0 and input_grid[i,j] != 5:
            if input_grid[i,j] not in dynamic_values_found:
                dynamic_values_found.append(input_grid[i,j])
                if len(dynamic_values_found) == 1:  # First dynamic value: replace with orange (7)
                    replacement_color = 7
                elif len(dynamic_values_found) == 2:  # Second dynamic value: replace with azure (8)
                    replacement_color = 8
                elif len(dynamic_values_found) == 3: # third dynamic value: replace with magenta(6)
                    replacement_color = 6

                output_grid[0:3, k:k+3] = replacement_color
                k+=4 # move k to next area
    
    # retain static '5' values from original grid
    for i in range(rows):
      for j in range(cols):
        if input_grid[i,j] == 5:
          output_grid[i,j] = 5

    return output_grid