"""
Transforms a 2D NumPy array (grid) of integers. The transformation is applied 
independently to each row. Within each row, it identifies contiguous horizontal 
groups of identical non-zero numbers. If a group's length is greater than 2, 
only the first and last elements of the group are kept in their original 
positions in the output grid's row, and the elements between them are set to 0. 
Groups of length 2 or less, and zeros outside of these groups, remain unchanged.
"""

import numpy as np

def find_groups_in_row(row: np.ndarray):
    """
    Identifies contiguous groups of identical non-zero numbers in a 1D NumPy array (row).

    Args:
        row: A 1D NumPy array of integers representing a single row.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'value', 'start_index', 'end_index', and 'length'.
    """
    groups = []
    i = 0
    n = len(row)
    while i < n:
        # Check if the current element is non-zero
        if row[i] != 0:
            value = row[i]
            start_index = i
            
            # Find the end of the contiguous group of the same value
            j = i + 1
            while j < n and row[j] == value:
                j += 1
            end_index = j - 1 # Inclusive index of the last element
            length = end_index - start_index + 1
            
            # Record the found group
            groups.append({
                'value': value,
                'start_index': start_index,
                'end_index': end_index,
                'length': length
            })
            
            # Move the main index past this group
            i = end_index + 1
        else:
            # Move to the next element if it's zero
            i += 1
    return groups

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the row-wise transformation rule to the input 2D NumPy array.

    Args:
        input_grid: A 2D NumPy array of integers.

    Returns:
        A 2D NumPy array with the transformation applied to each row.
    """
    # Initialize the output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the number of rows in the grid
    num_rows = input_grid.shape[0]
    
    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Extract the current row
        current_row = input_grid[r, :]
        
        # Find all contiguous groups of identical non-zero numbers in this row
        groups_in_row = find_groups_in_row(current_row)
        
        # Iterate through each identified group in the current row
        for group in groups_in_row:
            # Check if the length of the group is greater than 2
            if group['length'] > 2:
                # If the length is greater than 2, calculate the indices to modify
                # Column index immediately after the start of the group
                start_modify_col = group['start_index'] + 1
                # Column index of the last element in the group (exclusive for slicing)
                end_modify_col = group['end_index'] 
                
                # Ensure there are elements between the first and last to modify
                if start_modify_col < end_modify_col:
                    # Set the elements in the corresponding row of the output grid 
                    # between the first and last element of the group to 0
                    output_grid[r, start_modify_col:end_modify_col] = 0
                    
    # Return the final modified grid
    return output_grid