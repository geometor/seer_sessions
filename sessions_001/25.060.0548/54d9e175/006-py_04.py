"""
1.  **First Column Transformation:** The color of the first column in the input grid is transformed to orange (7) in the output grid.
2.  **White Pixel Transformation:** All white (0) pixels in the input grid are transformed to magenta (6) in the output grid.
3. **Preserve Gray Column:** If there exists a column where all values are gray(5), then preserve it.
"""

import numpy as np

def find_gray_columns(grid):
    # Find columns that contain only gray (5) pixels.
    gray_columns = []
    for j in range(grid.shape[1]):
        column = grid[:, j]
        if np.all(column == 5):
            gray_columns.append(j)
    return gray_columns

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input, filled with magenta (6)
    output_grid = np.full_like(input_grid, 6)

    rows, cols = input_grid.shape

    # Find purely gray columns
    gray_columns = find_gray_columns(input_grid)
    
    #First Column transformation
    first_col_color = input_grid[0,0]
    if first_col_color != 0: # Don't transform if it is white.
      for i in range(rows):
        output_grid[i,0] = 7

    # Preserve Gray Column
    for col in gray_columns:
        for i in range(rows):
            output_grid[i, col] = 5


    return output_grid