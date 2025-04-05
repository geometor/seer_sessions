import re

"""
Transforms sequences of 0s and 3s based on the relative lengths of contiguous groups of 3s.

1. Identify all contiguous groups (subsequences) consisting solely of the number 3.
2. Assume exactly two such groups exist. Let Group1 be the first group and Group2 be the second.
3. Compare the lengths of Group1 and Group2.
4. If Group1 is longer than Group2, replace the 3s in Group1 with 1s and the 3s in Group2 with 2s in the output.
5. Otherwise (Group1 is shorter or equal in length to Group2), replace the 3s in Group1 with 2s and the 3s in Group2 with 1s in the output.
6. Keep all 0s unchanged in their original positions.
"""

def find_groups_of_threes(numbers):
    """
    Finds contiguous groups of the number 3 in a list of numbers.

    Args:
        numbers: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start' index, 'end' index, and 'length'.
        Returns an empty list if no groups of 3 are found.
    """
    groups = []
    i = 0
    n = len(numbers)
    while i < n:
        if numbers[i] == 3:
            start_index = i
            # Find the end of the group
            while i + 1 < n and numbers[i + 1] == 3:
                i += 1
            end_index = i
            length = end_index - start_index + 1
            groups.append({'start': start_index, 'end': end_index, 'length': length})
        i += 1
    return groups

def transform(input_grid: str) -> str:
    """
    Applies the transformation rule to the input sequence string.
    
    Args:
        input_grid: A string representing the sequence of numbers separated by spaces.

    Returns:
        A string representing the transformed sequence separated by spaces.
    """
    # Parse the input string into a list of integers
    try:
        input_numbers = [int(x) for x in input_grid.split()]
    except ValueError:
        # Handle potential errors if input is not numbers
        print(f"Error: Input grid contains non-integer values: {input_grid}")
        return "" 

    # Initialize the output list as a copy of the input
    output_numbers = list(input_numbers)

    # Find groups of 3s
    groups = find_groups_of_threes(input_numbers)

    # --- Apply transformation logic ---
    # The logic assumes exactly two groups are found, as per the examples and analysis.
    if len(groups) == 2:
        group1 = groups[0]
        group2 = groups[1]

        # Determine the output values based on group lengths
        val1, val2 = (1, 2) if group1['length'] > group2['length'] else (2, 1)

        # Apply the transformation to the output list for the first group
        for i in range(group1['start'], group1['end'] + 1):
            output_numbers[i] = val1

        # Apply the transformation to the output list for the second group
        for i in range(group2['start'], group2['end'] + 1):
            output_numbers[i] = val2
            
    elif len(groups) == 1:
        # Handle case with only one group (though not in examples)
        # Assign a default value, e.g., 1? Or maybe 2 if length > X?
        # Based on the provided examples, this case might not occur or needs clarification.
        # Let's default to 1 for now if only one group exists.
        group1 = groups[0]
        for i in range(group1['start'], group1['end'] + 1):
            output_numbers[i] = 1 # Default assignment for single group
            
    # If len(groups) is 0 or > 2, the output remains unchanged from input (except for 3s),
    # or requires further rule clarification. The current code leaves 3s as 3s if != 2 groups.

    # Format the output list back into a space-separated string
    output_grid = " ".join(map(str, output_numbers))

    return output_grid