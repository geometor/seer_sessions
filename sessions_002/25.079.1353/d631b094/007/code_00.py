"""
1. **Identify Key Color:** Find the single non-zero color in the input grid. This is the "key color". If there are no non-zero colors, the key color is 0.
2. **Count Rows with Key Color:** Count the number of rows in the input grid that contain the key color at least once.
3. **Count Columns with Key Color:** Count the number of columns in the input grid that contain the key color at least once.
4. **Construct Output Grid:** Create a new output grid with dimensions M x N, where M is the number of rows containing the key color and N is the number of columns containing the key color.
5. **Fill Output Grid:** Fill the entire output grid with the key color.
6. **Handle the zero case:** If there are zero rows or columns containing the key color, the output will be a 1x1 grid with the value of the key color.
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
    rows_with_key_color = np.sum(np.any(input_grid == key_color, axis=1))

    # Count Columns with Key Color
    cols_with_key_color = np.sum(np.any(input_grid == key_color, axis=0))

    # Construct Output Grid (Handle the zero case)
    if rows_with_key_color == 0 or cols_with_key_color == 0:
        output_grid = np.full((1, 1), key_color)
    else:
        output_grid = np.full((rows_with_key_color, cols_with_key_color), key_color)
    

    return output_grid.tolist()