import numpy as np
import re # Although not strictly needed for this version, good practice for string parsing

"""
Identifies the unique non-zero integer value (d) present in the input sequence.
Finds the first (start_index) and last (end_index) occurrences of d.
Creates an output sequence of the same length, initially filled with zeros.
Sets the elements in the output sequence from start_index to end_index (inclusive) to the value d.
"""

def _find_non_zero_info(arr):
    """
    Helper function to find the non-zero digit and its first/last indices.
    
    Args:
        arr (np.ndarray): The input numpy array.

    Returns:
        tuple: (non_zero_digit, start_index, end_index)
               Returns (0, -1, -1) if no non-zero digit is found.
    """
    # Find indices where the element is not zero
    non_zero_indices = np.where(arr != 0)[0]
    
    # Handle the case where there are no non-zero elements (though unlikely based on examples)
    if len(non_zero_indices) == 0:
        return 0, -1, -1 
    
    # Get the first and last index of non-zero elements
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    
    # Get the value of the non-zero digit (assuming it's consistent)
    non_zero_digit = arr[start_index]
    
    return non_zero_digit, start_index, end_index

def transform(input_str):
    """
    Transforms the input string sequence by filling the space between 
    the first and last occurrence of the non-zero digit with that digit.

    Args:
        input_str (str): A space-separated string of integers.

    Returns:
        str: A space-separated string of integers representing the transformed sequence.
    """
    # Parse the input string into a numpy array of integers
    # Use list comprehension for parsing, then convert to numpy array
    input_arr = np.array([int(x) for x in input_str.split()], dtype=int)
    
    # Determine the size of the sequence
    n = len(input_arr)
    
    # Find the unique non-zero digit and its first and last indices
    non_zero_digit, start_index, end_index = _find_non_zero_info(input_arr)
    
    # Initialize the output array with zeros, same size as input
    output_arr = np.zeros(n, dtype=int)
    
    # If a non-zero digit was found (indices are valid)
    if start_index != -1:
        # Fill the segment from start_index to end_index (inclusive) 
        # with the non_zero_digit using numpy slicing
        output_arr[start_index : end_index + 1] = non_zero_digit
        
    # Convert the output numpy array back to a space-separated string
    output_str = " ".join(map(str, output_arr))
    
    return output_str
