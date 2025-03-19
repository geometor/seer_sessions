"""
Extracts the 7x7 top-left "flower" pattern from the input grid, replacing all non-flower pixels with green (3).
"""

import numpy as np

def get_flower_pattern_at(grid, center_row, center_col):
    """Extracts the 7x7 grid centered at the given coordinates."""
    rows, cols = grid.shape
    if not (3 <= center_row < rows - 3 and 3 <= center_col < cols - 3):
        return None  # Center too close to edge for 7x7

    return grid[center_row-3:center_row+4, center_col-3:center_col+4]

def is_flower_pixel(grid, row, col, center_color):
   """Checks if a pixel at grid[row,col] is part of the flower pattern,
   given center color.
   """   
   center_row, center_col = 3,3
   
   if grid[row,col] == center_color:
      if row == center_row and col == center_col:
          return True

   if grid[row, col] == 0:
      if (abs(row - center_row) == 3 and abs(col - center_col) <=1 ) or (abs(row-center_row)<=1 and abs(col-center_col)==3):
         return True
         
   if grid[row,col] == 2:
        if (abs(row - center_row) == 2 and abs(col - center_col) == 0 ) or (abs(row-center_row)==0 and abs(col-center_col)==2):
         return True
   
   if grid[row,col] == 4:
         if (abs(row - center_row) == 1 and abs(col - center_col) == 0 ) or (abs(row-center_row)==0 and abs(col-center_col)==1):
          return True

   if grid[row,col] == 8:
         if (abs(row - center_row) == 2 and abs(col - center_col) == 1 ) or (abs(row-center_row)==1 and abs(col-center_col)==2):
          return True
   return False

def transform(input_grid):
    # Find the top-left flower (center color 3)
    input_grid = np.array(input_grid)    
    center_row, center_col = 3,3
    
    flower_grid =  get_flower_pattern_at(input_grid, center_row, center_col)
    
    if flower_grid is None:
       return None
    
    output_grid = np.copy(flower_grid)
    center_color = output_grid[3,3]
    # Replace non-flower pixels with green (3)
    for row in range(7):
        for col in range(7):
            if not is_flower_pixel(output_grid, row, col, center_color):
                output_grid[row, col] = 3

    return output_grid.tolist()