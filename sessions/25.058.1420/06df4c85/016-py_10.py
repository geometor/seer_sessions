"""
1.  **Identify Vertical Stripes:** Locate vertical stripes of yellow (4) pixels. These stripes repeat every three columns across the entire grid.

2.  **Identify Target Objects:** Within each yellow stripe, identify 2x2 squares of green (3) or red (2) pixels.

3.  **Horizontal Replication (Conditional):** For each identified 2x2 square within a yellow stripe, replicate it horizontally *within the boundaries of that stripe*.
    *   If a green or red object exists on row `r` and column `c`, check how many empty yellow cells are on that row and within that stripe.
    *   Replicate the object to the right of existing objects, and then to the left (if space allows).
    * The green and red squares appear to duplicate differently depending on the specific input - sometimes just extending to the right, sometimes appearing on both left and right.

4.  **Preserve Unchanged:** All white (0) pixels, and yellow pixels that don't contain replicated objects, remain unchanged.

5. **Output Grid Creation:** The output grid maintains the exact same overall structure as the input, with the changes performed in the horizontal replication of green/red blocks within yellow stripes.
"""

import numpy as np

def find_objects(grid, color, size=2):
    objects = []
    rows, cols = grid.shape
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if np.all(grid[r:r+size, c:c+size] == color):
                objects.append((r, c))
    return objects

def get_stripe_bounds(col, grid_width):
    stripe_start = col
    while stripe_start >= 0 and (stripe_start % 3) != 2:
        stripe_start -= 1
    stripe_end = col
    while stripe_end < grid_width and (stripe_end % 3) != 1:
        stripe_end += 1
    return stripe_start, stripe_end


def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find green and red objects
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)

    all_objects = green_objects + red_objects

    # Iterate through the objects
    for r, c in all_objects:
      # find color
      color = input_grid[r,c]
      # Get stripe boundaries
      stripe_start, stripe_end = get_stripe_bounds(c, cols)

      # Replicate horizontally within stripe
      # First, replicate to the right
      current_col = c + 2 # original object width = 2
      while current_col + 1 <= stripe_end and input_grid[r, current_col] == 4 and input_grid[r+1, current_col] == 4 :
        output_grid[r:r+2, current_col:current_col+2] = color
        current_col += 3

      # Then, replicate to the left.
      current_col = c-3
      while current_col >= stripe_start and input_grid[r, current_col+2] == 4 and input_grid[r+1, current_col+2] == 4:
        output_grid[r:r+2, current_col:current_col+2] = color
        current_col -= 3
    return output_grid