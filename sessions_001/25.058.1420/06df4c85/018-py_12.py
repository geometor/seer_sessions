"""
1.  **Identify Yellow Stripes:** The grid is divided into vertical stripes that are 3 units wide. The pattern begins with two columns of any color, followed by a column of yellow.

2.  **Identify 2x2 Squares:** Locate 2x2 squares of green (3) or red (2) pixels within the grid.

3.  **Conditional Replication:**
    *   For each identified 2x2 square, determine the boundaries of the yellow stripe it resides in. The yellow stripe is the column of yellow pixels that either contains the square or, if the square starts to the left of a yellow column, includes the yellow column to the right of the start position.
    *   Replicate the 2x2 square bidirectionally *within* the yellow stripe.
    * The replication stops when it reaches the edge of the yellow stripe or another non-yellow pixel within that stripe. The replication moves 3 units at a time (one full stripe width).
    * If an object begins outside the yellow stripe (in the first two columns) it is replicated *into* the yellow stripe.

4.  **Preservation:** All other pixels remain unchanged.

5. **Output:** A new grid is created reflecting these changes.
"""

import numpy as np

def find_objects(grid, color, size=2):
    """Finds all 2x2 squares of a given color."""
    objects = []
    rows, cols = grid.shape
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if np.all(grid[r:r+size, c:c+size] == color):
                objects.append((r, c))
    return objects

def get_stripe_bounds(col, grid_width):
    """Calculates the start and end columns of the yellow stripe."""
    stripe_start = col
    while stripe_start >= 0 and (stripe_start % 3) != 2:
        stripe_start -= 1
    stripe_end = col
    while stripe_end < grid_width and (stripe_end % 3) != 1:
        stripe_end += 1
    return stripe_start, stripe_end


def transform(input_grid):
    """Transforms the input grid according to the rules."""
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
        if stripe_start < 0:
            stripe_start = 0

        # Replicate horizontally within stripe
        # First, replicate to the right
        current_col = c + 3
        while current_col <= stripe_end-1:
            output_grid[r:r+2, current_col:current_col+2] = color
            current_col += 3

        # Then, replicate to the left.
        current_col = c - 3
        while current_col >= stripe_start:
            output_grid[r:r+2, current_col:current_col+2] = color
            current_col -= 3
    return output_grid