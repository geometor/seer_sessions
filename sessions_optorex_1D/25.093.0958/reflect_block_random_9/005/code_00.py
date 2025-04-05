import math # Although not used in this specific implementation, it's a common import.
# No other specific libraries like numpy seem necessary based on the task description.

"""
Reverses the contiguous sub-sequence of non-zero digits within a sequence of digits provided as a space-separated string, 
leaving any leading or trailing zeros in their original positions. Returns the transformed sequence as a space-separated string.
"""

def find_first_non_zero_index(data_list):
    """
    Finds the index of the first non-zero element in a list of numbers.
    Returns -1 if no non-zero element is found.
    """
    for i, x in enumerate(data_list):
        if x != 0:
            return i
    return -1 # Indicate no non-zero element found

def find_last_non_zero_index(data_list):
    """
    Finds the index of the last non-zero element in a list of numbers.
    Returns -1 if no non-zero element is found (should not happen if find_first_non_zero_index found one).
    """
    n = len(data_list)
    for i in range(n - 1, -1, -1):
        if data_list[i] != 0:
            return i
    # This case should theoretically not be reached if the list contains non-zeros,
    # but included for completeness.
    return -1 

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Workflow:
    1. Parse the input string into a list of integers.
    2. Find the start and end indices of the contiguous non-zero block using helper functions.
    3. Handle the edge case: If no non-zero digits are found, return the original input string.
    4. Extract the leading zeros sub-list (before start_index).
    5. Extract the non-zero block sub-list (from start_index to end_index inclusive).
    6. Extract the trailing zeros sub-list (after end_index).
    7. Reverse the non-zero block sub-list.
    8. Reconstruct the output list by concatenating the three sub-lists in order.
    9. Format the output list back into a space-separated string.
    10. Return the formatted output string.
    """

    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]

    # 2. Find the start and end indices of the contiguous non-zero block.
    start_index = find_first_non_zero_index(input_list)
    
    # 3. Handle the edge case: If no non-zero digits are found (all zeros or empty input after split),
    #    return the original input string.
    if start_index == -1:
        return input_str
        
    # Since we know there's at least one non-zero number, end_index will also be valid.
    end_index = find_last_non_zero_index(input_list)

    # 4. Extract the leading zeros sub-list.
    leading_zeros = input_list[:start_index]
    
    # 5. Extract the non-zero block sub-list.
    non_zero_block = input_list[start_index : end_index + 1]
    
    # 6. Extract the trailing zeros sub-list.
    trailing_zeros = input_list[end_index + 1:]

    # 7. Reverse the non-zero block sub-list.
    reversed_non_zero_block = non_zero_block[::-1] # Python slicing creates a reversed copy

    # 8. Reconstruct the output list by concatenating the parts.
    output_list = leading_zeros + reversed_non_zero_block + trailing_zeros

    # 9. Format the output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    # 10. Return the formatted output string.
    return output_str