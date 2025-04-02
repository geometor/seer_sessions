import numpy as np

"""
Transforms an input grid by processing each row independently. For each row, it identifies the unique non-white color (if any) and finds the column indices of its first and last occurrences. It then fills the segment between these first and last columns (inclusive) in the output grid's corresponding row with that non-white color. Rows containing only the background color (white=0) remain unchanged.
"""

def find_row_span_and_color(row):
    """
    Finds the non-white color and its start/end column indices in a single row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (non_white_color, start_col, end_col)
               Returns (None, -1, -1) if no non-white color is found in the row.
    """
    non_white_color = None
    start_col = -1
    end_col = -1

    # Find indices of all non-zero elements
    non_zero_indices = np.where(row != 0)[0]

    if len(non_zero_indices) > 0:
        # Get the color of the first non-white pixel (assumption: only one non-white color per row)
        first_nz_index = non_zero_indices[0]
        non_white_color = row[first_nz_index]

        # Find the indices specifically for this color
        color_indices = np.where(row == non_white_color)[0]
        if len(color_indices) > 0:
             start_col = color_indices[0]
             end_col = color_indices[-1]
        # else: # Should not happen based on how non_white_color was found, but good practice
        #     return None, -1, -1

    return non_white_color, start_col, end_col


def transform(input_grid):
    """
    Applies the row-wise fill transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(rows):
        current_row = input_grid[r, :]

        # Find the non-white color and its span in the current row
        non_white_color, start_col, end_col = find_row_span_and_color(current_row)

        # If a non-white color and a valid span were found in this row
        if non_white_color is not None and start_col != -1:
            # Fill the corresponding segment in the output grid's row
            # Note: Slicing includes start_col but excludes end_col + 1, hence the +1
            output_grid[r, start_col : end_col + 1] = non_white_color

    # Return the modified output grid
    return output_grid