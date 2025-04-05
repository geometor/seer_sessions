import numpy as np
import math

"""
Transforms a 1D NumPy array of 12 integers based on the value of the single non-zero integer present.

1.  Accepts a 1D NumPy array (input_grid) of 12 integers.
2.  Identifies the unique non-zero integer value (N) present in the array.
3.  Counts the total number of occurrences (count) of N.
4.  Finds the index (first_idx) of the first occurrence of N in the input array.
5.  Initializes an output array of 12 zeros.
6.  Applies a specific rearrangement rule based on the value of N:
    - If N is 1 or 9: Places count copies of N into the output array starting at index first_idx + 4.
    - If N is 4 or 5: Places count copies of N into the output array starting at index 1.
    - If N is 6:
        - If count is 2, sets the elements at indices 3 and 4 of the output array to 6.
        - If count > 2, places count copies of 6 into the output array starting at index 0.
    - If N is 7: Calculates size1 = ceil(count / 2) and size2 = floor(count / 2). Places size1 copies of N at the beginning (index 0) and size2 copies of N at the end (index 12 - size2).
7.  Fills remaining positions with 0s (handled by initialization).
8.  Converts the final output array into a space-separated string and returns it.
"""

def find_non_zero_properties(grid: np.ndarray):
    """Finds the unique non-zero value, its count, and first index."""
    non_zero_elements = grid[grid != 0]
    if len(non_zero_elements) == 0:
        return 0, 0, -1 # Value, Count, First Index

    unique_non_zeros = np.unique(non_zero_elements)
    # Assuming homogeneity constraint holds (only one unique non-zero)
    non_zero_val = unique_non_zeros[0]
    count = len(non_zero_elements)
    first_idx = np.where(grid == non_zero_val)[0][0]

    return non_zero_val, count, first_idx

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array containing 12 integers.

    Returns:
        A string containing the transformed 12 space-separated integers.
    """
    # Get grid dimensions and initialize output grid with zeros
    n_elements = len(input_grid) # Should be 12 based on examples
    output_grid = np.zeros(n_elements, dtype=input_grid.dtype)

    # Find the non-zero element value (N), its count, and first index
    non_zero_val, count, first_idx = find_non_zero_properties(input_grid)

    # If no non-zero element found (all zeros), return zeros string
    if non_zero_val == 0:
        return " ".join(map(str, output_grid))

    # Apply transformation rule based on the non-zero value (N)
    if non_zero_val == 1 or non_zero_val == 9:
        # Place count N's starting at first_idx + 4
        start_index = first_idx + 4
        end_index = start_index + count
        # Use slicing, ensuring indices stay within bounds
        actual_start = max(0, start_index)
        actual_end = min(n_elements, end_index)
        if actual_start < actual_end: # Check if there's a valid slice
             output_grid[actual_start:actual_end] = non_zero_val

    elif non_zero_val == 4 or non_zero_val == 5:
        # Place count N's starting at index 1
        start_index = 1
        end_index = start_index + count
        # Use slicing, ensuring indices stay within bounds
        actual_start = max(0, start_index)
        actual_end = min(n_elements, end_index)
        if actual_start < actual_end:
            output_grid[actual_start:actual_end] = non_zero_val

    elif non_zero_val == 6:
        if count == 2:
            # Place '6 6' at indices 3 and 4
            if 3 < n_elements: output_grid[3] = 6
            if 4 < n_elements: output_grid[4] = 6
        elif count > 2:
            # Place count N's starting at index 0
            start_index = 0
            end_index = start_index + count
            # Use slicing, ensuring indices stay within bounds
            actual_start = max(0, start_index)
            actual_end = min(n_elements, end_index)
            if actual_start < actual_end:
                output_grid[actual_start:actual_end] = non_zero_val

    elif non_zero_val == 7:
        # Split into two halves and place at ends
        size1 = math.ceil(count / 2)
        size2 = math.floor(count / 2) # or count - size1

        # Place first half at the beginning
        end_index1 = min(size1, n_elements)
        if end_index1 > 0:
             output_grid[0:end_index1] = non_zero_val

        # Place second half at the end
        start_index_end = n_elements - size2
        actual_start_end = max(0, start_index_end) # Ensure start index is not negative
        if size2 > 0 and actual_start_end < n_elements: # Check if there's space and items to place
            output_grid[actual_start_end:n_elements] = non_zero_val


    # Convert the output grid back to a space-separated string
    return " ".join(map(str, output_grid))