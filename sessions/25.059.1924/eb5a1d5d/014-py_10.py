"""
1.  Determine Input Grid:** Examine the input grid.
2.  Identify Unique Colors:** Find all unique colors present in the input grid.
3. Output Grid:**
  - If the input grid contains only one unique color, and the grid shape is not 9x9, the output grid is a copy of the input grid.
  - If the input contains only one unique color, and the grid shape is 9x9, make a 3x3 grid.  Set the background of the output grid to black (0). Set the center pixel of the output grid to the color from the input grid.
4. **Return:** The output is the modified grid, according to the rules above.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Grid: Examine the input grid.
    input_grid = np.array(input_grid)
    
    # Identify Unique Colors: Find all unique colors present in the input grid.
    unique_colors = np.unique(input_grid)

    # Output Grid
    if len(unique_colors) == 1:
        # If the input grid contains only one unique color, and the grid shape is not 9x9, the output grid is a copy of the input grid.
        if input_grid.shape != (9, 9):
            output_grid = np.copy(input_grid)
        # If the input contains only one unique color, and the grid shape is 9x9, make a 3x3 grid.
        else:
          #Set the background of the output grid to black (0). 
          output_grid = np.zeros((3, 3), dtype=int)
          #Set the center pixel of the output grid to the color from the input grid.
          output_grid[1,1] = unique_colors[0]  
    
    # Return: The output is the modified grid, according to the rules above.
    return output_grid