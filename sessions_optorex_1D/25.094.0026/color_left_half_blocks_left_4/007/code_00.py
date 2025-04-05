"""
Transforms a 1D NumPy array of integers (0, 2) based on contiguous subsequences of 2s.
Identifies maximal contiguous subsequences composed solely of the integer 2.
For each sequence of 2s with length L, calculates the number of changes N = (L + (1 if L is even else 0)) // 2.
Changes the last N elements corresponding to this sequence from 2 to 8 in the output array.
Elements 0 and any 2s not part of the last N elements of a sequence remain unchanged.
"""

import numpy as np

def _find_end_of_value_sequence(grid: np.ndarray, start_index: int, target_value: int) -> int:
    """
    Finds the index immediately after the end of a contiguous sequence
    of target_value in a 1D NumPy array.

    Args:
        grid: The 1D NumPy array.
        start_index: The index to start searching from.
        target_value: The integer value to look for in the sequence.

    Returns:
        The index after the last element of the sequence.
    """
    i = start_index
    n = len(grid)
    # Iterate forward as long as we are within bounds and find the target value
    while i < n and grid[i] == target_value:
        i += 1
    return i # Return the index *after* the sequence ends

def _calculate_num_changes(seq_length: int) -> int:
    """
    Calculates the number of trailing elements to change based on sequence length L.
    Formula: N = (L + (1 if L is even else 0)) // 2

    Args:
        seq_length: The length (L) of the sequence.

    Returns:
        The number (N) of elements to change.
    """
    # Check if the sequence length is even
    is_even = 1 if seq_length % 2 == 0 else 0
    # Apply the formula using integer division
    return (seq_length + is_even) // 2

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 1D NumPy array.

    Args:
        input_grid: The 1D NumPy array containing integers 0 and 2.

    Returns:
        The transformed 1D NumPy array containing integers 0, 2, and 8.
    """
    # Initialize output_grid as a copy of the input array to avoid modifying the original
    output_grid = np.copy(input_grid)
    n = len(output_grid)
    i = 0 # Initialize index for iterating through the array

    # Iterate through the array elements
    while i < n:
        # Check the value at the current index
        current_value = output_grid[i]

        # If the current element is 0, it acts as a boundary, so skip it
        if current_value == 0:
            i += 1
            continue # Move to the next element

        # If the current element is 2, we've found the start of a potential sequence
        if current_value == 2:
            # Record the start index of the sequence
            seq_start_index = i
            
            # Use helper function to find the index *after* the end of the contiguous sequence of 2s
            seq_end_index = _find_end_of_value_sequence(output_grid, seq_start_index, 2)

            # Calculate the length (L) of the found sequence
            seq_length = seq_end_index - seq_start_index

            # If a sequence of length > 0 was indeed found
            if seq_length > 0:
                # Use helper function to calculate the number (N) of trailing 2s to change to 8s
                num_changes = _calculate_num_changes(seq_length)

                # Only proceed with modification if N > 0
                if num_changes > 0:
                    # Calculate the starting index for the modification (N elements from the end)
                    change_start_index = seq_end_index - num_changes

                    # Modify the output array: Change the values of the last 'num_changes' elements
                    # of the sequence (from change_start_index up to seq_end_index) to 8.
                    # NumPy slicing allows efficient in-place modification of this segment.
                    output_grid[change_start_index:seq_end_index] = 8

            # Advance the main iteration index 'i' to the position immediately after the processed sequence
            # This prevents reprocessing parts of the sequence or skipping elements.
            i = seq_end_index
        
        # Handle unexpected values defensively (though input guarantees only 0 and 2)
        else: 
             i += 1 # Simply move to the next element if it's not 0 or 2

    # Return the modified grid
    return output_grid