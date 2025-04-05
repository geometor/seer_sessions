import numpy as np
import collections

"""
Transforms a grid of single-digit integers. 
The rule is to identify the most frequent non-zero digit in the entire input grid. 
Then, create a new grid of the same dimensions where every non-zero digit from the input is replaced by this most frequent non-zero digit. 
Digits that are 0 in the input remain 0 in the output.
"""

def find_most_frequent_non_zero(numbers):
    """
    Finds the most frequent non-zero number in an iterable of numbers.

    Args:
        numbers: An iterable (e.g., list, numpy array) containing numbers.

    Returns:
        The most frequent non-zero number, or None if no non-zero numbers exist.
    """
    # Filter out zeros
    non_zeros = [n for n in numbers if n != 0]
    
    # Handle edge case: no non-zero numbers
    if not non_zeros:
        return None
        
    # Count frequencies of non-zero numbers
    counts = collections.Counter(non_zeros)
    
    # Find the number with the highest frequency
    # most_common(1) returns list of [(element, count)]
    most_frequent = counts.most_common(1)[0][0]
    return most_frequent

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A numpy array representing the grid of single-digit integers.

    Returns:
        A numpy array containing the transformed grid.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Flatten the grid to easily find the most frequent non-zero digit across all elements
    flat_list = input_grid.flatten()

    # Find the most frequent non-zero digit in the flattened list
    replacement_digit = find_most_frequent_non_zero(flat_list)

    # Only perform replacement if there was at least one non-zero digit found
    if replacement_digit is not None:
        # Iterate through each element of the grid
        # Using np.nditer for efficient iteration over multi-dimensional arrays
        it = np.nditer(output_grid, flags=['multi_index'], op_flags=['readwrite'])
        while not it.finished:
            idx = it.multi_index
            # Check if the current element is non-zero
            if output_grid[idx] != 0:
                # Replace non-zero elements with the most frequent non-zero digit
                output_grid[idx] = replacement_digit
            # Move to the next element
            it.iternext()
    # If replacement_digit is None (all zeros in input), output_grid remains a copy of input_grid

    return output_grid