import numpy as np

"""
Transforms the input grid based on a pivot line of 4s.

1. Finds a row or column consisting entirely of the number 4 (the pivot line).
   It is assumed exactly one such line exists.
2. Calculates the new position for the pivot line by reflecting its index across the grid's center.
   For a grid of dimension D and 0-based index i, the new index is (D - 1) - i.
3. If the pivot is a row at index `pivot_row_idx`:
   - Extracts the part of the grid above the pivot (`top_part`) and below the pivot (`bottom_part`).
   - Reflects `top_part` horizontally (flips left-right).
   - Reflects `bottom_part` horizontally (flips left-right).
   - Reconstructs the output grid by placing the horizontally reflected `bottom_part` at the top rows,
     the original `pivot_row` at its new calculated index `new_pivot_row_idx`,
     and the horizontally reflected `top_part` at the bottom rows.
4. If the pivot is a column at index `pivot_col_idx`:
   - Extracts the part of the grid left of the pivot (`left_part`) and right of the pivot (`right_part`).
   - Reflects `left_part` vertically (flips up-down).
   - Reflects `right_part` vertically (flips up-down).
   - Reconstructs the output grid by placing the vertically reflected `right_part` in the leftmost columns,
     the original `pivot_col` at its new calculated index `new_pivot_col_idx`,
     and the vertically reflected `left_part` in the rightmost columns.
5. If the pivot line is exactly in the center, the transformation places the reflected swapped parts
   back into their original sections, potentially resulting in the output being identical to the input
   if the input already possessed the required reflected symmetry across the center.
"""

def find_pivot_row(grid_np):
    """Finds the index of a row composed entirely of 4s."""
    D = grid_np.shape[0]
    for r in range(D):
        # Check if all elements in the row are 4
        if np.all(grid_np[r, :] == 4):
            return r
    return -1 # Not found

def find_pivot_col(grid_np):
    """Finds the index of a column composed entirely of 4s."""
    D = grid_np.shape[1]
    for c in range(D):
        # Check if all elements in the column are 4
        if np.all(grid_np[:, c] == 4):
            return c
    return -1 # Not found

def transform(input_grid):
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Get grid dimension (assuming square grid)
    D = input_np.shape[0]
    # Initialize output grid with zeros
    output_np = np.zeros_like(input_np)

    # Try to find a pivot row (a row full of 4s)
    pivot_row_idx = find_pivot_row(input_np)

    if pivot_row_idx != -1:
        # Pivot is a row
        # Extract the pivot row itself
        pivot_row = input_np[pivot_row_idx, :]
        # Calculate the new index for the pivot row after transformation
        new_pivot_row_idx = (D - 1) - pivot_row_idx

        # Extract the parts of the grid above and below the pivot row
        top_part = input_np[0:pivot_row_idx, :]
        bottom_part = input_np[pivot_row_idx+1:D, :]

        # Reflect these parts horizontally (left-right flip)
        flipped_top = np.fliplr(top_part)
        flipped_bottom = np.fliplr(bottom_part)

        # Construct the output grid:
        # Place the flipped bottom part at the top
        if flipped_bottom.shape[0] > 0:
            output_np[0:flipped_bottom.shape[0], :] = flipped_bottom
        # Place the original pivot row at its new calculated position
        output_np[new_pivot_row_idx, :] = pivot_row
        # Place the flipped top part at the bottom
        if flipped_top.shape[0] > 0:
            # Calculate the starting row index for the flipped top part
            start_row_for_flipped_top = D - flipped_top.shape[0]
            output_np[start_row_for_flipped_top:D, :] = flipped_top

    else:
        # If no pivot row was found, try to find a pivot column
        pivot_col_idx = find_pivot_col(input_np)
        if pivot_col_idx != -1:
            # Pivot is a column
            # Extract the pivot column itself
            pivot_col = input_np[:, pivot_col_idx]
            # Calculate the new index for the pivot column after transformation
            new_pivot_col_idx = (D - 1) - pivot_col_idx

            # Extract the parts of the grid left and right of the pivot column
            left_part = input_np[:, 0:pivot_col_idx]
            right_part = input_np[:, pivot_col_idx+1:D]

            # Reflect these parts vertically (up-down flip)
            flipped_left = np.flipud(left_part)
            flipped_right = np.flipud(right_part)

            # Construct the output grid:
            # Place the flipped right part on the left
            if flipped_right.shape[1] > 0:
                 output_np[:, 0:flipped_right.shape[1]] = flipped_right
            # Place the original pivot column at its new calculated position
            output_np[:, new_pivot_col_idx] = pivot_col
            # Place the flipped left part on the right
            if flipped_left.shape[1] > 0:
                 # Calculate the starting column index for the flipped left part
                 start_col_for_flipped_left = D - flipped_left.shape[1]
                 output_np[:, start_col_for_flipped_left:D] = flipped_left
        else:
            # Defensive case: If no pivot line (row or column of 4s) is found,
            # return the original grid. This shouldn't happen based on provided examples.
             output_np = input_np

    # Convert the resulting numpy array back to a list of lists
    return output_np.tolist()