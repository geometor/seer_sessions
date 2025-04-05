import numpy as np
import math

"""
Processes a sequence of integers (provided as a NumPy array).
The transformation rule depends on the value of the first element:
1. If the first element is 0:
   - The element at index 0 is moved to the end of the sequence.
2. If the first element is not 0:
   - Find the index of the first occurrence of 0.
   - The element immediately *preceding* the first 0 is moved to the end of the sequence.
The modified sequence is returned as a list of integers.
"""

# Helper function to find the index of the first occurrence of a value
def find_first_occurrence_index(sequence, value):
    """
    Finds the index of the first occurrence of a specific value in the sequence.
    
    Args:
        sequence: A list or NumPy array.
        value: The value to search for.
        
    Returns:
        The index of the first occurrence, or -1 if not found.
    """
    try:
        # Convert to list to use the index method reliably
        return list(sequence).index(value)
    except ValueError:
        return -1 # Value not found

# Helper function to move an element from a specific index to the end
def move_element_to_end(sequence_list, index_to_move):
    """
    Moves the element at the specified index to the end of the list.
    Modifies the list in place, but also returns it for convenience.

    Args:
        sequence_list: The list to modify.
        index_to_move: The index of the element to move.

    Returns:
        The modified list. Returns the original list if index is invalid.
    """
    # Check if index is valid
    if 0 <= index_to_move < len(sequence_list):
        # Remove the element at the specified index and get its value
        element_to_move = sequence_list.pop(index_to_move)
        # Append the removed element to the end
        sequence_list.append(element_to_move)
    # If index is invalid, the list remains unchanged
    return sequence_list

def transform(input_grid: np.ndarray):
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_grid: A 1D NumPy array of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    
    # Ensure input is treated as a sequence (convert NumPy array to list for easier manipulation)
    working_list = list(input_grid)
    
    # Handle empty input sequence
    if not working_list:
        return [] # Return an empty list

    # Get the scalar value of the first element
    # No NumPy ambiguity here as we access a specific index
    first_element_value = working_list[0] 
    
    # Initialize the index of the element to be moved
    target_index = -1 

    # --- Determine the index of the element to move ---
    if first_element_value == 0:
        # Case 1: The first element is 0.
        # The target element is the one at index 0.
        target_index = 0
    else:
        # Case 2: The first element is not 0.
        # Find the index of the first occurrence of 0.
        first_zero_idx = find_first_occurrence_index(working_list, 0)
        
        # Check if 0 was found and if it's not the very first element
        # (The second condition is implicitly covered by first_element_value != 0 check)
        if first_zero_idx > 0:
            # The target element is the one immediately *before* the first 0.
            target_index = first_zero_idx - 1
        else:
            # Handle unexpected cases where the rule cannot be applied:
            # - 0 is not found (first_zero_idx == -1)
            # - 0 is the first element (first_zero_idx == 0), but this contradicts the `else` branch.
            # Based on examples, these cases shouldn't occur. If they did, returning
            # the list unchanged might be a safe default.
            return working_list # Return original list if rule cannot be applied

    # --- Perform the move operation ---
    # Use the helper function to move the element at target_index to the end
    # The move_element_to_end function modifies the list in place
    output_list = move_element_to_end(working_list, target_index)

    # Return the transformed list
    return output_list