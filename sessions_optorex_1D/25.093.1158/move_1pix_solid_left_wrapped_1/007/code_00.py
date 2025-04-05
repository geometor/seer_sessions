import numpy as np
import math

"""
Processes a sequence of integers provided as a 1xN NumPy array.
The transformation rule depends on the value of the first element ([0, 0]):
1. If the first element is 0:
   - The element at index 0 of the sequence (corresponding to grid index [0, 0]) is moved to the end.
2. If the first element is not 0:
   - Find the index of the first occurrence of 0 within the sequence (first row of the grid).
   - The element immediately *preceding* this first 0 is moved to the end of the sequence.
The modified sequence is returned as a Python list.
"""

# Helper function to find the index of the first occurrence of a value in a list
def find_first_occurrence_index(sequence_list, value):
    """
    Finds the index of the first occurrence of a specific value in the list.
    
    Args:
        sequence_list: The list to search within.
        value: The value to search for.
        
    Returns:
        The index of the first occurrence, or -1 if not found.
    """
    try:
        return sequence_list.index(value)
    except ValueError:
        return -1 # Value not found

# Helper function to move an element from a specific index to the end of a list
def move_element_to_end(sequence_list, index_to_move):
    """
    Moves the element at the specified index to the end of the list.
    Modifies the list in place and returns it.

    Args:
        sequence_list: The list to modify.
        index_to_move: The index of the element to move.

    Returns:
        The modified list. Returns the original list if index is invalid.
    """
    # Check if index is valid for the list length
    if 0 <= index_to_move < len(sequence_list):
        # Remove the element at the specified index and capture its value
        element_to_move = sequence_list.pop(index_to_move)
        # Append the removed element to the end of the list
        sequence_list.append(element_to_move)
    # If index is invalid, the list remains unchanged
    return sequence_list

def transform(input_grid: np.ndarray):
    """
    Applies the transformation rule to the input sequence represented by the first row of the NumPy grid.

    Args:
        input_grid: A NumPy array, assumed to be shape (1, N), containing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    
    # Validate input shape - assuming it must have at least one row
    if input_grid.shape[0] < 1:
        # Handle cases with zero rows if necessary, returning empty list for now
        return []

    # Extract the first row of the grid into a Python list for manipulation
    working_list = list(input_grid[0])
    
    # Handle empty sequence case (if the first row was empty)
    if not working_list:
        return [] # Return an empty list

    # Get the value of the first element in the sequence
    first_element_value = working_list[0] 
    
    # Initialize the index of the element to be moved
    target_index = -1 

    # --- Determine the index of the element to move based on the first element's value ---
    if first_element_value == 0:
        # Case 1: The first element is 0.
        # The target element is the one at index 0.
        target_index = 0
    else:
        # Case 2: The first element is not 0.
        # Find the index of the first occurrence of 0 in the list.
        first_zero_idx = find_first_occurrence_index(working_list, 0)
        
        # Check if 0 was found and if it's located *after* the first position.
        # If 0 is at index 0, this 'else' block shouldn't have been entered.
        # If 0 is not found (first_zero_idx == -1), the rule cannot be applied.
        if first_zero_idx > 0:
            # The target element is the one immediately *before* the first 0.
            target_index = first_zero_idx - 1
        else:
            # Handle unexpected cases:
            # - 0 not found.
            # - 0 is the first element (but code execution shouldn't reach here if first_element_value != 0).
            # In these scenarios (based on examples, they shouldn't occur), return the list unchanged as a safe default.
            return working_list # Return original list if rule cannot be applied as expected

    # --- Perform the move operation ---
    # Use the helper function to move the element at the calculated target_index to the end.
    # This modifies working_list in place and also returns it.
    output_list = move_element_to_end(working_list, target_index)

    # Return the transformed list
    return output_list