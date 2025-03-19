"""
1.  **Identify the Yellow Shape:** Locate the contiguous region of yellow (4) pixels within the input grid.
2.  **Bounding Box and Expansion:**
    -   Determine the bounding box of the yellow shape, expanding on the right and bottom, filling it in.
    -   From the original box's top-left, extend a rectangle down and to the
        right to fill in the area encompassed by the original shape.
3.  **Output:** Create a new grid containing only the filled expanded yellow shape (with 0s as padding), where the bounding edges of the shape are aligned with the edges of the output image.

"""

import numpy as np

def find_yellow_shape(grid):
    """Finds the coordinates of yellow pixels in the grid."""
    yellow_pixels = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 4:
                yellow_pixels.append((r, c))
    return yellow_pixels

def bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    if not coords:
        return None  # Handle empty case
    min_row = min(coords, key=lambda x: x[0])[0]
    max_row = max(coords, key=lambda x: x[0])[0]
    min_col = min(coords, key=lambda x: x[1])[1]
    max_col = max(coords, key=lambda x: x[1])[1]
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Find yellow pixels
    yellow_pixels = find_yellow_shape(input_grid)

    # Calculate bounding box
    top_left, bottom_right = bounding_box(yellow_pixels)
    min_row, min_col = top_left
    max_row, max_col = bottom_right

    # Determine output grid size
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
        
    # expand by checking min/max row
    output_height *= 2
    output_width *= 2

    # Initialize output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # adjust for expansion
    max_row_exp = output_height -1
    max_col_exp = output_width - 1

    # Fill the expanded shape in the output grid
    for r in range(output_height):
      for c in range(output_width):
        if r >= 0 and r <= max_row_exp and c >=0 and c <= max_col_exp:
            output_grid[r,c] = 4

    return output_grid