import numpy as np

"""
Identifies all contiguous groups of identical non-zero numbers in the input sequence (1D array or list).
Determines the maximum length among these groups.
Finds the first group (from left to right, based on starting index) that has this maximum length.
Replaces the numbers within this specific target group with the number 1 in a copy of the input sequence.
All other numbers in the sequence remain unchanged. Returns the modified sequence in the same format as the input (list or NumPy array).
"""

def _find_groups(numbers):
    """
    Identifies contiguous groups of identical non-zero numbers in a list of integers.

    Args:
        numbers: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'value', 'length', 'start_index', 'end_index'.
        Returns an empty list if no non-zero groups are found.
    """
    groups = []
    # Return early if the input list is empty
    if not numbers:
        return groups

    current_value = None
    current_length = 0
    start_index = -1

    # Iterate through the list with index
    for i, num in enumerate(numbers):
        # Ensure we are working with standard Python integers
        num_int = int(num)

        if num_int != 0: # Process non-zero numbers
            if num_int == current_value:
                # Continue the current group
                current_length += 1
            else:
                # If a previous non-zero group was being tracked, record it
                if current_value is not None and current_value != 0:
                    groups.append({
                        'value': current_value,
                        'length': current_length,
                        'start_index': start_index,
                        'end_index': i - 1
                    })
                # Start a new group
                current_value = num_int
                current_length = 1
                start_index = i
        else: # Process zero
            # If a non-zero group was just ending, record it
            if current_value is not None and current_value != 0:
                groups.append({
                    'value': current_value,
                    'length': current_length,
                    'start_index': start_index,
                    'end_index': i - 1
                })
            # Reset tracking since we hit a zero
            current_value = None
            current_length = 0
            start_index = -1

    # After the loop, check if the sequence ended with a non-zero group
    if current_value is not None and current_value != 0:
        groups.append({
            'value': current_value,
            'length': current_length,
            'start_index': start_index,
            'end_index': len(numbers) - 1 # Group ends at the last index
        })

    return groups

def transform(input_grid):
    # Store original type (list or ndarray) to return the same type
    is_numpy = isinstance(input_grid, np.ndarray)
    # Preserve original dtype if input is numpy array
    original_dtype = input_grid.dtype if is_numpy else None

    # Convert input to a standard Python list of integers for processing
    input_numbers = [int(x) for x in input_grid]

    # Find all contiguous groups of identical non-zero numbers
    groups = _find_groups(input_numbers)

    # If no non-zero groups are found, return a copy of the original input
    if not groups:
        if is_numpy:
            # Return a numpy array copy
            return np.array(input_numbers, dtype=original_dtype)
        else:
            # Return a list copy
            return list(input_numbers)

    # Determine the maximum length among all found groups
    max_length = 0
    for group in groups:
        if group['length'] > max_length:
            max_length = group['length']
    # Alternative using max() and a generator expression:
    # max_length = max(group['length'] for group in groups)

    # Find the first group (minimum start index) that has the maximum length
    target_group = None
    for group in groups:
        if group['length'] == max_length:
            # Since groups are found left-to-right by _find_groups,
            # the first one encountered with max_length is the target.
            target_group = group
            break

    # Create a copy of the input list to serve as the output sequence
    output_numbers = list(input_numbers)

    # If a target group was identified (should always happen if groups is not empty)
    if target_group:
        start = target_group['start_index']
        end = target_group['end_index']
        # Iterate through the indices of the target group
        for i in range(start, end + 1):
            # Set the value in the output sequence to 1
            output_numbers[i] = 1

    # Convert the modified list back to the original input type and return it
    if is_numpy:
        return np.array(output_numbers, dtype=original_dtype)
    else:
        return output_numbers