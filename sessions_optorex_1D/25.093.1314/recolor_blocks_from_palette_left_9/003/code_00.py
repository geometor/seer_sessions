import numpy as np

"""
Transforms a 1D NumPy array of 12 integers.
1. Identifies all distinct groups of consecutive '5's in the input array.
2. Counts the number of such groups found ('k').
3. If k > 0, extracts the last 'k' integers from the input array as replacement values.
4. Creates a copy of the input array.
5. For each identified group of '5's (in order of appearance), replaces all '5's within that group in the copied array with the corresponding replacement value (also in order).
6. Returns the modified array. If k=0, returns the original array.
"""

def _find_consecutive_groups_indices(sequence: np.ndarray, target_value: int) -> list:
    """
    Finds groups of consecutive target_value in the sequence.
    Returns a list of lists, where each inner list contains the indices
    belonging to a single consecutive group.
    """
    groups_indices = []
    current_group_indices = []
    in_group = False
    
    # Iterate through the sequence with index
    for i, value in enumerate(sequence):
        if value == target_value:
            # Start or continue a group
            if not in_group:
                in_group = True
                current_group_indices = [i]
            else:
                current_group_indices.append(i)
        else:
            # End a group if we were in one
            if in_group:
                groups_indices.append(current_group_indices)
                in_group = False
                current_group_indices = []
            # Otherwise, just continue (value is not target_value and not in_group)

    # Handle a group that might end at the very last element
    if in_group:
        groups_indices.append(current_group_indices)

    return groups_indices

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # Ensure input is a numpy array (though type hint suggests it is)
    if not isinstance(input_grid, np.ndarray):
         # Or handle conversion if possible/desired
        raise TypeError("Input must be a NumPy array")
        
    if input_grid.ndim != 1 or input_grid.shape[0] != 12:
        raise ValueError("Input must be a 1D NumPy array of length 12")

    target_value = 5

    # 1. Identify all groups of consecutive '5's.
    groups = _find_consecutive_groups_indices(input_grid, target_value)

    # 2. Determine the number of replacement values needed (k).
    k = len(groups)

    # 3. Handle the case where no groups are found or k=0.
    if k == 0:
        return input_grid # Return original grid if no 5s groups

    # 4. Extract the last k integers as replacement values.
    # Check if enough elements exist for replacements (although k > 0 implies k <= 12 here)
    if k > len(input_grid):
         # This case is highly unlikely given the problem constraints but good practice
         raise ValueError("Error: More groups found than elements available for replacement.")
    replacement_values = input_grid[-k:]

    # 5. Create a copy of the input sequence to serve as the output sequence.
    output_grid = input_grid.copy()

    # 6. Iterate through groups and replacements, modify the output sequence.
    for i in range(k):
        group_indices = groups[i]       # Get indices for the current group
        replacement_val = replacement_values[i] # Get the corresponding replacement value

        # Use NumPy's ability to index with a list or array of indices
        # This efficiently assigns the replacement value to all elements at the specified indices.
        output_grid[group_indices] = replacement_val

    # 7. Return the modified output grid.
    return output_grid