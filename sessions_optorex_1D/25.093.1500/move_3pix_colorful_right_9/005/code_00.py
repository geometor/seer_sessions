import numpy as np
from typing import List, Tuple, Optional

"""
Identifies the sub-sequence within the input sequence that starts at the first non-zero 
element and ends at the last non-zero element (the "non-zero span"). This entire span 
is then shifted 3 positions to the right. The output sequence is initialized with zeros, 
and the shifted span is placed into it. Elements shifted beyond the sequence boundary 
are truncated. If the input sequence contains only zeros, the output sequence also 
contains only zeros.
"""

def find_non_zero_span(numbers: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the indices of the first and last non-zero elements in the list.

    Args:
        numbers: A list of integers.

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

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (represented as a 1D numpy array).

    Args:
        input_grid: A 1D numpy array of integers.

    Returns:
        A 1D numpy array representing the transformed sequence.
    """
    # Convert numpy array to list for easier index finding if needed, though direct iteration works too
    input_list = list(input_grid)
    n = len(input_list)
    
    # Initialize output_grid with zeros of the same length as the input
    output_grid = np.zeros(n, dtype=int)

    # Find the span (start and end indices) of non-zero numbers in the input
    span = find_non_zero_span(input_list)

    # If a non-zero span exists (i.e., the input was not all zeros)
    if span:
        start_index, end_index = span
        
        # Calculate the starting position for the span in the output grid (shifted right by 3)
        target_start_index = start_index + 3
        
        # Iterate through the elements within the identified span in the input list
        for i in range(start_index, end_index + 1):
            # Calculate the corresponding target index in the output grid
            # The offset within the span is (i - start_index)
            target_index = target_start_index + (i - start_index)
            
            # Check if the target index is within the bounds of the output grid
            if 0 <= target_index < n:
                # Copy the element from the input span to the target position in the output grid
                output_grid[target_index] = input_list[i]
                # If the target_index is out of bounds, the element is truncated (implicitly, as we don't copy it)
                
    # If no span was found, the output_grid remains all zeros, which is the correct output

    return output_grid