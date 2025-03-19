"""
The transformation rule identifies a rectangle of a unique color within the
input grid and outputs the color of that rectangle. The rectangle is
determined to be unique if it does not share its dimensions with any
surrounding rectangle of a different color. If multiple such unique rectangles
are found within different subgrids, it chooses the rectangle within the
innermost such layer. If no such unique rectangle is found within concentric
layers, it outputs the color of the innermost layer.
"""

import numpy as np

def get_center_pixel(grid):
    """Returns the color of the center pixel of a grid."""
    rows = len(grid)
    cols = len(grid[0])
    return grid[rows // 2][cols // 2]

def find_innermost_rectangle(grid):
    """
    Recursively finds an inner rectangle that contrasts with a surrounding
    rectangle.

    Args:
      grid: The input grid (list of lists).

    Returns:
       The inner contrasting rectangle (list of lists) or the original grid if no such
       rectangle exists.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Base case: If the grid is 1x1, return grid.
    if rows == 1 and cols == 1:
        return grid

    # Find the outermost color.
    outer_color = grid[0][0]

    #check if entire grid is made of the same color
    all_same = True
    for i in range(rows):
      for j in range(cols):
        if grid[i][j] != outer_color:
          all_same = False
          break

    if all_same: return grid

    # Extract the inner grid by removing the outer border.
    inner_grid = [row[1:-1] for row in grid[1:-1]]
    
    if not inner_grid or not inner_grid[0]:
       return grid
        
    #check to see if inner grid is a rectangle and different in color from outer
    inner_color = inner_grid[0][0]
    inner_rows = len(inner_grid)
    inner_cols = len(inner_grid[0])
    
    inner_rect = True
    for i in range(inner_rows):
        for j in range(inner_cols):
          if inner_grid[i][j] != inner_color:
            inner_rect = False

    if inner_rect and inner_color != outer_color:
      return inner_grid
    else:
    # Recursively find the innermost square in the inner grid.
      return find_innermost_rectangle(inner_grid)

def transform(input_grid):
    """
    Transforms the input grid to extract the color of the central pixel of the
    innermost nested square, and output is a 1 x 1 grid with that value.

    Args:
        input_grid (list of lists): The input 2D grid.

    Returns:
        list: A 1x1 grid (list of lists) containing the color of the innermost
              square's center pixel.
    """
    # Find the innermost rectangle.
    innermost_rectangle = find_innermost_rectangle(input_grid)

    # Get the color of the center pixel of the innermost rectangle.
    center_color = get_center_pixel(innermost_rectangle)

    # Create a 1x1 output grid with the center color.
    output_grid = np.array([[center_color]])

    return output_grid.tolist()