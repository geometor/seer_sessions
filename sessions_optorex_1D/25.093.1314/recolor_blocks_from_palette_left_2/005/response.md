```python
import math
import re # Although not strictly used in the final version, kept for potential alternative group finding

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
    Helper function to find the start and end indices of contiguous groups of a target value.

    Args:
        sub_list: The list (or list slice) to search within.
        target_value: The integer value to find contiguous groups of.

    Returns:
        A list of tuples, where each tuple is (start_index, end_index) inclusive.
        Returns an empty list if no groups are found.
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
    # 1. Parse Input: Convert input string/list to a list of 12 integers
    if isinstance(input_data, str):
        try:
            input_list = [int(x) for x in input_data.split()]
        except ValueError:
            # Handle cases where splitting or conversion fails
            raise ValueError("Input string must contain 12 space-separated integers.")
    elif isinstance(input_data, list):
        if not all(isinstance(x, int) for x in input_data):
             raise TypeError("Input list must contain only integers.")
        input_list = input_data # Use the list directly
    else:
        raise TypeError("Input must be a list of integers or a string of space-separated integers.")

    # Validate length
    if len(input_list) != 12:
        raise ValueError("Input must contain exactly 12 integers.")

    # 2. Extract Components: Get target sequence and control values
    val1 = input_list[10]
    val2 = input_list[11]
    # Create a mutable copy for modifications
    target_subsequence = list(input_list[:10])

    # 3. Find Target Groups: Identify contiguous runs of '5'
    target_value = 5
    groups = find_contiguous_groups(target_subsequence, target_value)
    num_groups = len(groups)

    # 4. Apply Conditional Replacement: Modify the target subsequence based on groups found
    if num_groups == 1:
        # Case 1: Exactly one group found
        replacement_value = val1 if val1 != 0 else val2
        start, end = groups[0]
        # Replace all 5s within this group's range
        for i in range(start, end + 1):
            if target_subsequence[i] == target_value: # Ensure we only replace the target
                 target_subsequence[i] = replacement_value

    elif num_groups >= 2:
        # Case 2: Two or more groups found (apply logic to first two)
        # Replace first group with val1
        start1, end1 = groups[0]
        for i in range(start1, end1 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val1

        # Replace second group with val2
        start2, end2 = groups[1]
        for i in range(start2, end2 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val2
    # Else (num_groups == 0): No groups found, no changes needed to target_subsequence

    # 5. Construct Output: Combine modified subsequence with original control values
    output_list = target_subsequence + [val1, val2]

    return output_list
```