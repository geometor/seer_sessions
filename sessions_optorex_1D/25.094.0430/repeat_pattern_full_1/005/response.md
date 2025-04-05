```python
import collections # Using collections although not strictly necessary for this solution

"""
Replace a sequence of trailing zeros in a list of integers with the initial segment of the list, 
where the segment's length equals the number of zeros.
"""

def find_trailing_zeros_start_index(sequence: list[int]) -> int:
    """
    Finds the starting index of the block of trailing zeros in a sequence.
    
    Args:
        sequence: The input list of integers.
        
    Returns:
        The index where the trailing zeros begin. If no trailing zeros, 
        returns the length of the sequence. If all elements are zero, returns 0.
    """
    n = len(sequence)
    # Iterate backwards from the end of the list
    for i in range(n - 1, -2, -1):
        # If we go past the beginning (i == -1) or find a non-zero number,
        # the trailing zeros (if any) start at the next position (i + 1).
        if i == -1 or sequence[i] != 0:
            return i + 1
    # This line is theoretically unreachable for non-empty lists due to the i == -1 check,
    # but provides a fallback for completeness (e.g., empty list).
    return 0 

def transform(input_list: list[int]) -> list[int]:
    """
    Transforms the input list by replacing trailing zeros with the initial segment.
    
    Args:
        input_list: A list of integers.
        
    Returns:
        A new list of integers with trailing zeros replaced by the initial segment
        of corresponding length.
    """
    # Determine the total length of the input list.
    L = len(input_list)

    # Find the starting index of the block of trailing zeros.
    # idx will be equal to L if there are no trailing zeros.
    # idx will be 0 if all elements are zeros.
    idx = find_trailing_zeros_start_index(input_list)

    # Calculate the number of trailing zeros (N).
    N = L - idx

    # If there are no trailing zeros (N is 0), return a copy of the original list.
    if N == 0:
        return input_list[:] # Return a copy to avoid modifying the original if it's mutable

    # Extract the prefix of the list (elements before the trailing zeros).
    # This slice goes from the beginning up to, but not including, index idx.
    non_zero_prefix = input_list[:idx]

    # Extract the initial segment of the list (the first N elements).
    # This slice goes from the beginning up to, but not including, index N.
    initial_segment_to_copy = input_list[:N]

    # Construct the output list by concatenating the non-zero prefix 
    # and the initial segment that needs to be copied.
    output_list = non_zero_prefix + initial_segment_to_copy

    # Return the constructed output list.
    return output_list
```