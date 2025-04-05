import numpy as np # Using numpy for potential array operations, though lists work too

"""
Transforms sequences of 0s and 3s based on the relative lengths of contiguous groups of 3s, assuming exactly two such groups exist.

1. Identify all contiguous groups (subsequences) consisting solely of the number 3.
2. Assume exactly two such groups are found. Let Group1 be the group that appears first (smaller start index) and Group2 be the group that appears second.
3. Compare the lengths of Group1 and Group2.
4. If Group1 is strictly longer than Group2, replace the 3s in Group1 with 1s and the 3s in Group2 with 2s in the output.
5. Otherwise (if Group1 is shorter or equal in length to Group2), replace the 3s in Group1 with 2s and the 3s in Group2 with 1s in the output.
6. Keep all 0s unchanged in their original positions.
"""

def find_groups_of_threes(numbers):
    """
    Finds contiguous groups of the number 3 in a list or array of numbers.

    Args:
        numbers: A list or NumPy array of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start' index, 'end' index, and 'length'.
        Returns an empty list if no groups of 3 are found.
    """
    groups = []
    i = 0
    n = len(numbers)
    while i < n:
        # Check if the current number starts a group of 3s
        if numbers[i] == 3:
            start_index = i
            # Find the end of the contiguous group of 3s
            while i + 1 < n and numbers[i + 1] == 3:
                i += 1
            end_index = i
            # Calculate the length of the group
            length = end_index - start_index + 1
            # Store the group information
            groups.append({'start': start_index, 'end': end_index, 'length': length})
        i += 1 # Move to the next number
    return groups

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.
    
    Args:
        input_grid: A list or NumPy array representing the sequence of numbers.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Convert input to a list for easier manipulation if it's a NumPy array
    # This ensures consistent handling regardless of input type (list or np.array)
    input_list = list(input_grid) 
    
    # initialize output_grid as a copy of the input
    # Using list() ensures we don't modify the original input_grid if it was mutable
    output_list = list(input_list) 

    # Find all contiguous groups of the number 3
    groups = find_groups_of_threes(input_list)

    # Apply transformation logic only if exactly two groups are found
    if len(groups) == 2:
        group1 = groups[0] # The first group encountered
        group2 = groups[1] # The second group encountered

        # Compare the lengths of the two groups
        # Assign output values: 1 for the longer group, 2 for the shorter/equal one
        # If lengths are equal, group1 gets 2, group2 gets 1
        val1, val2 = (1, 2) if group1['length'] > group2['length'] else (2, 1)

        # Modify the output list based on the determined values
        # Replace 3s in the first group's range with val1
        for i in range(group1['start'], group1['end'] + 1):
            output_list[i] = val1

        # Replace 3s in the second group's range with val2
        for i in range(group2['start'], group2['end'] + 1):
            output_list[i] = val2
            
    # If the number of groups is not exactly 2, the function currently
    # returns the original grid unchanged (as output_list was initialized
    # as a copy and no modifications were made in the 'if' block).
    # This matches the behavior implicitly required by the examples, which all have two groups.

    # Convert the result back to a NumPy array as per common practice in this context
    output_grid = np.array(output_list)
    
    return output_grid