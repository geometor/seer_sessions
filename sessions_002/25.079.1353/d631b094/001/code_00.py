"""
1. **Identify Key Color:** Find the single non-zero color value within the input grid. This is the "key color".
2. **Count Key Colors:** Count, for the non zero colors, how many are present in each row and column.
3. **Construct Output Grid:** Create a new output grid. The key color will fill a new grid of M x N where M is the number of non-zero colors in the rows and N is the number of non-zero colors in the columns.
"""

import numpy as np

def get_key_color(grid):
    # Flatten the grid and remove zeros, then return the unique color
    unique_colors = np.unique(grid[grid != 0])
    if len(unique_colors) > 0:
        return unique_colors[0]
    else:
        return 0

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Identify Key Color
    key_color = get_key_color(input_grid)

    # Count Key Colors in rows and cols
    row_count = 0
    for row in input_grid:
        if key_color in row:
            row_count += np.count_nonzero(row == key_color)
            
    col_count = 0
    for col in input_grid.T:  # Transpose for column-wise iteration
        if key_color in col:
            col_count += np.count_nonzero(col == key_color)

    # Construct Output Grid
    output_grid = np.full((row_count, col_count), key_color) if row_count >0 and col_count > 0 else np.array([[key_color]])
    if row_count == 0 and col_count >0:
        output_grid = np.full((col_count), key_color)
    if col_count == 0 and row_count > 0:
        output_grid = np.full((row_count), key_color)

    return output_grid.tolist()