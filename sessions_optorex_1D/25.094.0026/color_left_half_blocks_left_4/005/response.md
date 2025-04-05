```python
"""
Transforms a 1D NumPy array of integers (0, 2) based on contiguous subsequences of 2s.
Identifies maximal contiguous subsequences composed solely of the integer 2.
For each sequence of 2s with length L, calculates the number of changes N = (L + (1 if L is even else 0)) // 2.
Changes the last N elements corresponding to this sequence from 2 to 8 in the output array.
Elements 0 and any 2s not part of the last N elements of a sequence remain unchanged.
"""

import numpy as np

def _find_end_of_value_sequence(grid, start_index, target_value):
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
    while i < n and grid[i] == target_value:
        i += 1
    return i

def _calculate_num_changes(seq_length):
    """
    Calculates the number of trailing elements to change based on sequence length L.
    Formula: N = (L + (1 if L is even else 0)) // 2

    Args:
        seq_length: The length (L) of the sequence.

    Returns:
        The number (N) of elements to change.
    """
    is_even = 1 if seq_length % 2 == 0 else 0
    return (seq_length + is_even) // 2

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 1D NumPy array.

    Args:
        input_grid: The 1D NumPy array containing integers 0 and 2.

    Returns:
        The transformed 1D NumPy array containing integers 0, 2, and 8.
    """
    # Initialize output_grid as a copy of the input array
    output_grid = np.copy(input_grid)
    n = len(output_grid)
    i = 0 # Initialize index for iterating through the array

    # Iterate through the array
    while i < n:
        # If the current element is 0, skip it
        if output_grid[i] == 0:
            i += 1
            continue

        # If the current element is 2, find and process the sequence
        if output_grid[i] == 2:
            # Record the start index of the sequence
            seq_start_index = i
            
            # Find the end index (exclusive) of the contiguous sequence of 2s
            seq_end_index = _find_end_of_value_sequence(output_grid, seq_start_index, 2)

            # Calculate the length (L) of the sequence
            seq_length = seq_end_index - seq_start_index

            # Only proceed if a valid sequence was found (should always be > 0 here)
            if seq_length > 0:
                # Calculate the number of trailing 2s to change to 8s
                num_changes = _calculate_num_changes(seq_length)

                # Calculate the starting index for the modification within the sequence
                # change_start_index = seq_start_index + seq_length - num_changes
                change_start_index = seq_end_index - num_changes

                # Modify the output array: Change the last 'num_changes' elements
                # of the sequence (from change_start_index up to seq_end_index) to 8
                # Using slicing for efficiency
                if num_changes > 0:
                    output_grid[change_start_index:seq_end_index] = 8

            # Advance the main index past the processed sequence
            i = seq_end_index
        else:
             # Handle unexpected values defensively (though not expected per task)
             i += 1

    # Return the modified grid
    return output_grid
```