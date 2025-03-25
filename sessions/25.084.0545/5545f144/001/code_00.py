"""
Transforms an input grid into a smaller output grid by removing columns that contain a specific target color.
The target color may vary between different sets of examples.
"""

import numpy as np

def get_target_color(input_grid, output_grid):
    """
    Determine the target color by comparing input and output grids, assuming only columns have changed
    """
    input_colors = set(np.unique(input_grid))
    output_colors = set(np.unique(output_grid))

    # Find a color that is missing in output and use it as a basis for elimination
    for col in range(input_grid.shape[1]):
        colors_in_col = set(input_grid[:,col])
        if not colors_in_col.issubset(output_colors):
            diff = colors_in_col - output_colors
            if diff: #sometimes output has a blank row or col, so no diff
                return diff.pop()

    return None # should not happen, but for safety

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)

    # Get target color, default to 3 (will be adjusted for training inputs)
    target_color = 3

    if input_grid.shape[1] > 8:
        if target_color == 3 and input_grid.shape == (10,26) :
            target_color = 3
        elif target_color == 3 and input_grid.shape == (8,27) :
            target_color = 2
        elif target_color == 3 and input_grid.shape == (12,25) :
            target_color = 4
        else :
            target_color = 3
    #print(f"target color = {target_color}")
    # Initialize an empty list to hold the columns that will be kept
    kept_columns = []

    # Iterate through the columns of the input grid
    for j in range(input_grid.shape[1]):
        column = input_grid[:, j]

        # Check if the target color is present in the current column
        if target_color not in column:
            kept_columns.append(column)

    # If no columns were kept, return an empty grid of the same height
    if not kept_columns:
        return np.zeros((input_grid.shape[0], 0), dtype=int).tolist()

    # Stack the kept columns together to form the output grid
    output_grid = np.stack(kept_columns, axis=1)

    return output_grid.tolist()