import math # Although not used in this specific function, good practice to include if math ops might arise
import collections # May be useful for more complex counting or grouping

"""
Transforms a sequence of digits by identifying the first and last occurrences 
of a non-zero digit and filling the segment between them (inclusive) with that digit.
Elements outside this segment remain unchanged.
"""

def transform(input_str: str) -> str:
    """
    Applies the segment filling transformation to a space-separated string of digits.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the transformed sequence, also space-separated.
    """

    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]
    
    # Initialize the output list as a copy of the input
    output_list = list(input_list) # Use list() to ensure it's a copy, not a reference

    # 2. Identify the unique non-zero integer value (`fill_value`).
    #    Find indices of all non-zero elements.
    non_zero_indices = [i for i, x in enumerate(input_list) if x != 0]

    # If there are no non-zero digits, return the original string unchanged.
    if not non_zero_indices:
        return input_str
        
    # Determine the fill value from the first non-zero element found.
    # The problem description implies only one type of non-zero digit per input.
    fill_value = input_list[non_zero_indices[0]] 

    # 3. Find the index of the first occurrence (`start_index`).
    start_index = non_zero_indices[0]

    # 4. Find the index of the last occurrence (`end_index`).
    end_index = non_zero_indices[-1]

    # 5. Fill the segment in the output list.
    #    Iterate from start_index to end_index (inclusive).
    for i in range(start_index, end_index + 1):
        output_list[i] = fill_value
        
    # 6. Format the output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str
