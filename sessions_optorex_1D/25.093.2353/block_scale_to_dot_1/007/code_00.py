import numpy as np

"""
The transformation rule operates on a 1D NumPy array of integers. It identifies
all occurrences of the integer '2'. For each '2', it checks its immediate left
and right neighbors based on the *original* input array. If a neighbor is '0',
it identifies the full contiguous block of '0's extending away from the '2' in
that direction, again based on the original input. It then looks at the element
immediately bordering this block of '0's on the side opposite the '2' in the
original input. If this bordering element exists (is within the array bounds)
and is non-zero, the entire contiguous block of '0's in the *output* array is
replaced with the value of that non-zero bordering element. This check and
potential replacement are performed independently for the left and right sides
of each '2' found in the array. If no '2' is present, or if the conditions for
replacement (adjacent '0' block bordered by a non-zero digit) are not met for
a given side, the corresponding section of the output array remains unchanged
from the initial copy of the input.
"""

def find_contiguous_zeros_left(grid, start_index):
    """Finds the start index of a contiguous block of zeros ending just before start_index."""
    current_index = start_index - 1
    # Check initial condition: must be a 0 at start_index - 1
    if current_index < 0 or grid[current_index] != 0:
        return -1, -1 # No zero block found immediately left

    zero_start = current_index
    # Scan leftwards
    while zero_start > 0 and grid[zero_start - 1] == 0:
        zero_start -= 1
    return zero_start, current_index # Return start and end index of the zero block

def find_contiguous_zeros_right(grid, start_index):
    """Finds the end index of a contiguous block of zeros starting just after start_index."""
    n = len(grid)
    current_index = start_index + 1
     # Check initial condition: must be a 0 at start_index + 1
    if current_index >= n or grid[current_index] != 0:
        return -1, -1 # No zero block found immediately right

    zero_end = current_index
    # Scan rightwards
    while zero_end < n - 1 and grid[zero_end + 1] == 0:
        zero_end += 1
    return current_index, zero_end # Return start and end index of the zero block


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the zero-filling rule adjacent to '2's based on bordering non-zero digits.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the transformed sequence of integers.
    """
    # Initialize output_grid as a copy of the input to allow modifications
    # All checks for conditions (locations of 2s, 0s, fill digits) will be done
    # on the original input_grid, but modifications will be applied to output_grid.
    output_grid = np.copy(input_grid)
    n = len(input_grid)

    # Find indices of all elements equal to 2 in the original input
    two_indices = np.where(input_grid == 2)[0]

    # Iterate through each index where a '2' was found in the input
    for idx in two_indices:

        # --- Check Left Side ---
        # Find the contiguous block of zeros immediately to the left of the '2'
        zero_start_left, zero_end_left = find_contiguous_zeros_left(input_grid, idx)

        # If a zero block was found (indices are valid)
        if zero_start_left != -1:
            # Check the element bordering the zero block on the far left in the input_grid
            fill_digit_idx_left = zero_start_left - 1
            # Ensure the border index is valid
            if fill_digit_idx_left >= 0:
                fill_digit_left = input_grid[fill_digit_idx_left]
                # If the bordering element is non-zero, fill the zeros in the output grid
                if fill_digit_left != 0:
                    # Modify the output_grid in the range of the zero block
                    output_grid[zero_start_left : zero_end_left + 1] = fill_digit_left

        # --- Check Right Side ---
        # Find the contiguous block of zeros immediately to the right of the '2'
        zero_start_right, zero_end_right = find_contiguous_zeros_right(input_grid, idx)

        # If a zero block was found (indices are valid)
        if zero_start_right != -1:
            # Check the element bordering the zero block on the far right in the input_grid
            fill_digit_idx_right = zero_end_right + 1
            # Ensure the border index is valid
            if fill_digit_idx_right < n:
                fill_digit_right = input_grid[fill_digit_idx_right]
                # If the bordering element is non-zero, fill the zeros in the output grid
                if fill_digit_right != 0:
                     # Modify the output_grid in the range of the zero block
                    output_grid[zero_start_right : zero_end_right + 1] = fill_digit_right

    # Return the modified grid
    return output_grid