"""
Transforms a 3x3 input grid containing 0s and 5s to a 3x3 output grid based on the positions of the 5s.

1. Initialization: Create a copy of the input grid to modify.
2. Color Mapping:
   - If a cell contains '0', replace it with specific value based on the postion of 5.
   - If a cell contains '5', replace it based on pre-defined spatial rules.
3. Output: Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the location of 5s.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Helper function to find the positions of 5s
    def find_fives(grid):
        fives_positions = []
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == 5:
                    fives_positions.append((r, c))
        return fives_positions

    fives = find_fives(input_grid)
    
    # Determine the pattern and apply transformations
    if all(pos[1] == 2 for pos in fives):  # All 5s on the right
        output_grid[:] = 3
    elif all(pos[1] == 0 for pos in fives): # All 5s on the left side
         for r in range(rows):
            for c in range(cols):
                if output_grid[r,c] == 5:
                    if r==0 or r==2:
                        output_grid[r,c]=2
                    elif r==1:
                        output_grid[r,c]=4
                if output_grid[r,c] == 0:
                    output_grid[r,c] = 2


    elif (0, 0) in fives and (2, 0) in fives and (1,1) in fives: # 5s in top-left, bottom-left, and center
        for r in range(rows):
            for c in range(cols):
                if output_grid[r,c] == 5:
                    if r==0 or r==2:
                        output_grid[r,c]=2
                    elif r==1:
                        output_grid[r,c]=4
                if output_grid[r,c] == 0:
                    output_grid[r,c] = 4
    elif (0, 1) in fives and (1, 2) in fives and (2,1) in fives: # 5s forming an 'L' in the top-center, middle-right and bottom-center
        for r in range(rows):
            for c in range(cols):
                if output_grid[r,c] == 5:
                    if r==0 or r==2:
                        output_grid[r,c]=4
                    elif r==1:
                        output_grid[r,c]=3
                if output_grid[r,c] == 0:
                    output_grid[r,c] = 4

    else:   # if it doesn't fall into any of the cases, change '0' into '4'
        for r in range(rows):
          for c in range(cols):
            if output_grid[r,c] == 0:
                output_grid[r,c] = 3
    
    return output_grid