"""
Processes an input grid containing white pixels (0) and objects of a single non-white color.
It fills columns that were entirely white in the input with gray (5).
Then, it fills rows that were entirely white in the input with the object's color,
but only in positions that were not already filled with gray.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 1. Find the single non-white object color
    object_color = 0
    unique_colors = np.unique(input_np)
    for color in unique_colors:
        if color != 0:
            object_color = color
            break
    # Handle edge case where grid might be all white (though unlikely based on examples)
    if object_color == 0:
        return input_grid # Or decide on specific behavior for all-white input

    # 2. Identify columns that are all white (0) in the input
    empty_col_indices = []
    for c in range(width):
        if np.all(input_np[:, c] == 0):
            empty_col_indices.append(c)

    # 3. Fill identified columns in the output grid with gray (5)
    for c in empty_col_indices:
        output_np[:, c] = 5

    # 4. Identify rows that are all white (0) in the input
    empty_row_indices = []
    for r in range(height):
        if np.all(input_np[r, :] == 0):
            empty_row_indices.append(r)

    # 5. Fill identified rows in the output grid with object_color,
    #    but only if the pixel hasn't already been changed to gray (5)
    for r in empty_row_indices:
        for c in range(width):
            # Check the *current* state of the output grid pixel
            if output_np[r, c] == 0: # Only change if it's still white
                output_np[r, c] = object_color

    # Convert the result back to a list of lists
    return output_np.tolist()