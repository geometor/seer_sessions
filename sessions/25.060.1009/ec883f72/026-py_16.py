"""
1.  **Identify a dividing line:** Find the highest row index `r` that contains a non-zero pixel.
2.  **Preserve the bottom:** Keep all rows from `r` to the bottom of the grid unchanged in the output grid.
3. Find the object at the dividing line
4.  **Clear above object:** Clear any pixels in the rows above object.
5. Move the object to the top of the grid.
"""

import numpy as np

def find_dividing_line(grid):
    """Finds the highest row index with a non-zero pixel."""
    non_zero_rows = np.where(grid != 0)[0]
    return np.min(non_zero_rows) if non_zero_rows.size > 0 else -1

def find_object_at_line(grid, row):
    """Finds the object that exists at the dividing line."""
    # Get the colors at the dividing row
    colors_at_row = grid[row, :]
    unique_colors = np.unique(colors_at_row)
    unique_colors = unique_colors[unique_colors != 0] #remove background
    
    if len(unique_colors) == 0:
      return None, None, None, None

    # pick the first non-zero color for now, assumption is one obj
    first_color = unique_colors[0]

    coords = np.argwhere(grid == first_color)
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    
    # additional check: does this object exist on the dividing line?
    if row >= min_row and row <= max_row:
      return min_row, min_col, max_row, max_col, first_color

    # object at line not found
    return None, None, None, None, None

def transform(input_grid):
    # Initialize output grid.
    output_grid = np.zeros_like(input_grid)

    # Find the dividing line.
    dividing_line = find_dividing_line(input_grid)

    if dividing_line == -1:
        return output_grid # Empty grid

    # Preserve the bottom part.
    output_grid[dividing_line:] = input_grid[dividing_line:]

    #Find the object at the dividing line
    min_row, min_col, max_row, max_col, color = find_object_at_line(input_grid, dividing_line)

    if color is None:
        return output_grid  # No object spans the dividing line

    #Clear above the object
    output_grid[:min_row,:] = 0

    # Move the object to the top.
    object_height = max_row - min_row + 1
    object_width = max_col - min_col + 1
    output_grid[0:object_height, min_col:min_col+object_width] = color

    return output_grid