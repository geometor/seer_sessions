import collections # Using collections although not strictly necessary for this solution

"""
Replace a sequence of trailing zeros in a list of integers with the initial segment of the list, 
where the segment's length equals the number of zeros.
"""

def find_trailing_zeros_start_index(sequence: list[int]) -> int:
    """
    Finds the starting index of the block of trailing zeros in a sequence.
    
    Helper function to locate the beginning of the trailing zero segment.
    
    Args:
        sequence: The input list of integers.
        
    Returns:
        The index where the trailing zeros begin. If no trailing zeros, 
        returns the length of the sequence. If all elements are zero, returns 0.
        If the list is empty, returns 0.
    """
    n = len(sequence)
    # Iterate backwards from the end of the list towards the beginning.
    # The range goes down to -2 so that the loop includes checking index 0
    # and handles the case where i becomes -1 after checking index 0.
    for i in range(n - 1, -2, -1):
        # If we've iterated past the beginning of the list (i == -1) 
        # or if we find an element that is not zero,
        # then the block of trailing zeros starts at the next index (i + 1).
        if i == -1 or sequence[i] != 0:
            return i + 1
    # This fallback is theoretically unreachable for non-empty lists due to the i == -1 check,
    # but ensures 0 is returned for an empty list (n=0, range is empty).
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
    # Determine the total length (L) of the input list.
    L = len(input_list)

    # Find the starting index (idx) of the block of trailing zeros using the helper function.
    # idx will be equal to L if there are no trailing zeros.
    # idx will be 0 if all elements are zeros or the list is empty.
    idx = find_trailing_zeros_start_index(input_list)

    # Calculate the number of trailing zeros (N) by subtracting the start index from the total length.
    N = L - idx

    # Check if there are any trailing zeros.
    if N == 0:
        # If N is 0, no trailing zeros exist. Return a copy of the original list.
        # Returning a copy ([ : ]) ensures the original list is not modified if it's mutable elsewhere.
        return input_list[:] 
    else:
        # If N > 0, there are trailing zeros to replace.
        
        # Extract the prefix of the list: elements from the beginning up to the start of the zeros (index idx).
        non_zero_prefix = input_list[:idx]

        # Extract the initial segment of the list: the first N elements (from index 0 up to N-1).
        # This is the segment that will replace the trailing zeros.
        initial_segment_to_copy = input_list[:N]

        # Construct the output list by concatenating the non-zero prefix 
        # with the initial segment that needs to be copied.
        output_list = non_zero_prefix + initial_segment_to_copy

        # Return the newly constructed output list.
        return output_list