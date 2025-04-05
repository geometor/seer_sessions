```python
"""
Transforms an input string sequence of integers by identifying the unique non-zero digit (d), finding its first (start_index) and last (end_index) occurrences, and creating an output sequence of the same length where the elements from start_index to end_index (inclusive) are set to d, and all other elements are zero. The output is formatted as a space-separated string.
"""

import numpy as np
import re # Although not strictly needed for this specific version, importing for potential future string parsing needs.

def _find_non_zero_info(arr):
    """
    Helper function to find the non-zero digit and its first/last indices.
    
    Args:
        arr (np.ndarray): The input numpy array of integers.

    Returns:
        tuple: (non_zero_digit, start_index, end_index)
               Returns (0, -1, -1) if no non-zero digit is found or only one is found.
               Assumes exactly two non-zero digits based on problem description.
    """
    # Find indices where the element is not zero
    non_zero_indices = np.where(arr != 0)[0]
    
    # Handle cases based on the number of non-zero elements found
    if len(non_zero_indices) < 2: # Expecting exactly two based on examples
        # Return default values if fewer than 2 non-zero elements are found
        # This might indicate an edge case or unexpected input format
        return 0, -1, -1 
    
    # Get the first and last index from the list of non-zero indices
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1] # Use the last index found
    
    # Get the value of the non-zero digit (assuming it's consistent, taking the first one)
    non_zero_digit = arr[start_index]
    
    return non_zero_digit, start_index, end_index

def transform(input_str: str) -> str:
    """
    Transforms the input string sequence according to the specified rule.

    Args:
        input_str (str): A space-separated string of integers.

    Returns:
        str: A space-separated string of integers representing the transformed sequence.
    """
    
    # 1. Parse the input string into a list/array of integers.
    # Using numpy for efficient array operations.
    try:
        input_arr = np.array([int(x) for x in input_str.split()], dtype=int)
    except ValueError:
        # Handle potential errors if the input string is not formatted correctly
        # For this problem, assume valid input based on examples.
        # If invalid, could return empty string, raise error, or return input.
        return "" # Or handle error appropriately

    # Get the length of the sequence
    n = len(input_arr)

    # 2. Identify the unique non-zero digit (d).
    # 3. Find the index of the first (start_index) and last (end_index) occurrences of d.
    # Use the helper function for this.
    non_zero_digit, start_index, end_index = _find_non_zero_info(input_arr)

    # 4. Create a new list/array of the same length, initially filled with zeros.
    output_arr = np.zeros(n, dtype=int)

    # 5. Fill the output array with the non-zero digit between the found indices (inclusive).
    # Check if valid indices were found (non_zero_digit is not 0 and indices are valid)
    if start_index != -1: # Check if valid indices were returned
        # Use numpy slicing for efficient filling
        output_arr[start_index : end_index + 1] = non_zero_digit
        
    # 6. Format the output array back into a space-separated string.
    output_str = " ".join(map(str, output_arr))
    
    # 7. Return the formatted string.
    return output_str

```