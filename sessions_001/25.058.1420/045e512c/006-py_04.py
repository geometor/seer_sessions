"""
1.  **Identify Objects:** Locate the distinct azure, green, and red objects within the input grid. An object is a contiguous block of pixels of the same color.
2.  **Red Object Transformation:** The red object is extended vertically. The red object's pattern is extended to cover the full height of the output grid.
3.  **Preserve Other Objects:** The azure and green objects retain their original shapes, positions, and colors. The final positions and shapes are present in both the input and output grids.
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
    output_grid = np.copy(input_grid)

    # Find objects
    azure_obj = find_object(input_grid, 8)
    green_obj = find_object(input_grid, 3)
    red_obj = find_object(input_grid, 2)

    # Red Object Transformation: extend vertically, preserving pattern
    if red_obj:
        red_pos, red_height, red_width = red_obj
        for row in range(output_grid.shape[0]):
            for col_offset in range(red_width):
                if (red_pos[1] + col_offset < input_grid.shape[1] and
                    red_pos[0] + row < input_grid.shape[0] ) :

                    output_grid[row, red_pos[1] + col_offset] = input_grid[(red_pos[0] + (row % red_height)), red_pos[1] + col_offset]
    
    # Preserve green and azure
    return output_grid