"""
1.  **Find the Blue Stripe:** Examine the input grid to locate a vertical stripe composed entirely of blue (1) pixels.
2.  **Record Stripe Index:** Note the column index (x-coordinate) where the blue stripe is found.
3.  **Extract Column:** Get all of the pixel values from the input grid at the recorded column.
4.  **Transform Column:** Within this extracted column, *only* replace the blue (1) pixels with azure (8) pixels. Leave other pixel colors unchanged.
5.  **Create Output:** Construct a new grid with a width of 3 and the same height as the input grid.
6.  **Populate Center Column:** Fill the center column of the new grid with transformed values.
7.  **Pad with White:** Fill the left and right columns of the output grid with white (0) pixels.
"""

import numpy as np

def find_vertical_stripe(grid, color):
    """Finds the index of a vertical stripe of the specified color."""
    height, width = grid.shape
    for x in range(width):
        is_stripe = True
        for y in range(height):
            if grid[y, x] != color:
                is_stripe = False
                break
        if is_stripe:
            return x
    return -1

def transform(input_grid):
    # 1. Find the Blue Stripe and its index.
    blue_stripe_index = find_vertical_stripe(input_grid, 1)

    # Initialize the height and padding
    height = input_grid.shape[0]
    preceding_columns = 1
    following_columns = 1

    # 2. If no blue stripe is found, return an empty grid
    if blue_stripe_index == -1:
        return np.zeros((input_grid.shape[0], 3), dtype=int)

    # 3. Extract Column
    extracted_column = input_grid[:, blue_stripe_index]

    # 4. Transform Column: Corrected selective replacement
    transformed_column = extracted_column.copy()  # Create a copy to modify
    transformed_column[transformed_column == 1] = 8  # Only replace 1s with 8s

    # 5. Construct Output Grid
    output_grid = np.zeros((height, preceding_columns + 1 + following_columns), dtype=int)

    # 6. Populate Center Column
    output_grid[:, preceding_columns] = transformed_column

    # 7. Pad with white (already done by initialization with zeros)

    return output_grid