"""
Fill white rows below a gray separator based on a repeating color pattern from the row above the separator.

1. Create a copy of the input grid to serve as the initial output grid.
2. Locate the row index (separator_index) of the first row that consists entirely of gray (5) pixels.
3. Extract the sequence of colors (pattern_colors) from the row directly above the separator row (at separator_index - 1).
4. Iterate through each row index `r` starting from the row immediately below the separator row (separator_index + 1) down to the last row of the grid.
5. For each row `r`:
    a. Calculate the position of this row relative to the first row being filled: relative_row_index = r - (separator_index + 1).
    b. Determine the index into the pattern_colors sequence by taking the relative_row_index modulo the number of colors in the pattern_colors sequence: color_index = relative_row_index % len(pattern_colors).
    c. Select the color (fill_color) from pattern_colors at the calculated color_index.
    d. Modify the output grid by filling the entire row `r` with the fill_color.
6. Return the modified output grid.
"""

import numpy as np

def find_separator_row(grid):
    """Finds the index of the first row consisting entirely of gray (5) pixels."""
    for r, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return r
    return -1 # Indicate not found, though problem description implies it always exists

def transform(input_grid):
    """
    Fills white rows below a gray separator based on a repeating color pattern
    from the row above the separator.
    """
    # Convert input to numpy array for easier manipulation
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.copy(input_arr)
    height, width = input_arr.shape

    # 1. Locate the separator row
    separator_index = find_separator_row(input_arr)

    if separator_index == -1 or separator_index == 0:
        # Handle cases where separator is not found or is the first row (no pattern row)
        # Based on examples, this shouldn't happen, but good practice.
        return output_arr.tolist() # Return unmodified copy

    # 2. Extract the pattern colors from the row above the separator
    pattern_colors = input_arr[separator_index - 1]

    # 3. Iterate through rows below the separator
    for r in range(separator_index + 1, height):
        # Check if the row is supposed to be filled (originally white)
        # While the description says the target area is white, the logic
        # just fills based on position regardless of original content below separator.
        # Let's follow the pattern repetition logic directly.

        # a. Calculate relative row index
        relative_row_index = r - (separator_index + 1)

        # b. Calculate pattern color index using modulo
        pattern_length = len(pattern_colors)
        if pattern_length == 0: # Avoid division by zero if pattern row is empty
             continue
        color_index = relative_row_index % pattern_length

        # c. Select the fill color
        fill_color = pattern_colors[color_index]

        # d. Fill the entire row in the output grid
        output_arr[r, :] = fill_color

    # Return the result as a list of lists
    return output_arr.tolist()