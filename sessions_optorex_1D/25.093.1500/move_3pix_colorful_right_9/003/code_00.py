import numpy as np
from typing import List, Tuple, Optional

"""
Identifies the sub-sequence spanning from the first non-zero element to the last non-zero element 
in the input sequence. This sub-sequence (span) is then shifted 3 positions to the right within a new 
sequence of the same length, initially filled with zeros. If the input sequence contains only 
zeros, the output sequence also contains only zeros. Elements shifted beyond the sequence boundary are truncated.
"""

def find_non_zero_span(numbers: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the indices of the first and last non-zero elements in the list.

    Args:
        numbers: A list or 1D numpy array of integers.

    Returns:
        A tuple containing the start and end indices (inclusive) of the span
        containing all non-zero numbers, or None if all numbers are zero.
    """
    start_index = -1
    end_index = -1
    # Iterate through the list to find the first and last non-zero indices
    for i, num in enumerate(numbers):
        if num != 0:
            if start_index == -1:
                start_index = i # Found the first non-zero number
            end_index = i # Update the last known non-zero index
    
    # If no non-zero number was found, start_index will still be -1
    if start_index == -1:
        return None
    else:
        return start_index, end_index

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A 1D numpy array of integers.

    Returns:
        A 1D numpy array representing the transformed sequence.
    """
    # Ensure input is treated as a list for consistent processing
    input_list = list(input_sequence)
    n = len(input_list)
    
    # Initialize output list with zeros of the same length
    output_list = [0] * n

    # Find the span of non-zero numbers in the input
    span = find_non_zero_span(input_list)

    # If a non-zero span exists (i.e., the input was not all zeros)
    if span:
        start_index, end_index = span
        
        # Calculate the new starting position for the span (shifted right by 3)
        target_start_index = start_index + 3
        
        # Iterate through the elements within the identified span in the input
        for i in range(start_index, end_index + 1):
            # Calculate the corresponding target index in the output list
            current_output_index = target_start_index + (i - start_index)
            
            # Check if the target index is within the bounds of the output list
            if 0 <= current_output_index < n:
                # Copy the element from the input span to the target position in the output
                output_list[current_output_index] = input_list[i]
                
    # Convert the result back to a numpy array
    return np.array(output_list)