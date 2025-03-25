"""
1.  **Identify Key Lines:** Find the leftmost vertical blue line (color 1) and the leftmost vertical gray line (color 5) in the input grid.
2.  **Extract Region of Interest After Grey:** Extract the rectangular region to the *right* of the gray line. This is the "transform region".
3.  **Create Output Grid:** Create a new output grid with the same height as the input grid and a width of 4.
4.  **Copy Blue Line (Conditional on Position):**
    *   If the blue line is at x=0, copy the blue line to the first column (column 0) of the output grid.
    *    If the blue line is *not* at x=0, the first column is copied from the transform region (if available)
5.  **Copy Transform Region (Conditional):** Copy the "transform region" to the output grid, starting at column 1 if blue line *was* at x=0, and at column 0 if it wasn't.  Only copy up to 3 columns of the transform region, ensuring the total output width is 4.
6.  **Fill Remaining Columns (Conditional on Blue Position):**
    *   If the blue line was present at x=0:
        *   If the transform region had fewer than 3 columns, fill the remaining columns of the output grid by repeating the columns between the blue line and the grey line. If there are no columns between, fill with the blue column.
    *   If the blue line was *not* present at x = 0
        *   If the transform region had fewer than 4 columns, fill remaining columns by repeating columns between the blue line and the gray line. If there are no columns between, leave black.
"""

import numpy as np

def find_vertical_line(grid, color):
    """Finds the leftmost vertical line of a specified color."""
    height, width = grid.shape
    for x in range(width):
        for y in range(height):
            if grid[y, x] == color:
                # Check if it's a vertical line
                if y + 1 == height or grid[y+1, x] == color:
                    return x
    return -1  # Not found

def extract_transform_region(grid, start_x):
    """Extracts the region to the right of the given x-coordinate."""
    if start_x == -1:
        return np.zeros((grid.shape[0], 0), dtype=int)
    height, width = grid.shape
    if start_x + 1 >= width:
        return np.zeros((height, 0), dtype=int)

    return grid[:, start_x + 1:]

def get_fill_columns(grid, blue_x, gray_x):
    """Gets the columns between the blue and gray lines for filling."""
    if blue_x + 1 >= gray_x:
      return None
    else:
      return grid[:, blue_x + 1:gray_x]

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    # 1. Identify Key Lines
    blue_line_x = find_vertical_line(input_grid, 1)
    gray_line_x = find_vertical_line(input_grid, 5)

    # 2. Extract Region of Interest After Grey
    transform_region = extract_transform_region(input_grid, gray_line_x)
    transform_height, transform_width = transform_region.shape

    # 3. Create Output Grid
    output_grid = np.zeros((height, 4), dtype=int)

    # 4. Copy Blue Line (Conditional on Position)
    if blue_line_x == 0:
        for y in range(height):
            output_grid[y, 0] = input_grid[y, blue_line_x]
        start_col = 1
    else:
        start_col = 0


    # 5. Copy Transform Region (Conditional)
    for y in range(transform_height):
        for x in range(min(transform_width, 4 - start_col)):
            output_grid[y, x + start_col] = transform_region[y, x]


    # 6. Fill Remaining Columns (Conditional on Blue Position)
    if blue_line_x == 0:

        fill_columns = get_fill_columns(input_grid, blue_line_x, gray_line_x)
        if fill_columns is None:
            fill_columns = input_grid[:, blue_line_x:blue_line_x+1]
        fill_height, fill_width = fill_columns.shape

        for x in range(transform_width + start_col, 4):
          for y in range(height):
              output_grid[y,x] = fill_columns[y % fill_height, (x - (transform_width + start_col)) % fill_width ]

    elif blue_line_x != -1:
        fill_columns = get_fill_columns(input_grid, blue_line_x, gray_line_x)

        if fill_columns is not None: # fill if there were any
            fill_height, fill_width = fill_columns.shape
            for x in range(transform_width, 4):
              for y in range(height):
                  output_grid[y,x] = fill_columns[y % fill_height, (x-transform_width) % fill_width]
    return output_grid.tolist()