"""
1. **Identify Key Color:** Determine the single non-zero color (the "key color") present in the input grid.
2. **Count Rows with Key Color:** Count the number of rows in the input grid that contain the key color.
3. **Count Columns with Key Color:** Count the number of columns in the input grid that contain the key color.
4. **Construct Output Grid:** Create a new grid where:
    *   The number of rows equals the count from step 2.
    *   The number of columns equals the count from step 3.
    *   All cells are filled with the key color.
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

    # Count Rows with Key Color
    rows_with_key_color = np.any(input_grid == key_color, axis=1).sum()

    # Count Columns with Key Color
    cols_with_key_color = np.any(input_grid == key_color, axis=0).sum()

    # Construct Output Grid
    output_grid = np.full((rows_with_key_color, cols_with_key_color), key_color)

    return output_grid.tolist()