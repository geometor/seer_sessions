```python
import collections

"""
Transforms an input list of integers based on the following rule:
1. Identify all unique non-zero digits and the indices where they appear.
2. Check if any non-zero digit appears exactly twice in the list.
3. If one or more digits appear exactly twice, select the digit whose *first* occurrence (smallest index) is earliest in the list. This is the "target digit".
4. If a target digit is found with indices idx1 and idx2 (idx1 < idx2), create a copy of the input list.
5. In the copied list, change the value of all elements at indices strictly between idx1 and idx2 (i.e., from index idx1 + 1 up to, but not including, index idx2) to the value of the target digit.
6. Return the modified list.
7. If no non-zero digit appears exactly twice, return the original input list unchanged.
"""

def find_indices_and_first_occurrence(data_list):
    """
    Finds all indices for each non-zero number and tracks the first index seen.

    Args:
        data_list: The input list of integers.

    Returns:
        A tuple containing:
        - dict: A dictionary mapping each non-zero digit to a list of its indices.
        - dict: A dictionary mapping each non-zero digit to its first encountered index.
    """
    indices_map = collections.defaultdict(list)
    first_occurrence = {}
    for index, value in enumerate(data_list):
        if value != 0:
            indices_map[value].append(index)
            if value not in first_occurrence:
                first_occurrence[value] = index
    return indices_map, first_occurrence

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers.

    Returns:
        A new list representing the transformed output, or the original list if no transformation applies.
    """

    # Analyze the input to find indices and first occurrences of non-zero digits
    indices_map, first_occurrence = find_indices_and_first_occurrence(input_list)

    # Initialize variables to find the target digit (the one appearing twice with the earliest first occurrence)
    target_digit = None
    min_first_index = float('inf')
    target_indices = None

    # Iterate through the digits found to identify potential targets
    for digit, indices in indices_map.items():
        # Check if the digit occurs exactly twice
        if len(indices) == 2:
            # Get the first index of this digit
            current_first_index = first_occurrence[digit]
            # If this digit's first occurrence is earlier than the current best, update the target
            if current_first_index < min_first_index:
                min_first_index = current_first_index
                target_digit = digit
                target_indices = indices

    # If no target digit was found (no digit appeared exactly twice)
    if target_digit is None:
        # Return the original list unchanged
        return list(input_list) # Return a copy to be safe, matching pattern of returning new list on change
    else:
        # A target digit was found, perform the fill operation
        # Create a copy of the input list to modify
        output_list = list(input_list)
        idx1, idx2 = target_indices[0], target_indices[1]

        # Fill the gap between the two indices (exclusive) with the target digit
        # Range starts from the element *after* the first occurrence (idx1 + 1)
        # and goes up to (but does not include) the second occurrence (idx2).
        for i in range(idx1 + 1, idx2):
            output_list[i] = target_digit

        # Return the modified list
        return output_list
```