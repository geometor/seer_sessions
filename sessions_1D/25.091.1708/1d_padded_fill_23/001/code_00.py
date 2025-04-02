"""
Transforms the input grid based on the following rules applied row by row:
1. Iterate through each row of the input grid independently.
2. Identify all non-white (non-zero) pixels in the current row.
3. If exactly one non-white pixel exists in the row:
    - Let its color be C and its column index be c.
    - Fill the row in the output grid from column c to the end (right edge) with color C.
4. If two or more non-white pixels exist in the row AND they all have the same color C:
    - Find the leftmost column index (c_left) and the rightmost column index (c_right) of these non-white pixels.
    - Fill the row in the output grid from column c_left to c_right (inclusive) with color C.
5. Otherwise (zero non-white pixels, or multiple non-white pixels of different colors):
    - The row in the output grid remains unchanged from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Find non-white pixels in the current row
        non_white_indices = np.where(input_grid[r] != 0)[0]
        num_non_white = len(non_white_indices)

        # If there are non-white pixels
        if num_non_white > 0:
            # Get the colors of these pixels
            non_white_colors = input_grid[r, non_white_indices]
            unique_colors = np.unique(non_white_colors)

            # Case 1: Exactly one non-white pixel
            if num_non_white == 1:
                color = unique_colors[0]
                col_index = non_white_indices[0]
                # Fill from this pixel to the right edge
                output_grid[r, col_index:] = color

            # Case 2: Multiple non-white pixels, all of the same color
            elif num_non_white > 1 and len(unique_colors) == 1:
                color = unique_colors[0]
                col_left = non_white_indices[0] # np.where guarantees sorted indices
                col_right = non_white_indices[-1]
                # Fill between the leftmost and rightmost non-white pixels (inclusive)
                output_grid[r, col_left:col_right + 1] = color
            
            # Case 3: Multiple non-white pixels of different colors (implicit 'else')
            # No change needed as output_grid started as a copy

        # Case 4: Row has only white pixels (implicit 'else')
        # No change needed

    return output_grid