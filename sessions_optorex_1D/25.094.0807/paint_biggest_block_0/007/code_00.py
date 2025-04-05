import numpy as np

"""
Identifies all contiguous groups of identical non-zero numbers in the input sequence (potentially a multi-dimensional array, treated as flattened).
Determines the maximum length among these groups.
Finds the first group (from left to right in the flattened sequence) that has this maximum length.
Replaces the numbers within this specific target group with the number 1 in a copy of the sequence.
All other numbers in the sequence remain unchanged. 
Returns the modified sequence in the same format as the input (list or NumPy array with original shape/dtype).
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
    # 1. Accept the input data, noting if it is a NumPy array or a Python list.
    is_numpy = isinstance(input_grid, np.ndarray)
    original_shape = None
    original_dtype = None
    if is_numpy:
        original_shape = input_grid.shape
        original_dtype = input_grid.dtype

    # 2. Create a flattened, 1D list of Python integers from the input data.
    if is_numpy:
        # Use .flat for efficient iteration over potentially multi-dimensional arrays
        input_numbers = [int(x) for x in input_grid.flat]
    else:
        # Assuming input_grid is already a list or similar iterable of numbers
        # If nested lists are possible, flatten them here (simplest case assumed)
        try:
            input_numbers = [int(x) for x in input_grid]
        except TypeError: # Handle potential nested lists if needed
             # A more robust flattening might be required for complex list structures
             # For now, assume it's a flat list or directly iterable numbers
             print("Warning: Input list structure might be complex. Assuming flattenable.")
             # Basic flatten for list of lists (depth 1)
             if any(isinstance(el, list) for el in input_grid):
                 input_numbers = [int(item) for sublist in input_grid for item in sublist]
             else: # Assume flat list already
                input_numbers = [int(x) for x in input_grid]


    # 3. Find all contiguous groups of identical non-zero numbers.
    groups = _find_groups(input_numbers)

    # 4. If no non-zero groups were found, return a copy in the original format.
    if not groups:
        if is_numpy:
            # Reconstruct numpy array
            return np.array(input_numbers, dtype=original_dtype).reshape(original_shape)
        else:
            # Return a list copy
            return list(input_numbers) # Assuming original was flat list

    # 5. Calculate the maximum length among all identified groups.
    max_length = 0
    for group in groups:
        if group['length'] > max_length:
            max_length = group['length']
    # Alternative: max_length = max(group['length'] for group in groups) if groups else 0

    # 6. Find the first group (smallest start index) with the maximum length.
    target_group = None
    for group in groups:
        if group['length'] == max_length:
            target_group = group
            break # Found the first (leftmost)

    # 7. Create a copy of the flattened list of integers.
    output_numbers = list(input_numbers)

    # 8. Modify the copy: set values in the target group to 1.
    # This check is slightly redundant since we handled the 'not groups' case, but safe.
    if target_group:
        start = target_group['start_index']
        end = target_group['end_index']
        for i in range(start, end + 1):
            output_numbers[i] = 1

    # 9. Convert the modified list back into the original input format.
    if is_numpy:
        output_grid = np.array(output_numbers, dtype=original_dtype).reshape(original_shape)
    else:
        # Assuming the original was a flat list structure
        output_grid = output_numbers # Return the modified list

    # 10. Return the final formatted output.
    return output_grid