"""
Replaces '0' (white) pixels in the input grid based on these rules:

1. Leading Zeros: At the beginning of each row, before any non-zero pixel, replace all '0's with '5' (gray).
2. Propagation: For remaining '0's, replace them with the value of the nearest non-zero pixel to their left within that row.
3. All-Zero Rows: If a row is all '0's after step 1, if the previous row is all '5's or all of a single color 'c', and did not get its color from its previous row, set the current row to 'c'. Otherwise, set the row to '5'.
"""

import numpy as np

def _get_leftmost_non_zero(row):
    """Finds the index of the leftmost non-zero element in a row."""
    for i, val in enumerate(row):
        if val != 0:
            return i, val
    return -1, 0  # Return -1 if no non-zero element is found

def _is_uniform(row):
    """
    Checks if all elements in the row are the same. Returns the uniform
    value or None.
    """

    first = row[0]
    for x in row:
        if x != first:
            return None
    return first

def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Start with a copy to preserve original non-zero values
    prev_row_uniform_color = None

    for r in range(rows):
        row = input_grid[r]
        leftmost_non_zero_index, _ = _get_leftmost_non_zero(row)

        # Leading Zeros
        if leftmost_non_zero_index > 0 :
            for c in range(leftmost_non_zero_index):
                output_grid[r,c] = 5
        elif leftmost_non_zero_index == -1:
            #handle all zero rows
            if r > 0:
                prev_row_uniform_color = _is_uniform(output_grid[r-1])
                if prev_row_uniform_color is not None:
                    if r>1:
                        prev_prev_row_uniform_color = _is_uniform(output_grid[r-2])
                        if prev_row_uniform_color != prev_prev_row_uniform_color:
                            output_grid[r] = np.full(cols, prev_row_uniform_color)
                        else:
                            output_grid[r] = np.full(cols, 5)
                    else:
                       output_grid[r] = np.full(cols, prev_row_uniform_color)

                else:
                    output_grid[r] = np.full(cols, 5)  # Fill with 5s
            else:
                output_grid[r] = np.full(cols, 5)


        # Propagation
        for c in range(leftmost_non_zero_index + 1, cols):
            if output_grid[r, c] == 0:
                for c_left in range(c - 1, -1, -1):
                    if output_grid[r,c_left] != 0:
                         output_grid[r, c] = output_grid[r, c_left]
                         break


    return output_grid