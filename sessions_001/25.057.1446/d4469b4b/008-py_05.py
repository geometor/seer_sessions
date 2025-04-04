"""
1.  **Identify the Shape:** Locate the contiguous region of blue (1) pixels within the input grid.
2.  **Find Bounding Box:** Determine the smallest rectangle (bounding box) that completely encloses the blue shape. In this case it is 3x3.
3.  **Create Output Grid:** Generate a new, empty grid with the dimensions of the bounding box.
4. **Map input to output**: Map the input grid 3x3 central region on to the output grid
5.  **Color Mapping:**
    *   If an input pixel within the bounding box is blue (1), set the corresponding output pixel to gray (5).
    *   If an input pixel within the bounding box  is white (0), set the corresponding output pixel to white(0).
"""

import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No pixels of the specified color
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Find bounding box of blue pixels (color 1)
    bounding_box = get_bounding_box(input_grid, 1)
    if bounding_box is None:
        return np.zeros((1, 1), dtype=int) # Handle cases where the color doesn't exist

    min_row, max_row, min_col, max_col = bounding_box

    # Create output grid based on bounding box dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Map input pixels within the bounding box to the output grid
    for i in range(output_height):
        for j in range(output_width):
            input_row = min_row + i
            input_col = min_col + j
            if input_grid[input_row, input_col] == 1:
              output_grid[i,j] = 5
            else:
              output_grid[i, j] = 0


    return output_grid