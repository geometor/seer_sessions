# 045e512c • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule involves identifying distinct colored objects (azure, green, and red), 
replicating the red object vertically, and overlaying a replicated and expanded green object
onto the azure object, maintaining the original white space.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds the top-left corner and dimensions of a contiguous block of the given color.
    Returns None if no such object is found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None

    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return (min_row, min_col), height, width

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.zeros_like(input_grid)

    # Find objects
    azure_obj = find_object(input_grid, 8)
    green_obj = find_object(input_grid, 3)
    red_obj = find_object(input_grid, 2)

    # Replicate and extend Red vertically
    if red_obj:
        red_pos, red_height, red_width = red_obj
        for row in range(input_grid.shape[0]): #grid height
            for col_offset in range(red_width):
                if (red_pos[1] + col_offset < input_grid.shape[1] and
                    red_pos[0] + row < input_grid.shape[0] and
                    input_grid[red_pos[0] + (row%red_height) , red_pos[1] + col_offset] == 2) :
                    
                   output_grid[row, red_pos[1] + col_offset] = 2

    # Overlay extended green on azure.
    if azure_obj and green_obj:
        azure_pos, azure_height, _ = azure_obj
        green_pos, _, _ = green_obj
        
        row_start = azure_pos[0]
        row_end = input_grid.shape[0] # or azure_pos[0] + azure_height

        # print(f"DEBUG: row_start={row_start}, row_end={row_end}, azure_pos={azure_pos}, green_pos={green_pos}")

        for row in range(row_start, row_end):
          if row < input_grid.shape[0] :
            col = green_pos[1]
            if row >= azure_pos[0] and (row - azure_pos[0])< azure_height :
                output_grid[row,col] = 3

                if (row - azure_pos[0])%2 != 0:
                    if col+1 < output_grid.shape[1] :
                       output_grid[row, col+1] = 3
                col+=2

            # check azure to the right.
            while col < azure_pos[1] + azure_height and col < input_grid.shape[1] :
                output_grid[row,col] = input_grid[row,col]
                col+=1

    # copy azure ontop of green 
    if azure_obj and green_obj:
        azure_pos, azure_height, azure_width = azure_obj
        for row in range(azure_height):
           for col in range(azure_width):
               if( azure_pos[0] + row < output_grid.shape[0] and
                   azure_pos[1] + col < output_grid.shape[1] and
                   input_grid[azure_pos[0] + row, azure_pos[1] + col] == 8
                   ) :
                  output_grid[azure_pos[0] + row, azure_pos[1] + col] = 8

    return output_grid
```
