"""
1.  **Identify the Red Anchor:** Find the red rectangular object. This is the anchor point for the transformation.
2.  **Construct Extension Shape:**
    *   Extend one unit up from the top of the red square.
    *   Extend to the right based on a rule: find any other objects in the grid, the width of the constructed shape should match the right-most edge of the all non-red colored objects.
    *   Fill this extended shape with blue.
3.  **Overlay Remaining Objects:** Overlay any objects not of color red on top of the constructed blue shape, maintaining original colors and positions.
4. **Background** The background color is yellow(4)
"""

import numpy as np

def find_object(grid, color):
    """Finds the top-left corner and dimensions of an object of a given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None, None, None, None  # Object not found
    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return min_row, min_col, height, width

def find_rightmost_edge(grid, excluded_color):
    """Finds the rightmost edge of objects, excluding a specific color."""
    rows, cols = np.where(grid != excluded_color)
    if len(cols) == 0:
        return 0  # No objects found (other than excluded color)
    return np.max(cols)

def transform(input_grid):
    # Initialize output grid with the background color (yellow = 4)
    output_grid = np.full(input_grid.shape, 4, dtype=int)

    # 1. Identify the Red Anchor
    red_row, red_col, red_height, red_width = find_object(input_grid, 2)

    if red_row is None:  # If no red object, return background grid (or original)
        return output_grid

    # 2. Construct Extension Shape
    #   - Extend one unit up
    top_row = max(0, red_row - 1)

    #   - Extend to the right
    rightmost_edge = find_rightmost_edge(input_grid, 2)
    
    # adjust for zero based indexing
    rightmost_col = rightmost_edge + 1

    #   - Fill with blue
    for r in range(top_row, red_row + red_height):
        for c in range(red_col, rightmost_col):
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                output_grid[r, c] = 1

    # 3. Overlay Remaining Objects (excluding red)
    for color in range(10):  # Iterate through all possible colors
        if color != 2 and color != 4: #exclude red and yellow
            obj_row, obj_col, obj_height, obj_width = find_object(input_grid, color)
            if obj_row is not None:
                for r in range(obj_row, obj_row + obj_height):
                    for c in range(obj_col, obj_col + obj_width):
                        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                            output_grid[r, c] = color

    #replace red anchor(needed because of overlap in loop above)
    for r in range(red_row, red_row + red_height):
        for c in range(red_col, red_col + red_width):
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
               output_grid[r,c] = 2        

    return output_grid