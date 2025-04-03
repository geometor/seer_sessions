import numpy as np
import collections

"""
Identify the primary foreground color (non-white/0) in the input grid.
Iterate through each row of the input grid and count the occurrences of this foreground color.
Determine the row index that contains the maximum count of the foreground color. If multiple rows share the maximum count, select the topmost row (smallest row index).
Create an output grid of the same dimensions as the input, filled entirely with the background color (white/0).
Copy the selected row from the input grid into the corresponding row of the output grid.
Return the modified output grid.
"""

def find_foreground_color(grid):
    """Finds the first non-zero color in the grid."""
    for row in grid:
        for pixel in row:
            if pixel != 0:
                return pixel
    return 0 # Return background color if no foreground color is found

def transform(input_grid):
    """
    Transforms the input grid by selecting the row with the most foreground pixels
    and placing it in an otherwise background-filled grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize output_grid with background color (0)
    output_array = np.zeros_like(input_array)

    # Identify the foreground color
    # Assumes only one foreground color exists besides background (0)
    foreground_color = find_foreground_color(input_array)

    # If no foreground color exists (grid is all background), return the all-background grid
    if foreground_color == 0:
        return output_array.tolist()

    # Initialize variables to track the row with the maximum count
    max_count = -1
    selected_row_index = -1

    # Iterate through each row to find the one with the most foreground pixels
    for r in range(height):
        # Count occurrences of the foreground color in the current row
        current_count = np.count_nonzero(input_array[r, :] == foreground_color)

        # Update max_count and selected_row_index if current count is higher
        # We only update if strictly greater, ensuring the first row is kept in case of ties
        if current_count > max_count:
            max_count = current_count
            selected_row_index = r

    # If a row with foreground pixels was found (max_count > 0 implies selected_row_index is valid)
    if selected_row_index != -1:
        # Copy the selected row from the input to the output grid
        output_array[selected_row_index, :] = input_array[selected_row_index, :]

    # Convert the numpy array back to a list of lists for the standard ARC format
    return output_array.tolist()