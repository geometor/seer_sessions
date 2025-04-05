import numpy as np

"""
Transforms an input NumPy array of integers.
Finds the index of the first non-zero integer in the array.
If a non-zero integer is found at index 'i', a new array is constructed by:
1. Taking the slice of the input array from the start up to index 'i'.
2. Appending an array of three zero elements: [0, 0, 0].
3. Appending the slice of the input array from index 'i' to the end.
The resulting array is then truncated to match the original input array length.
If the input array contains only zeros, it is returned unchanged.
"""

def find_first_non_zero_index(arr):
    """
    Finds the index of the first non-zero element in a NumPy array.

    Args:
        arr: A NumPy array of integers.

    Returns:
        The index of the first non-zero element, or -1 if all elements are zero.
    """
    # Find indices of non-zero elements
    non_zero_indices = np.nonzero(arr)[0]
    # If there are non-zero elements, return the first index
    if non_zero_indices.size > 0:
        return non_zero_indices[0]
    # Otherwise, return -1
    return -1

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array containing the transformed sequence.
    """
    # Determine the original length of the input array
    original_length = len(input_grid)

    # Find the index of the first non-zero element
    first_non_zero_idx = find_first_non_zero_index(input_grid)

    # Handle the edge case where all elements are zero
    if first_non_zero_idx == -1:
        # Return the original array if no non-zero elements found
        return input_grid

    # Construct the new sequence if a non-zero element is found
    # 1. Slice before the first non-zero element
    part1 = input_grid[:first_non_zero_idx]
    # 2. Define the three zeros to insert
    zeros_to_insert = np.array([0, 0, 0], dtype=input_grid.dtype)
    # 3. Slice from the first non-zero element onwards
    part2 = input_grid[first_non_zero_idx:]

    # Concatenate the parts to form the modified sequence
    output_grid_intermediate = np.concatenate((part1, zeros_to_insert, part2))

    # Truncate the sequence to the original length
    output_grid = output_grid_intermediate[:original_length]

    return output_grid