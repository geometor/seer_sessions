"""
Modifies contiguous sequences of identical non-zero digits in a 1D array.
If a sequence's length is 3 or more, its internal elements (all except the first and last) are replaced with 0.
Sequences of length 1 or 2 remain unchanged.
"""

import copy

def transform(input_list):
    """
    Transforms the input list based on the rule described above.

    Args:
        input_list: A list of single-digit integers.

    Returns:
        A new list with the transformation applied.
    """
    # Initialize output_list as a copy of the input list
    output_list = copy.deepcopy(input_list)
    n = len(input_list)
    i = 0

    # Iterate through the list to find sequences
    while i < n:
        current_val = input_list[i]

        # Check if the current element is non-zero and potentially starts a sequence
        if current_val != 0:
            start_index = i
            # Find the end of the contiguous sequence of the same non-zero value
            j = i + 1
            while j < n and input_list[j] == current_val:
                j += 1
            
            # The sequence ends at index j-1
            end_index = j - 1
            length = end_index - start_index + 1

            # If the sequence length is 3 or more, modify the output list
            if length >= 3:
                # Set elements between the first and last to 0
                for k in range(start_index + 1, end_index):
                    output_list[k] = 0
            
            # Move the main loop index past the processed sequence
            i = j 
        else:
            # If the current element is 0, just move to the next element
            i += 1

    return output_list