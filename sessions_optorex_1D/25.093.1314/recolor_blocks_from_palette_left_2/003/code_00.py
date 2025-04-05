import math
import re # Using re for potential group finding, although manual iteration is also fine

"""
Transforms an input sequence (list or string of 12 integers) based on the following rules:
1. Parses the input into a list of 12 integers.
2. Identifies the last two integers (index 10 and 11) as control values (val1, val2).
3. Focuses on the first 10 integers as the target subsequence.
4. Finds contiguous groups (runs) of the integer 5 within the target subsequence.
5. If exactly one group of 5s is found:
   - Replaces all 5s in that group with val1 if val1 is not 0, otherwise with val2.
6. If two or more groups of 5s are found:
   - Replaces all 5s in the first group with val1.
   - Replaces all 5s in the second group with val2.
   (Assumes transformation logic only applies to the first two groups found if more exist, based on examples).
7. Integers other than 5 (e.g., 0) in the target subsequence remain unchanged.
8. Constructs the final output sequence by appending the original control values (val1, val2) to the modified target subsequence.
"""

def find_contiguous_groups(sub_list, target_value):
    """
    Finds the start and end indices of contiguous groups of a target value in a list.

    Args:
        sub_list: The list to search within.
        target_value: The value to find contiguous groups of.

    Returns:
        A list of tuples, where each tuple contains the (start_index, end_index)
        of a contiguous group. End_index is inclusive. Returns an empty list if no groups found.
    """
    groups = []
    start_index = -1
    for i, val in enumerate(sub_list):
        if val == target_value and start_index == -1:
            # Start of a new group
            start_index = i
        elif val != target_value and start_index != -1:
            # End of the current group (non-inclusive index is i)
            groups.append((start_index, i - 1))
            start_index = -1 # Reset for finding next group

    # Check if the list ends with an ongoing group
    if start_index != -1:
        groups.append((start_index, len(sub_list) - 1))

    return groups

def transform(input_data):
    """
    Applies the transformation rule to the input data.
    """
    # 1. Parse input into a list of 12 integers
    if isinstance(input_data, str):
        # Assuming space-separated integers if input is a string
        try:
            input_list = [int(x) for x in input_data.split()]
        except ValueError:
            raise ValueError("Input string must contain space-separated integers.")
    elif isinstance(input_data, list):
        # Ensure all elements are integers if it's already a list
        if not all(isinstance(x, int) for x in input_data):
             raise ValueError("Input list must contain only integers.")
        input_list = input_data
    else:
        raise TypeError("Input must be a list of integers or a string of space-separated integers.")

    if len(input_list) != 12:
        raise ValueError("Input must contain exactly 12 integers.")

    # 2. Extract control values
    val1 = input_list[10]
    val2 = input_list[11]

    # 3. Isolate the target subsequence and create a modifiable copy
    target_subsequence = list(input_list[:10]) # Make a copy

    # 4. Find contiguous groups of 5
    target_value = 5
    groups = find_contiguous_groups(target_subsequence, target_value)
    num_groups = len(groups)

    # 5. & 6. Apply replacement logic based on the number of groups
    if num_groups == 1:
        # Determine replacement value for the single group
        replacement_value = val1 if val1 != 0 else val2
        start, end = groups[0]
        # Replace 5s within the group
        for i in range(start, end + 1):
            # Check again to ensure we only replace the target value
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = replacement_value

    elif num_groups >= 2:
        # Apply replacement for the first group using val1
        start1, end1 = groups[0]
        for i in range(start1, end1 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val1

        # Apply replacement for the second group using val2
        start2, end2 = groups[1]
        for i in range(start2, end2 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val2

    # 7. Integers other than 5 remain unchanged implicitly as we only modify specific indices/values.

    # 8. Construct the final output sequence
    output_list = target_subsequence + [val1, val2]

    return output_list