"""
1.  **Identify Objects:** Find the single vertical line (a column where all pixels have the same non-zero color).  Also, find the horizontal object (row) which intersects this line.

2.  **Locate Intersection:** Determine the row and column indices where the vertical line and horizontal line intersect.

3. **Frame the Intersection Point:** Starting from the row above the interesection, down to the intersection row, replace the cells adjacent (left and right) to the vertical line's original color with yellow ('4').

4. **Preserve other parts of grid**: Ensure that the original vertical line of pixels remain their color, with the new frame extending out, and ensure pixels away from the intersection and frame are unchanged.
"""

import numpy as np

def find_vertical_line(grid):
    """Finds the vertical line in the grid."""
    rows, cols = grid.shape
    for j in range(cols):
        first_color = grid[0, j]
        if first_color == 0:
            continue
        is_vertical_line = True
        for i in range(1, rows):
            if grid[i, j] != first_color:
                is_vertical_line = False
                break
        if is_vertical_line:
            return j, first_color
    return None, None

def find_horizontal_line(grid, vertical_line_col, vertical_line_color):
    """Finds the horizontal line intersecting the vertical line."""
    rows, cols = grid.shape
    for i in range(rows):
        if grid[i,vertical_line_col] == vertical_line_color:
          for j in range(cols):
            if j != vertical_line_col:
              if grid[i,j] != 0 and grid[i,j] != vertical_line_color:
                #check to see if it is a horizontal line
                first_color = grid[i,j]
                is_horizontal = True
                for k in range(cols):
                  if grid[i,k] != first_color and grid[i,k] != 0 and k != vertical_line_col:
                    is_horizontal = False
                    break

                if is_horizontal:
                  return i, first_color
    return None, None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = grid.shape
    output_grid = grid.copy()

    # Find the vertical line
    vertical_line_col, vertical_line_color = find_vertical_line(grid)

    if vertical_line_col is None:
        return output_grid # No vertical line found, return original

    #find horizontal line
    horizontal_line_row, horizontal_line_color = find_horizontal_line(grid, vertical_line_col, vertical_line_color)

    if horizontal_line_row is None:
      return output_grid


    # Locate intersection (already have row and col from above steps)

    # Frame the intersection
    intersection_row = horizontal_line_row
    intersection_col = vertical_line_col

    #row above
    row_above = max(0, intersection_row -1)
    if row_above != intersection_row:
      for j in range(cols):
        if grid[row_above,j] == vertical_line_color:
          if j > 0:
            output_grid[row_above, j-1] = 4
          if j < cols -1:
            output_grid[row_above, j+1] = 4
    
    #intersection row
    if intersection_col > 0:
        output_grid[intersection_row, intersection_col - 1] = 4  # Left
    if intersection_col < cols - 1:
        output_grid[intersection_row, intersection_col + 1] = 4  # Right

    return output_grid.tolist()