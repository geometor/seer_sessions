import math  # Although not strictly needed for this specific logic, it's good practice to include if math ops were anticipated.

"""
Transforms an input sequence containing 0s and 3s based on the lengths
of contiguous groups of 3s.

Rule:
1. Identify all distinct contiguous groups (runs) of the number 3 in the input sequence. Assume there are exactly two such groups.
2. Compare the lengths of the two groups.
3. Elements corresponding to the longer group of 3s in the input are replaced with 1s in the output sequence.
4. Elements corresponding to the shorter group of 3s in the input are replaced with 2s in the output sequence.
5. Elements that are 0 in the input remain 0 in the output.
6. If the two groups of 3s have the same length, the group that appears earlier in the sequence is treated as the 'longer' one (mapped to 1s).
"""

def find_groups_of_threes(sequence):
    """
    Identifies contiguous groups (runs) of the number 3 in a sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start' (index), 'end' (index), and 'length'.
        Returns an empty list if no groups of 3 are found.
    """
    groups = []
    in_group = False
    start_index = -1
    # Ensure input is a list
    sequence_list = list(sequence)

    for i, val in enumerate(sequence_list):
        if val == 3 and not in_group:
            # Start of a new group
            in_group = True
            start_index = i
        elif val != 3 and in_group:
            # End of the current group because a non-3 is encountered
            in_group = False
            end_index = i - 1
            length = end_index - start_index + 1
            groups.append({'start': start_index, 'end': end_index, 'length': length})
            start_index = -1 # Reset start index

    # Check if the sequence ends while inside a group of 3s
    if in_group:
        end_index = len(sequence_list) - 1
        length = end_index - start_index + 1
        groups.append({'start': start_index, 'end': end_index, 'length': length})

    return groups

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # Ensure input is treated as a standard Python list
    input_list = list(input_sequence)
    n = len(input_list)

    # 1. Initialize an output sequence of the same length as the input sequence, filled with 0s.
    output_sequence = [0] * n

    # 2. Find all contiguous groups of 3s in the input sequence.
    groups = find_groups_of_threes(input_list)

    # Based on observations, we assume exactly two groups. Handle deviations gracefully.
    if len(groups) != 2:
        # If there are no 3s or a number of groups other than 2, return the initial zero sequence.
        # This covers cases where the rule assumptions aren't met.
        # The 0s from the input are already correctly handled by the initialization.
        # If input contains only 3s (one group), this will also return all zeros based on this condition.
        return output_sequence

    # 3. Compare the lengths of the two identified groups of 3s.
    group1 = groups[0]
    group2 = groups[1]

    # 4. Determine which group is longer and which is shorter. Handle ties.
    # If lengths are equal, the first group (group1) is designated 'longer'.
    if group1['length'] >= group2['length']:
        longer_group = group1
        shorter_group = group2
    else:
        longer_group = group2
        shorter_group = group1

    # 5. Iterate through the input sequence positions:
    #   a. If the element was 0, the output remains 0 (already initialized).
    #   b. Map elements belonging to the longer group to 1.
    for i in range(longer_group['start'], longer_group['end'] + 1):
        output_sequence[i] = 1

    #   c. Map elements belonging to the shorter group to 2.
    for i in range(shorter_group['start'], shorter_group['end'] + 1):
        output_sequence[i] = 2

    # 6. Return the generated output sequence.
    return output_sequence