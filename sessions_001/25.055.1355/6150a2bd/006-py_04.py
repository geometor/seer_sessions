"""
The transformation rule distinguishes between single-pixel objects at the corners and other parts of the grid. Single-pixel objects at the four corners of the grid remain unchanged in their position and color. The remaining elements of the grid undergo a -90 degree rotation (currently under revision as it doesn't fully explain Example 1's transformation).
"""

import numpy as np

def get_corners(grid):
    """
    Returns the coordinates of the four corners of the grid.
    """
    rows = len(grid)
    cols = len(grid[0])
    return [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]

def is_single_pixel_object(grid, row, col):
    """
    Checks if a pixel at a given location is a single-pixel object (no adjacent pixels of the same color).
    """
    rows = len(grid)
    cols = len(grid[0])
    color = grid[row][col]

    # Check adjacent cells (up, down, left, right)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] == color:
            return False  # Found an adjacent pixel of the same color

    return True

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    1. Single-pixel objects at the corners remain unchanged.
    2. Other parts of the grid undergo a -90 degree rotation (to be refined).
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = [[0] * cols for _ in range(rows)]  # Initialize with 0s

    # 1. Handle single-pixel corner objects
    corners = get_corners(input_grid)
    for row, col in corners:
        if is_single_pixel_object(input_grid, row, col):
            output_grid[row][col] = input_grid[row][col]

    # 2. Rotate the rest (-90 degrees, needs further analysis)
    # Create a temporary grid to hold the non-corner elements
    temp_grid = []
    temp_row_map = []
    for i in range(rows):
      temp_row = []
      map_row = []
      for j in range(cols):
        if (i,j) not in corners or not is_single_pixel_object(input_grid, i, j):
          temp_row.append(input_grid[i][j])
          map_row.append((i,j))
        else:
          map_row.append(None)  # Mark as already handled (corner single-pixel)
      if len(temp_row) > 0:
        temp_grid.append(temp_row)
        temp_row_map.append(map_row)


    # Rotate the temp_grid using numpy (-90 deg = flipud then transpose)
    if len(temp_grid) > 0: #handle empty grid
        rotated_temp_grid = np.flipud(np.array(temp_grid)).transpose().tolist()
    else:
        rotated_temp_grid = []

    #merge back into the output grid.
    rotated_row_map = np.flipud(np.array(temp_row_map)).transpose().tolist()


    # Map rotated elements back to output_grid
    for i in range(len(rotated_temp_grid)):
        for j in range(len(rotated_temp_grid[0])):
            orig_i, orig_j = rotated_row_map[i][j]
            if orig_i is not None and orig_j is not None:  # Check for valid mapping
               output_grid[orig_i][orig_j] = rotated_temp_grid[i][j]

    return output_grid