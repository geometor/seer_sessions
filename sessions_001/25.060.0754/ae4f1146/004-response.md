# ae4f1146 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation extracts azure (8) and blue (1) pixels from the input grid, discarding white (0) pixels, and creates a condensed 3x3 output grid preserving the relative positions of the extracted pixels.
"""

import numpy as np

def find_seed_pixel(grid, colors):
    # Find first instance of one of the target color pixels, starting at top left.
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel in colors:
                return (r, c)
    return None

def get_value_at_scaled_position(grid, row_scale, col_scale, start_row, start_col):
    # Calculate scaled indices
    scaled_row = int(start_row + row_scale)
    scaled_col = int(start_col + col_scale)
    
    # Check bounds - if outside the input grid, return a default value (e.g., 0)
    if 0 <= scaled_row < grid.shape[0] and 0 <= scaled_col < grid.shape[1]:
        return grid[scaled_row, scaled_col]
    else:
        return 0

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)
    target_colors = [1, 8]

    # Find a seed pixel (starting point)
    seed = find_seed_pixel(input_grid, target_colors)
    if seed is None:
        return output_grid # Return empty grid if no target colors found

    start_row, start_col = seed

    row_scale = (input_grid.shape[0]-1) /2
    col_scale = (input_grid.shape[1] -1) /2

    # Populate the output grid
    for i in range(3):
        for j in range(3):
            scaled_row = start_row + (i-1)*row_scale
            scaled_col = start_col + (j-1)*col_scale
            
            
            if scaled_row<0:
              scaled_row=0
            if scaled_col<0:
              scaled_col = 0
              
            if scaled_row>=input_grid.shape[0]:
              scaled_row=input_grid.shape[0]-1
            if scaled_col>=input_grid.shape[1]:
              scaled_col = input_grid.shape[1]-1
            
            pixel = input_grid[int(scaled_row), int(scaled_col)]
            
            if pixel in target_colors:
              output_grid[i,j]=pixel
            else:
              for r_off in range(-1,2):
                for c_off in range(-1,2):
                   n_row = int(scaled_row) + r_off
                   n_col = int(scaled_col) + c_off
                   if n_row<0:
                      n_row=0
                   if n_col<0:
                      n_col = 0
                      
                   if n_row>=input_grid.shape[0]:
                      n_row=input_grid.shape[0]-1
                   if n_col>=input_grid.shape[1]:
                      n_col = input_grid.shape[1]-1
                   
                   neighbor = input_grid[n_row,n_col]
                   if neighbor in target_colors:
                      output_grid[i,j]=neighbor
                      break
                else:
                  continue
                break
            

    return output_grid
```
