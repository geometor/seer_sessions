"""
Transforms an input grid based on row-by-row comparisons and cyclic shifts.

The transformation process is as follows:
1. Initialize the output grid as a copy of the input grid.
2. Iterate through the rows of the input grid starting from the second row (index 1).
3. For each odd-indexed row `i`:
    a. Compare row `i` with the previous row `i-1`.
    b. Identify the range of columns where these two rows differ. Find the minimum column index `j` and the maximum column index `k` of these differences.
    c. If there are differences:
        i. Define a segment in row `i` starting from column `j` and ending at column `k+1` (inclusive).
        ii. Extract this segment.
        iii. Perform a right cyclic shift on the extracted segment (the last element moves to the first position).
        iv. Place the shifted segment back into the output grid at the same position (row `i`, columns `j` through `k+1`).
4. Even-indexed rows and pixels outside the identified segments in odd rows remain unchanged.
5. Return the modified output grid.
"""

import numpy as np

def right_cyclic_shift(arr):
    """Performs a right cyclic shift on a 1D numpy array."""
    if arr.size < 2:
        return arr
    # Take the last element and concatenate it with the rest of the array (excluding the last element)
    return np.concatenate(([arr[-1]], arr[:-1]))

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if necessary
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = input_grid_np.copy()
    height, width = output_grid.shape

    # Iterate through rows, starting from the second row (index 1)
    for i in range(1, height):
        # Check if the current row index is odd
        if i % 2 != 0:
            # Get the current row and the previous row
            current_row = input_grid_np[i]
            previous_row = input_grid_np[i-1]

            # Find indices where the rows differ
            diff_indices = np.where(current_row != previous_row)[0]

            # If there are differences
            if diff_indices.size > 0:
                # Find the start (min) and end (max) column index of the differences
                j = np.min(diff_indices)
                k = np.max(diff_indices)

                # Define the segment slice: from j up to k+1 (inclusive).
                # Numpy slicing is exclusive at the end, so we use k+2.
                start_col = j
                end_col = k + 2 # Exclusive index for slicing

                # Ensure end_col does not exceed grid width for extraction
                # (though slicing handles this, explicit check might be safer for understanding)
                actual_end_col_extraction = min(end_col, width)

                # Extract the segment from the current state of the output grid row
                segment = output_grid[i, start_col:actual_end_col_extraction]

                # Perform the right cyclic shift on the segment
                shifted_segment = right_cyclic_shift(segment)

                # Place the shifted segment back into the output grid
                # Ensure end_col does not exceed grid width for assignment
                actual_end_col_assignment = min(end_col, width)
                output_grid[i, start_col:actual_end_col_assignment] = shifted_segment

    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if needed by calling environment
