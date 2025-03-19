"""
1.  **Identify** any horizontal or vertical bars, where all pixels in a row or
    column are the same.
2.  **Identify** shape1: For each example, shape1 consists of the colored pixels that are *not* blue.
3.  **Copy** shape1 to create shape2.
4.  **Translate** shape2:
    *   If there is a vertical bar, place shape2 to the immediate right of the
        bar. Align the top edge of shape2 with the bottom edge of the bar.
    *   if there is a horizontal bar, place shape2 immediately below the bar.
        Align the left edge of shape2 with the right edge of the bar.
    *   If there is no bar, place shape 2 at the origin (0,0)
5.  **Keep** the bar, if present, in its original position.
6.  **Remove** all blue pixels from the grid.
"""

import numpy as np

def find_bar(grid):
    """Finds the column index of a vertical bar or row index of a horizontal bar, and returns the type, or -1, None if not found."""
    rows, cols = grid.shape
    # Check for vertical bar
    for c in range(cols):
        first_val = grid[0, c]
        if all(grid[r, c] == first_val for r in range(rows)):
            return c, 'vertical'
    # Check for horizontal bar
    for r in range(rows):
        first_val = grid[r, 0]
        if all(grid[r, c] == first_val for c in range(cols)):
            return r, 'horizontal'
    return -1, None  # Return -1, None if no bar is found

def find_shape(grid):
    """Finds the coordinates of a shape defined by non-blue pixels."""
    rows, cols = grid.shape
    shape_coords = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1:
                shape_coords.append((r, c))
    return shape_coords

def translate_shape(coords, row_offset, col_offset):
    """Translates a set of coordinates by given offsets."""
    return [(r + row_offset, c + col_offset) for r, c in coords]

def remove_color(grid, color):
    """Removes all pixels of a specified color from the grid."""
    return np.where(grid == color, 0, grid)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Identify any horizontal or vertical bars
    bar_pos, bar_type = find_bar(input_grid)

    # Identify shape1 (all non-blue pixels)
    shape1_coords = find_shape(input_grid)

    # Copy shape1 to create shape2
    shape2_coords = shape1_coords.copy()

    #fill original shape into output
    for r, c in shape1_coords:
      output_grid[r,c] = input_grid[r,c]

    # Determine row and column offset for shape2 translation
    if bar_type == 'vertical':
        bar_bottom = input_grid.shape[0]
        row_offset = bar_bottom - min(r for r, c in shape1_coords)
        col_offset = bar_pos - min(c for r, c in shape1_coords) + 1
    elif bar_type == 'horizontal':
        bar_right = input_grid.shape[1]
        row_offset = bar_pos - min(r for r, c in shape1_coords) + 1
        col_offset = bar_right - min(c for r, c in shape1_coords)
    else:  # No bar
        row_offset = -min(r for r, c in shape1_coords)
        col_offset = -min(c for r, c in shape1_coords)

    # Translate shape2
    shape2_coords = translate_shape(shape2_coords, row_offset, col_offset)

    #fill translated shape into output
    for r, c in shape2_coords:
        #make sure to stay in grid, the shape can be clipped
        if r < output_grid.shape[0] and c < output_grid.shape[1]:
            output_grid[r, c] = input_grid[r-row_offset,c-col_offset]

    # Keep the bar
    if bar_type == 'vertical':
        for r in range(output_grid.shape[0]):
            output_grid[r, bar_pos] = input_grid[r, bar_pos]
    elif bar_type == 'horizontal':
        for c in range(output_grid.shape[1]):
            output_grid[bar_pos, c] = input_grid[bar_pos, c]

    # Remove blue pixels
    output_grid = remove_color(output_grid, 1)

    return output_grid