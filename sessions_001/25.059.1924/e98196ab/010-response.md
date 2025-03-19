# e98196ab • 010 • example_2 • investigate_coder

---
```python
"""
The transformation removes the grey horizontal line, merges specific rows based upon color. Columns that contain multiple colors on the vertical axis combine colors, keeping the objects in the same columns.
"""

import numpy as np

def get_objects(grid):
    objects = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r,c]
            if color != 0:
                if color not in objects:
                    objects[color] = []
                objects[color].append((r, c))
    return objects

def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows // 2 + 1, cols), dtype=int) # //2 for safe division, +1 to handle input row with only 0

    # get objects
    objects = get_objects(input_grid)

    # Remove grey object (5)
    if 5 in objects:
      del objects[5] #delete grey color from objects
    
    # Group rows by color
    row_groups = {}
    for color, positions in objects.items():
        for r, c in positions:
            if color not in row_groups:
                row_groups[color] = set()
            row_groups[color].add(r)

    # Condense Rows, Combine Colors, skipping all-zero rows.
    output_row_index = 0
    sorted_colors = sorted(row_groups.keys()) #ensure consistent order, since dicts are unordered
    
    for color in sorted_colors:
        rows_ = sorted(list(row_groups[color])) #order rows
        target_rows = []
        
        
        combined_row = np.zeros(cols, dtype=int) #create blank combined row

        for row_index in rows_: #scan through rows of the given color
            for col_index in range(cols): #scan through columns
                if input_grid[row_index, col_index] != 0: #process non-zero
                    if combined_row[col_index] == 0: #if empty output, set color of current input cell
                        combined_row[col_index] = input_grid[row_index, col_index]
                    elif input_grid[row_index, col_index] != combined_row[col_index]:
                        # Check input grid vertically for any other color
                        found_other_color = False
                        for other_row_index in range(rows):
                            if input_grid[other_row_index, col_index] != 0 and\
                               input_grid[other_row_index, col_index] != combined_row[col_index]:
                                  combined_row[col_index] = input_grid[other_row_index, col_index]

        
        empty = True
        for c in range(cols): #find if any color at the columns index
          if combined_row[c] != 0:
            empty = False
        if not empty:
          output_grid[output_row_index,:] = combined_row
          output_row_index += 1
    
    #remove all zero rows, again
    output_grid_final=[]
    for i in range(output_grid.shape[0]):
      row = output_grid[i,:]
      is_zero = all(e == 0 for e in row) 
      if not is_zero:
        output_grid_final.append(list(row))
    output_grid_final = np.array(output_grid_final)

    return output_grid_final
```
