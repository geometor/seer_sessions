"""
Accepts an input sequence (list or NumPy array) of 12 integers.
Keeps the first 4 elements (which are assumed to be [0, 0, 0, 0] based on examples).
Identifies the unique non-zero integer (X) in the elements from index 4 to 11.
Replaces the elements from index 4 to 11 with the fixed pattern [X, X, X, 0, X, X, 0, X].
Returns the modified 12-element sequence, preserving the input type (list or NumPy array).
"""

import numpy as np
from typing import List, Union

# Define types for clarity, assuming input can be list or ndarray
InputType = Union[List[int], np.ndarray]
OutputType = Union[List[int], np.ndarray]

def find_non_zero_digit(sub_sequence: InputType) -> int:
    """
    Finds the first (and assumed unique) non-zero digit in a subsequence.

    Args:
        sub_sequence: A list or NumPy array slice containing integers.

    Returns:
        The non-zero integer found.

    Raises:
        ValueError: If no non-zero digit is found in the subsequence.
    """
    # Iterate through the elements of the subsequence
    for digit in sub_sequence:
        # Check if the digit is not zero
        if digit != 0:
            # Return the non-zero digit as an integer
            return int(digit)
    # If the loop completes without finding a non-zero digit, raise an error
    # (This case is not expected based on the provided examples)
    raise ValueError("No non-zero digit found in the expected segment (indices 4-11).")

def transform(input_grid: InputType) -> OutputType:
    """
    Transforms the input sequence according to the specified rule.

    Args:
        input_grid: A 12-element sequence (list or NumPy array) of integers.

    Returns:
        A 12-element sequence (list or NumPy array, matching input type)
        with the transformation applied.

    Raises:
        ValueError: If the input sequence does not have exactly 12 elements.
        TypeError: If the input is not a list or NumPy array.
    """
    # Initialize output_grid as a copy of the input to preserve type and initial structure
    # Using list() for lists or .copy() for numpy arrays ensures modification doesn't affect original input
    if isinstance(input_grid, np.ndarray):
        # Create a copy if it's a numpy array
        output_grid = input_grid.copy()
    elif isinstance(input_grid, list):
        # Create a copy if it's a list
        output_grid = list(input_grid)
    else:
        # Handle unexpected input types
        raise TypeError("Input must be a sequence type like list or numpy array.")

    # Validate the length of the input sequence
    if len(output_grid) != 12:
         raise ValueError("Input sequence must have exactly 12 elements.")

    # Isolate the segment from index 4 to 11 (inclusive) from the original input
    # This segment contains the pattern to be analyzed
    variable_segment = input_grid[4:12]

    # Find the unique non-zero digit 'X' within this variable segment
    non_zero_x = find_non_zero_digit(variable_segment)

    # Define the fixed target pattern using the identified non-zero digit 'X'
    # The pattern is [X, X, X, 0, X, X, 0, X]
    target_pattern_segment = [
        non_zero_x, non_zero_x, non_zero_x, 0,
        non_zero_x, non_zero_x, 0, non_zero_x
    ]

    # Overwrite the corresponding segment (indices 4 through 11) in the output_grid
    # Slice assignment works for both Python lists and NumPy arrays
    output_grid[4:12] = target_pattern_segment

    # Return the modified grid
    return output_grid