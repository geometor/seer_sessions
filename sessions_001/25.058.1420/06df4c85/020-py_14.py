"""
1.  **Identify 2x2 Squares:** Locate all 2x2 squares of green (3) or red (2) pixels within the input grid.

2.  **Determine Yellow Stripe:** For each 2x2 square:
    *   Find the nearest column containing yellow (4) pixels to the *right* of the square's starting column. If no such column exists, the object does not get replicated.
    *   Calculate the yellow stripe boundaries based on this yellow column:
        *   `stripe_start = yellow_column - (yellow_column mod 3)`
        *   `stripe_end = stripe_start + 2`

3.  **Replicate within Stripe:** If a yellow stripe is found for a 2x2 square, replicate the 2x2 square bidirectionally (left and right) *within* that stripe.

    *   Replication occurs in steps of 3 units (the width of the stripe).
    *   Replication stops at the stripe boundaries or if it encounters a non-background pixel within the stripe.

4.  **Preservation:** All other pixels in the input grid remain unchanged.

5.  **Output:** Create a new grid reflecting these changes.
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

def find_yellow_column(grid, start_col):
    """Finds the nearest column with yellow (4) to the right of start_col."""
    _, cols = grid.shape
    for c in range(start_col, cols):
        if np.any(grid[:, c] == 4):
            return c
    return -1  # Indicate no yellow column found

def get_stripe_bounds(yellow_column):
    """Calculates stripe boundaries based on a yellow column."""
    stripe_start = yellow_column - (yellow_column % 3)
    stripe_end = stripe_start + 2
    return stripe_start, stripe_end

def transform(input_grid):
    # initialize output_grid
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

        # Find the nearest yellow column to the right
        yellow_column = find_yellow_column(input_grid, c)

        # If no yellow column is found, skip replication
        if yellow_column == -1:
            continue

        # Get stripe boundaries
        stripe_start, stripe_end = get_stripe_bounds(yellow_column)

        # Replicate horizontally within the stripe
        # Replicate to the right
        current_col = c + 3
        while current_col <= stripe_end:
            output_grid[r:r+2, current_col:current_col+2] = color
            current_col += 3

        # Replicate to the left
        current_col = c - 3
        while current_col >= stripe_start:
            output_grid[r:r+2, current_col:current_col+2] = color
            current_col -= 3
    return output_grid