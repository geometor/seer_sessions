"""
1.  **Color Transformation:** Every blue pixel (color code 1) in the input grid is transformed to a red pixel (color code 2) in the output grid.
2.  **Row Extension (Conditional):** The output grid *may* have additional rows added to its bottom.
3.  **Extension Pattern:** If rows are added, the colors of the pixels in the added rows continue the vertical color alternation pattern that exist in the input. The number of rows to add appears related to extending the existing patterns until complete.
4. No columns are ever added or removed.
"""

import numpy as np

def get_vertical_color_pattern(grid, col):
    """Extracts the vertical color pattern for a given column."""
    pattern = []
    for row in range(grid.shape[0]):
        color = grid[row, col]
        if not pattern or color != pattern[-1]:
          pattern.append(color)
    return pattern

def calculate_extension_rows(input_grid):
   """
   Calculates the number of rows needed for extension.
   Finds the most common pattern length, and extends to a multiple of that.
   """
   pattern_lengths = []
   for col in range(input_grid.shape[1]):
      pattern = get_vertical_color_pattern(input_grid, col)
      pattern_lengths.append(len(pattern))
    
   #find most common
   counts = np.bincount(pattern_lengths)
   most_common_length = np.argmax(counts)

   rows_needed = 0
   if (input_grid.shape[0] % most_common_length) != 0:
       rows_needed =  most_common_length - (input_grid.shape[0] % most_common_length)

   return rows_needed

def extend_pattern(input_grid, num_rows):
    """Extends the grid by adding rows, continuing the established pattern."""
    extended_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    if num_rows > 0:
      new_rows = []
      for _ in range(num_rows):
        new_row = []
        for col in range(cols):
            pattern = get_vertical_color_pattern(extended_grid,col)
            next_color_index = len(new_rows) % len(pattern)
            if (len(new_rows) + rows )> 0: #need to use current last row
                last_row = extended_grid[-1,col]
                for i in range(len(pattern)):
                    if pattern[i] == last_row:
                        next_color_index = (i+1) % len(pattern)
                        break
            
            new_row.append(pattern[next_color_index])
        new_rows.append(new_row)
        extended_grid = np.vstack([extended_grid, new_row])

    return extended_grid

def transform(input_grid):
    # Create a copy of the input grid
    output_grid = np.copy(input_grid)

    # Replace all blue (1) pixels with red (2)
    output_grid[output_grid == 1] = 2

    # Determine how many rows to add
    rows_to_add = calculate_extension_rows(input_grid)
    
    #extend the pattern
    output_grid = extend_pattern(output_grid, rows_to_add)

    return output_grid