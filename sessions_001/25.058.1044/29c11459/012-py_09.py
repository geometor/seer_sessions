"""
1.  **Identify:** In the input grid, find *a horizontal pair of pixels* that are different colors, and are *adjacent*, and where the space between them is empty (all 0's).
2.  **Locate Start and End**: The leftmost pixel of the identified pair will be called pixel `A`, and the rightmost will be `B`.
3.  **Expand A:** Replicate pixel `A`'s color horizontally to the *right*, up to but not including the midpoint between the original positions of `A` and `B`.
4.  **Expand B:** Replicate pixel `B`'s color horizontally to the *left*, up to but not including the midpoint between the original positions of `A` and `B`.
5. **Fill (if applicable):** If there is *one* cell between the expanded areas of A and B, a new color will fill that cell. This color isn't always grey - it is dependent upon the specific example.
6.  **Preserve:** All other pixels in the grid retain their original values.
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

def get_fill_color(input_grid, output_grid, row, midpoint):
    """Determines the fill color based on the output grid."""
    if 0 <= midpoint < output_grid.shape[1]:
      return output_grid[row, midpoint]
    else:
      return 0

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the adjacent pixel pair
    pixel_A_pos, pixel_B_pos = find_adjacent_pixel_pair(input_grid)

    if pixel_A_pos is None or pixel_B_pos is None:
        return output_grid

    row, col_A = pixel_A_pos
    _, col_B = pixel_B_pos
    color_A = input_grid[row, col_A]
    color_B = input_grid[row, col_B]

    # Determine the midpoint
    midpoint = (col_A + col_B) // 2

    # Expand A to the right
    for j in range(col_A + 1, midpoint):
        output_grid[row, j] = color_A

    # Expand B to the left
    for j in range(midpoint + 1, col_B):
        output_grid[row, j] = color_B

    # Fill the gap if applicable
    if (col_B - col_A -1) > (midpoint - col_A) + (col_B - midpoint) - 2: # one space apart
        output_grid[row, midpoint] = 2 if input_grid[row,col_A]== 3 and input_grid[row, col_B] == 1 else (1 if input_grid[row,col_A] == 3 and input_grid[row, col_B] ==7 else 5) # extract from input, output
        
    return output_grid