import numpy as np

"""
Transforms a 1D sequence containing 0s and 3s by identifying exactly two contiguous groups 
of 3s and replacing them based on their relative lengths. Zeros remain unchanged.

The transformation logic is as follows:
1. Identify all contiguous groups (subsequences) consisting solely of the number 3.
2. The logic specifically applies only when exactly two such groups are found. Let Group1 be 
   the group that appears first (smaller start index) and Group2 be the group that appears second.
3. Compare the lengths of Group1 and Group2.
4. If Group1 is strictly longer than Group2, replace the 3s in Group1 with 1s and the 3s 
   in Group2 with 2s in the output sequence.
5. Otherwise (if Group1 is shorter than or equal in length to Group2), replace the 3s in 
   Group1 with 2s and the 3s in Group2 with 1s in the output sequence.
6. Keep all 0s unchanged in their original positions.
7. If the number of groups of 3s is not exactly two, the input sequence is returned unchanged.
"""

def find_groups_of_threes(numbers):
    """
    Finds contiguous groups of the number 3 in a list or 1D array of numbers.

    Args:
        numbers: A list or 1D NumPy array of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start' index (inclusive), 'end' index (inclusive), 
        and 'length'. Returns an empty list if no groups of 3 are found.
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
        # Move to the next number after the group or the current number if it wasn't 3
        i += 1 
    return groups

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence.
    
    Args:
        input_grid: A 1D NumPy array representing the sequence of numbers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Convert input NumPy array to a list for easier iteration and modification.
    input_list = input_grid.tolist() 
    
    # Initialize output_list as a copy of the input list. 
    # This ensures zeros are preserved and provides a base for modification.
    # If the transformation condition (exactly two groups) isn't met, 
    # this unmodified copy will be returned.
    output_list = list(input_list) 

    # Find all contiguous groups of the number 3 in the input list.
    groups = find_groups_of_threes(input_list)

    # Apply transformation logic only if exactly two groups are found.
    if len(groups) == 2:
        group1 = groups[0] # The first group encountered
        group2 = groups[1] # The second group encountered

        # Compare the lengths of the two groups to determine the replacement values.
        # If group1 is strictly longer, it gets replaced by 1s, and group2 by 2s.
        # Otherwise (group1 is shorter or equal), group1 gets 2s, and group2 gets 1s.
        val1, val2 = (1, 2) if group1['length'] > group2['length'] else (2, 1)

        # Modify the output list based on the determined values.
        # Replace 3s in the first group's range (inclusive) with val1.
        for i in range(group1['start'], group1['end'] + 1):
             output_list[i] = val1 # Modify the copy

        # Replace 3s in the second group's range (inclusive) with val2.
        for i in range(group2['start'], group2['end'] + 1):
             output_list[i] = val2 # Modify the copy
            
    # If the number of groups is not exactly 2, the 'output_list' remains 
    # the initial copy of 'input_list', effectively returning the input unchanged.

    # Convert the final list back to a NumPy array with the same data type 
    # as the original input grid.
    output_grid = np.array(output_list, dtype=input_grid.dtype) 
    
    return output_grid