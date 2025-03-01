"""
The transformation extracts the contiguous non-zero colored "object" from the input grid and represents it in a compressed, alternating-column format in the output grid. The crucial aspects are identifying the object, its color, and rearranging its pixels while preserving a compressed trace of its original shape within the alternating color/white columns of the output.
"""

import numpy as np

def find_object(grid):
    # Find the non-zero colored object in the grid
    rows, cols = grid.shape
    object_color = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                object_color = grid[r, c]
                break
        if object_color != 0:
            break

    if object_color == 0:
        return None, 0  # No object found

    object_pixels = []
    visited = set()

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != object_color:
            return
        visited.add((row, col))
        object_pixels.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == object_color:
               dfs(r,c)
               break
        if len(visited) > 0:
            break

    return object_pixels, object_color

def transform(input_grid):
    # Find the object and its color
    object_pixels, object_color = find_object(input_grid)

    if object_color == 0:
        return np.zeros((3, 6), dtype=int)  # Return a default 3x6 grid if no object

    # Determine output grid dimensions based on input object rows and columns
    object_rows = set()
    object_cols = set()
    
    for r, c in object_pixels:
      object_rows.add(r)
      object_cols.add(c)
    
    num_rows = len(object_rows)
    num_cols = len(object_cols)
    
    output_cols = max(num_rows,num_cols) * 2
    output_grid = np.zeros((3, output_cols), dtype=int)


    # Process object pixels row by row
    row_index = 0
    col_index = 0
    
    processed_rows = set()

    for r, c in object_pixels:
        if r not in processed_rows:
            if input_grid[r, :].max() > 0:  #color pixel present
               
               temp_col_index = 0
               row_pixels = []

               # collect all object pixels of current row
               for c_scan in range(input_grid.shape[1]):
                   if input_grid[r, c_scan] == object_color:
                      row_pixels.append( (r,c_scan))

                #populate the output row with alternating object colors
               for _ in row_pixels:
                    output_grid[row_index, temp_col_index] = object_color
                    temp_col_index += 2  # Skip a column for the alternating 0

            processed_rows.add(r)
            row_index += 1
            if row_index > 2:
              break; # stop if done with rows

    return output_grid