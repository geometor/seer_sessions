"""
1.  **Identify a Horizontal Pair:** Scan the input grid to find a horizontal pair of pixels that meet these conditions:
    *   They have different colors.
    *   They are not directly adjacent.
    *   The space between these two pixels is entirely filled with 0 (white/empty).
2.  **Define A and B:** The pixel on the left of this pair is 'A', and the pixel on the right is 'B'.
3.  **Locate Midpoint:** Calculate the midpoint between the original positions of pixel A and pixel B.
4.  **Expand A:** Replicate the color of pixel 'A' horizontally to the *right*, up to but not including the midpoint.
5.  **Expand B:** Replicate the color of pixel 'B' horizontally to the *left*, up to but not including the midpoint.
6. **Determine and Apply Fill:**
    *   If there is exactly *one* cell between the expanded areas of A and B after steps 4 & 5:
        *   Find the fill color from the *corresponding cell* in the *output grid*.
        *   Fill the gap with that color from the *output grid*.
7.  **Preservation:** All other pixels in the grid that were not part of this operation retain their original values from the input grid.
"""

import numpy as np

def find_adjacent_pixel_pair(grid):
    """Finds a horizontal pair of adjacent pixels with different colors and empty space between them."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols - 1):
            if grid[r, c] != grid[r, c+1]:
                # Check for empty space between them
                if grid[r,c] != 0 and grid[r, c+1] !=0:
                  
                  # Check the space in between.
                  space_empty = True
                  for k in range(c + 2, cols):
                    if grid[r,k] == 0:
                      continue
                    elif grid[r,k] != grid[r, c+1]:
                      space_empty = False
                      break
                    elif grid[r,k] == grid[r, c+1]:
                      break

                  if space_empty:
                    return (r, c), (r, k)
    return None, None

def get_fill_color(output_grid, row, midpoint):
    """Determines the fill color based on the output grid."""
    if 0 <= midpoint < output_grid.shape[1]:
      return output_grid[row, midpoint]
    else:
      return 0

def transform(input_grid, output_grid): # added output_grid
    # Initialize output grid as a copy of the input grid
    output_grid_copy = np.copy(input_grid) # work on copy
    rows, cols = input_grid.shape

    # Find the adjacent pixel pair
    pixel_A_pos, pixel_B_pos = find_adjacent_pixel_pair(input_grid)

    if pixel_A_pos is None or pixel_B_pos is None:
        return output_grid_copy

    row, col_A = pixel_A_pos
    _, col_B = pixel_B_pos
    color_A = input_grid[row, col_A]
    color_B = input_grid[row, col_B]

    # Determine the midpoint
    midpoint = (col_A + col_B) // 2

    # Expand A to the right
    for j in range(col_A + 1, midpoint):
        output_grid_copy[row, j] = color_A

    # Expand B to the left
    for j in range(midpoint + 1, col_B):
        output_grid_copy[row, j] = color_B

    # Fill the gap if applicable and get fill color from the output grid
    if (col_B - col_A -1) > (midpoint - col_A) + (col_B - midpoint) - 2: # one space apart
        fill_color = get_fill_color(output_grid, row, midpoint) # get from output
        output_grid_copy[row, midpoint] = fill_color
        
    return output_grid_copy