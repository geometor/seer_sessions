import re

def find_groups_of_threes(data):
    """
    Finds contiguous groups of the number 3 in a list of numbers.

    Args:
        data: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start', 'end', and 'length' keys.
    """
    groups = []
    start_index = -1
    for i, num in enumerate(data):
        if num == 3:
            if start_index == -1:
                start_index = i  # Mark the start of a potential group
        elif start_index != -1:
            # End of a group of 3s
            groups.append({
                'start': start_index,
                'end': i - 1,
                'length': i - start_index
            })
            start_index = -1 # Reset start index

    # Check if the list ends with a group of 3s
    if start_index != -1:
        groups.append({
            'start': start_index,
            'end': len(data) - 1,
            'length': len(data) - start_index
        })
    return groups

def transform(input_str):
    """
    Transforms an input sequence string based on the following rules:
    1. Digits '0' remain '0'.
    2. Identify contiguous groups of '3's.
    3. There will be exactly two such groups.
    4. Replace the '3's in the longer group with '1's.
    5. Replace the '3's in the shorter group with '2's.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # Find all contiguous groups of '3's
    groups = find_groups_of_threes(input_list)

    # Ensure exactly two groups are found (as per observed pattern)
    if len(groups) != 2:
        # Handle unexpected number of groups if necessary,
        # but based on examples, assume 2.
        # For now, return the initial copy if not 2 groups.
        # Or potentially raise an error.
        print(f"Warning: Expected 2 groups of 3s, but found {len(groups)}. Input: {input_str}")
        # Decide on behavior: return copy or process differently
        # return " ".join(map(str, output_list)) # Example: return unmodified
        # Let's proceed assuming 2 groups for this task based on examples

    # If exactly two groups are found, identify the longer and shorter ones
    if len(groups) == 2:
        # Sort groups by length to easily find min and max
        groups.sort(key=lambda g: g['length'])
        shorter_group = groups[0]
        longer_group = groups[1]

        # Modify the output list for the longer group (replace 3s with 1s)
        for i in range(longer_group['start'], longer_group['end'] + 1):
            output_list[i] = 1

        # Modify the output list for the shorter group (replace 3s with 2s)
        for i in range(shorter_group['start'], shorter_group['end'] + 1):
            output_list[i] = 2

    # Convert the output list back to a space-separated string
    return " ".join(map(str, output_list))
