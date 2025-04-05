```python
# -*- coding: utf-8 -*-
"""
Transforms a 12-element NumPy array according to a specific rule:
1. Receives a 12-element NumPy array of integers as input.
2. Isolates the subarray consisting of elements from index 4 up to (but not including) index 12.
3. Iterates through this subarray to find the first non-zero integer; this is the target digit `X`.
4. Constructs a new 12-element list following this structure: `[0, 0, 0, 0, X, X, X, 0, X, X, 0, X]`, using the identified digit `X`.
5. Converts each integer in the newly constructed list into its string representation.
6. Joins these string representations together, separated by single spaces.
7. Returns the resulting space-separated string.
"""

# Imports
import numpy as np
from typing import List, Union

# Define type hints for clarity
InputType = np.ndarray
OutputType = str

# === Helper Functions ===

def find_unique_non_zero(sub_array: np.ndarray) -> int:
    """
    Finds the unique non-zero digit within a NumPy array slice.
    Iterates through the slice and returns the first non-zero element found.
    Assumes based on problem description that exactly one unique non-zero digit exists.

    Args:
        sub_array: The NumPy array slice to search (e.g., indices 4-11).

    Returns:
        The integer value of the unique non-zero digit.

    Raises:
        ValueError: If no non-zero digit is found in the slice.
    """
    # Iterate through the elements of the sub-array
    for digit in sub_array:
        # Check if the digit is not zero
        if digit != 0:
            # Return the non-zero digit immediately
            # Convert to standard python int just in case it's a numpy int type
            return int(digit)
    # If the loop finishes without finding any non-zero digit, raise an error
    raise ValueError("No non-zero digit found in the provided sub-array.")

def format_list_to_string(output_list: List[int]) -> str:
    """
    Converts a list of integers into a space-separated string.

    Args:
        output_list: The list of integers to format.

    Returns:
        A string representation with elements joined by spaces.
    """
    # Convert each integer to its string representation using map
    # Join the resulting strings with a single space separator
    return " ".join(map(str, output_list))

# === Main Transformation Function ===

def transform(input_grid: InputType) -> OutputType:
    """
    Applies the sequence transformation rule to the input NumPy array.

    Args:
        input_grid: A 12-element NumPy array of integers.

    Returns:
        A string containing the transformed 12 space-separated digits.
    """
    # Validate input size (optional but good practice)
    if input_grid.shape != (12,):
        raise ValueError(f"Input array must have shape (12,), but got {input_grid.shape}")

    # Step 1: Isolate the relevant subarray (indices 4 to 11)
    variable_segment = input_grid[4:12]

    # Step 2: Find the unique non-zero digit 'X' in this segment
    non_zero_x = find_unique_non_zero(variable_segment)

    # Step 3: Construct the target pattern segment using X
    # Pattern: [X, X, X, 0, X, X, 0, X]
    target_pattern_segment = [
        non_zero_x, non_zero_x, non_zero_x, 0,
        non_zero_x, non_zero_x, 0, non_zero_x
    ]

    # Step 4: Construct the final output list
    # Combine the fixed prefix [0, 0, 0, 0] with the target pattern segment
    # The prefix can be taken directly from the input or hardcoded
    final_output_list = list(input_grid[0:4]) + target_pattern_segment

    # Step 5: Format the final list into a space-separated string
    output_string = format_list_to_string(final_output_list)

    # Step 6: Return the result
    return output_string
```