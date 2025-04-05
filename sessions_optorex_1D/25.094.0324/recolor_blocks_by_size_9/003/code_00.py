import numpy as np

"""
Identifies contiguous groups of the digit '3' in the input sequence.
Compares the lengths of the first two such groups found.
If the first group (ordered left-to-right) is shorter than the second, replaces the first group with '2's and the second with '1's in the output.
Otherwise (if the first group is longer or equal in length to the second), replaces the first group with '1's and the second with '2's in the output.
Digits '0' remain unchanged.
The output sequence has the same length as the input sequence. Assumes exactly two groups of '3's exist in the input based on training examples.
"""

def _find_groups_of_threes(data):
    """
    Helper function to find start index, end index, and length of 
    contiguous groups of '3's in a list or 1D numpy array.

    Args:
        data: A list or 1D numpy array of integers.

    Returns:
        A list of dictionaries, where each dictionary contains 'start', 'end', 
        and 'len' for a group of '3's. Returns an empty list if no groups are found.
    """
    groups = []
    in_group = False
    start_index = -1
    n = len(data)
    
    for i, val in enumerate(data):
        if val == 3 and not in_group:
            # Start of a new group
            in_group = True
            start_index = i
        elif val != 3 and in_group:
            # End of the current group (before the current index)
            in_group = False
            end_index = i - 1
            groups.append({'start': start_index, 'end': end_index, 'len': end_index - start_index + 1})
            start_index = -1 # Reset start_index
            
    # Handle case where the sequence ends with a group of 3s
    if in_group:
        end_index = n - 1
        groups.append({'start': start_index, 'end': end_index, 'len': end_index - start_index + 1})
        
    return groups

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms an input sequence (1D numpy array) based on the relative lengths 
    of the first two groups of '3's.

    Args:
        input_grid: A 1D numpy array containing integers (expected 0s and 3s).

    Returns:
        A 1D numpy array representing the transformed sequence.
    """
    # Ensure input is treated as a 1D sequence
    if input_grid.ndim > 1:
         # Assuming the task implies a 1D sequence based on examples
         # If multi-dimensional grids are possible, logic needs adjustment
         # For now, flatten or handle the first row if appropriate.
         # Let's assume flattening is okay, or raise error if ambiguity exists.
         # Based on examples, it's always 1D.
         input_sequence = input_grid.flatten() # Or handle error
    else:
         input_sequence = input_grid

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_sequence)

    # Find the contiguous groups of '3's
    three_groups = _find_groups_of_threes(input_sequence)

    # Proceed only if exactly two groups are found (as per observed pattern)
    if len(three_groups) == 2:
        group1_info = three_groups[0]
        group2_info = three_groups[1]

        # Get lengths
        len1 = group1_info['len']
        len2 = group2_info['len']

        # Determine replacement values based on length comparison
        if len1 < len2:
            val1 = 2 # First group is shorter, replace with 2
            val2 = 1 # Second group is longer, replace with 1
        else: # Covers len1 >= len2
            val1 = 1 # First group is longer or equal, replace with 1
            val2 = 2 # Second group is shorter or equal, replace with 2

        # Apply transformations to the output grid
        # Replace first group
        start1, end1 = group1_info['start'], group1_info['end']
        output_grid[start1 : end1 + 1] = val1

        # Replace second group
        start2, end2 = group2_info['start'], group2_info['end']
        output_grid[start2 : end2 + 1] = val2
        
    # If not exactly two groups, the current logic returns the original grid copy implicitly.
    # Depending on requirements, an error could be raised or different logic applied.

    # Reshape back to original grid shape if it was multi-dimensional?
    # Based on examples, output is always 1D, so reshaping might not be needed.
    # If the original input_grid could be e.g., (1, N), return (1, N)?
    # Let's assume output should match input dimensionality if > 1D.
    if input_grid.ndim > 1:
        output_grid = output_grid.reshape(input_grid.shape)

    return output_grid