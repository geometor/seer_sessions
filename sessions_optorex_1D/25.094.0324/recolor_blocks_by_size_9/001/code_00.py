import math
import re # Using regex might simplify finding groups

"""
Identifies contiguous groups of the digit '3' in the input sequence.
Compares the lengths of the first two such groups found.
If the first group is shorter than the second, replaces the first group with '2's and the second with '1's.
Otherwise (if the first group is longer or equal in length to the second), replaces the first group with '1's and the second with '2's.
Digits '0' remain unchanged.
The output sequence has the same length as the input sequence.
"""

def find_groups_of_threes(data):
    """
    Finds the start and end indices of contiguous groups of '3's.

    Args:
        data: A list of integers.

    Returns:
        A list of tuples, where each tuple is (start_index, end_index)
        for a group of '3's.
    """
    groups = []
    in_group = False
    start_index = -1
    for i, val in enumerate(data):
        if val == 3 and not in_group:
            # Start of a new group
            in_group = True
            start_index = i
        elif val != 3 and in_group:
            # End of the current group
            in_group = False
            groups.append((start_index, i - 1))
            start_index = -1 # Reset start_index
    # Handle case where the sequence ends with a group of 3s
    if in_group:
        groups.append((start_index, len(data) - 1))
    return groups

def transform(input_str):
    """
    Transforms an input string sequence based on the relative lengths of 
    the first two groups of '3's.

    Args:
        input_str: A string of space-separated digits (only '0' and '3').

    Returns:
        A string of space-separated digits representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # Find the contiguous groups of '3's
    three_groups = find_groups_of_threes(input_list)

    # Check if exactly two groups of '3's were found (as per examples)
    if len(three_groups) != 2:
        # If not exactly two groups, maybe return input or raise error?
        # Based on examples, we assume exactly two groups.
        # If the logic needs to handle 0, 1 or >2 groups, this needs adjustment.
        # For now, proceed assuming 2 groups.
        # Or handle gracefully if assumptions fail.
        # Let's assume for now it will always be 2 groups based on training data.
         pass # Or print a warning, or raise ValueError("Expected exactly two groups of '3's.")

    if len(three_groups) == 2:
        group1_indices = three_groups[0]
        group2_indices = three_groups[1]

        # Calculate lengths
        len1 = group1_indices[1] - group1_indices[0] + 1
        len2 = group2_indices[1] - group2_indices[0] + 1

        # Determine replacement values based on length comparison
        if len1 < len2:
            val1 = 2
            val2 = 1
        else: # Covers len1 >= len2
            val1 = 1
            val2 = 2

        # Apply transformations to the output list
        # Replace first group
        for i in range(group1_indices[0], group1_indices[1] + 1):
            output_list[i] = val1

        # Replace second group
        for i in range(group2_indices[0], group2_indices[1] + 1):
            output_list[i] = val2

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
