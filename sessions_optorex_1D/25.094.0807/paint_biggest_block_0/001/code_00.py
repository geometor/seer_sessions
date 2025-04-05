import re

"""
Identifies all contiguous groups of identical non-zero numbers in the input sequence.
Determines the maximum length among these groups.
Finds the first group (from left to right) that has this maximum length.
Replaces the numbers within this specific group with the number 1.
All other numbers in the sequence remain unchanged.
"""

def _find_groups(numbers):
    """
    Identifies contiguous groups of identical non-zero numbers.

    Args:
        numbers: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'value', 'length', 'start_index', 'end_index'.
        Returns an empty list if no non-zero groups are found.
    """
    groups = []
    if not numbers:
        return groups

    current_value = None
    current_length = 0
    start_index = -1

    for i, num in enumerate(numbers):
        if num != 0: # Consider non-zero numbers
            if num == current_value:
                # Continue the current group
                current_length += 1
            else:
                # End the previous group (if it existed and was non-zero)
                if current_value is not None and current_value != 0:
                    groups.append({
                        'value': current_value,
                        'length': current_length,
                        'start_index': start_index,
                        'end_index': i - 1
                    })
                # Start a new group
                current_value = num
                current_length = 1
                start_index = i
        else:
            # End the previous group if it was non-zero
            if current_value is not None and current_value != 0:
                groups.append({
                    'value': current_value,
                    'length': current_length,
                    'start_index': start_index,
                    'end_index': i - 1
                })
            # Reset group tracking as we encountered a zero
            current_value = None
            current_length = 0
            start_index = -1

    # Handle the last group if the sequence doesn't end with 0
    if current_value is not None and current_value != 0:
        groups.append({
            'value': current_value,
            'length': current_length,
            'start_index': start_index,
            'end_index': len(numbers) - 1
        })

    return groups


def transform(input_str):
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the transformed space-separated integers.
    """
    # 1. Parse the input string into a sequence (list) of integers.
    input_numbers = [int(x) for x in input_str.split()]

    # 2. Identify all contiguous groups of identical non-zero numbers.
    groups = _find_groups(input_numbers)

    # If no non-zero groups found, return the original sequence
    if not groups:
        return input_str

    # 3. Determine the maximum length among all identified groups.
    max_length = 0
    for group in groups:
        if group['length'] > max_length:
            max_length = group['length']

    # 4. Find the first group (the one with the smallest starting index)
    #    that has this maximum length. This is the "target group".
    target_group = None
    for group in groups:
        if group['length'] == max_length:
            target_group = group
            break # Found the first one

    # 5. Create a copy of the input sequence to serve as the output sequence.
    output_numbers = list(input_numbers)

    # 6. Iterate through the indices corresponding to the target group.
    # 7. For each index within the target group, set the value to 1.
    if target_group: # Should always be true if groups were found
        start = target_group['start_index']
        end = target_group['end_index']
        for i in range(start, end + 1):
            output_numbers[i] = 1

    # 8. Convert the modified output sequence back into a space-separated string.
    output_str = " ".join(map(str, output_numbers))

    return output_str