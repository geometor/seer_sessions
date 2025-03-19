# ec883f72 • 015 • refine_coder

---
```python
"""
1. **Identify the "azure shape"**: This is a contiguous block of azure (8) pixels.
2. **Translate the azure shape**: Move the entire azure shape down by one row.
3. **Identify "magenta columns"**: These are vertical lines of magenta (6) pixels, potentially starting from a single magenta pixel.
4. **Handle each existing "magenta column" :**
    -  if there are any non-white pixels below, "push" the entire magenta column down by shifting its contents down one row at a time until the bottom-most magenta pixel is one above the highest non-white pixel in that column.
    - otherwise, extend the magenta column down to the bottom-most row if no other non-white pixels exist.

5. **Identify Columns in the original azure shape:**
   - Extend these columns down with magenta (6) until reaching one row above the lowest non-white pixel in the input grid, *unless* a non-white pixel is encountered earlier.
"""

import numpy as np

def find_azure_shape(grid):
    """Finds the coordinates of all azure (8) pixels."""
    return np.argwhere(grid == 8)

def translate_shape(coords, rows_to_move, grid_shape):
    """Translates a set of coordinates down by a specified number of rows."""
    translated_coords = []
    for r, c in coords:
        new_r = r + rows_to_move
        if 0 <= new_r < grid_shape[0]:  # Check bounds
            translated_coords.append((new_r, c))
    return np.array(translated_coords)

def find_magenta_columns(grid):
    """Identifies magenta columns and their start/end rows."""
    magenta_coords = np.argwhere(grid == 6)
    columns = {}
    for r, c in magenta_coords:
        if c not in columns:
            columns[c] = [r, r]  # [min_row, max_row]
        else:
            columns[c][0] = min(columns[c][0], r)
            columns[c][1] = max(columns[c][1], r)
    return columns

def find_lowest_non_white_row_in_column(grid, col, start_row):
    """Finds the lowest row index that contains a non-white pixel in a column, starting from a given row."""
    rows = grid.shape[0]
    for r in range(start_row, rows):
        if grid[r, col] != 0:
            return r
    return rows # if none found, return the last row + 1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. & 2. Translate Azure Shape
    azure_coords = find_azure_shape(input_grid)
    translated_azure_coords = translate_shape(azure_coords, 1, input_grid.shape)
    
    for r, c in azure_coords:
        output_grid[r,c] = 0 # clear the original

    for r, c in translated_azure_coords:
        output_grid[r, c] = 8

    # 3. Identify Magenta Columns
    magenta_columns = find_magenta_columns(input_grid)

    # 4. Handle Existing Magenta Columns (Push Down)
    for col, (start_row, end_row) in magenta_columns.items():
        lowest_non_white = find_lowest_non_white_row_in_column(input_grid, col, end_row + 1)
        
        if lowest_non_white < rows:
           # push
           push_distance = (lowest_non_white -1) - end_row
           if push_distance > 0:
              for r in range(end_row, start_row -1, -1):
                 output_grid[r + push_distance, col] = output_grid[r,col]
                 output_grid[r,col] = 0
        else:
           # extend - no other non-white pixels
           for r in range(end_row + 1, rows):
              output_grid[r,col] = 6 

    # 5. Extend Columns from Original Azure Shape
    azure_cols = np.unique(azure_coords[:, 1])
    for col in azure_cols:
        lowest_non_white = find_lowest_non_white_row_in_column(input_grid, col, 0)

        start_row_fill = 0
        if len(translated_azure_coords) > 0: # find any in this col
           azure_in_col = [ (r,c) for (r,c) in translated_azure_coords if c == col ]
           if len(azure_in_col) > 0:
              start_row_fill = max([r for (r,c) in azure_in_col]) + 1
        
        for row_index in range(start_row_fill, lowest_non_white):            
              output_grid[row_index, col] = 6

    return output_grid
```
