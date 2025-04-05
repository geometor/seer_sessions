```python
import math # Although not used in the final logic, kept for potential future needs
import re   # Although not used in the final logic, kept for potential future needs

"""
Transforms an input sequence (list or string of 12 integers) based on the following rules:
1. Parses the input into a list of 12 integers.
2. Identifies the last two integers (index 10 and 11) as control values (val1, val2).
3. Focuses on the first 10 integers as the target subsequence.
4. Finds contiguous groups (runs) of the integer 5 within the target subsequence.
5. If exactly one group of 5s is found:
   - Replaces all 5s in that group with val2 (the value at index 11).
6. If two or more groups of 5s are found:
   - Replaces all 5s in the first group with val1 (the value at index 10).
   - Replaces all 5s in the second group with val2 (the value at index 11).
   (Assumes transformation logic only applies to the first two groups found if more exist).
7. Integers other than 5 (e.g., 0) in the target subsequence remain unchanged.
8. Constructs the final output sequence by appending the original control values (val1, val2) to the modified target subsequence.
"""

# No specific imports required beyond standard Python capabilities for this task


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
    # Iterate through the list with index
    for i, val in enumerate(sub_list):
        # Check if the current value matches the target and if we are not already in a group
        if val == target_value and start_index == -1:
            # Start of a new group found at current index
            start_index = i
        # Check if the current value does *not* match the target and if we *were* in a group
        elif val != target_value and start_index != -1:
            # End of the previous group found (ends at the previous index)
            groups.append((start_index, i - 1))
            # Reset start_index to indicate we are no longer in a group
            start_index = -1

    # After the loop, check if we were still in a group when the list ended
    if start_index != -1:
        # The group extends to the end of the list
        groups.append((start_index, len(sub_list) - 1))

    return groups


def transform(input_data):
    """
    Applies the transformation rule to the input data.
    """
    # --- 1. Parse Input ---
    # Check if input is a string, try to split and convert to integers
    if isinstance(input_data, str):
        try:
            input_list = [int(x) for x in input_data.split()]
        except ValueError:
            raise ValueError("Input string must contain 12 space-separated integers.")
    # Check if input is already a list
    elif isinstance(input_data, list):
        # Verify all elements in the list are integers
        if not all(isinstance(x, int) for x in input_data):
             raise TypeError("Input list must contain only integers.")
        input_list = input_data # Use the list directly
    # Handle invalid input types
    else:
        raise TypeError("Input must be a list of integers or a string of space-separated integers.")

    # Validate that the list has the correct length
    if len(input_list) != 12:
        raise ValueError("Input must contain exactly 12 integers.")

    # --- 2. Extract Components ---
    # Get the control values from the end of the list
    val1 = input_list[10]
    val2 = input_list[11]
    # Create a mutable copy of the first 10 elements (target subsequence)
    # This copy will be modified
    target_subsequence = list(input_list[:10])

    # --- 3. Find Target Groups ---
    # Define the value we are looking for groups of
    target_value = 5
    # Use the helper function to find groups of '5'
    groups = find_contiguous_groups(target_subsequence, target_value)
    num_groups = len(groups) # Count how many groups were found

    # --- 4. Apply Conditional Replacement Logic ---
    # Check the number of groups found and apply the corresponding rule
    if num_groups == 1:
        # Case: Exactly one group of 5s found
        # Use val2 as the replacement value
        replacement_value = val2
        # Get the start and end indices of the single group
        start, end = groups[0]
        # Iterate through the indices within the group's range
        for i in range(start, end + 1):
            # Double-check if the value at the index is indeed the target value before replacing
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = replacement_value

    elif num_groups >= 2:
        # Case: Two or more groups found (logic only applies to the first two)
        # Process the first group
        start1, end1 = groups[0]
        # Replace 5s in the first group with val1
        for i in range(start1, end1 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val1

        # Process the second group
        start2, end2 = groups[1]
        # Replace 5s in the second group with val2
        for i in range(start2, end2 + 1):
            if target_subsequence[i] == target_value:
                 target_subsequence[i] = val2
    # Else (num_groups == 0): No groups found, so no changes are made to target_subsequence

    # --- 5. Construct Output ---
    # Combine the (potentially modified) target subsequence with the original control values
    output_list = target_subsequence + [val1, val2]

    # Return the final transformed list
    return output_list
```