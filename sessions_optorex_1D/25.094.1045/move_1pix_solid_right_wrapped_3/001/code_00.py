import math # Not used, but included per template convention
import copy # Not used, list() creates a shallow copy sufficient here

"""
Scan the input sequence from left to right. Find the first index 'i' where the digit at 'i' is different from the digit at 'i+1'. 
If such an index 'i' is found, remember the digit originally at index 'i', remove the last digit of the sequence, and then insert the remembered digit into the sequence at index 'i+1'.
If no such difference is found (i.e., all adjacent elements are the same, or the sequence has fewer than two elements), return the sequence unchanged.
"""

def transform(input_grid):
    """
    Transforms the input sequence based on the first adjacent difference found.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    n = len(input_grid)
    
    # Handle sequences with less than 2 elements, as no adjacent pair exists
    if n < 2:
        # Return a copy to avoid modifying the original input if it were mutable elsewhere
        return list(input_grid) 

    # Iterate through the sequence to find the first index 'i' where
    # the element at 'i' differs from the element at 'i+1'.
    diff_index = -1 
    for i in range(n - 1):
        if input_grid[i] != input_grid[i+1]:
            diff_index = i
            # Stop searching once the first difference is found
            break 

    # If no difference was found after checking all adjacent pairs
    if diff_index == -1:
        # Return a copy of the original sequence
        return list(input_grid) 
    
    # If a difference was found at diff_index
    else:
        # Create a mutable copy of the input sequence to modify
        output_grid = list(input_grid) 
        
        # Remember the digit at the location of the detected difference
        digit_to_move = output_grid[diff_index] 
        
        # Remove the last element from the copied sequence
        output_grid.pop() 
        
        # Insert the remembered digit into the copied sequence 
        # at the position immediately following the original difference index.
        # This effectively shifts elements from index diff_index + 1 onwards to the right.
        output_grid.insert(diff_index + 1, digit_to_move) 
        
        # Return the modified sequence
        return output_grid
