import math
import numpy as np # Import numpy as the input might be an ndarray

"""
Processes a sequence of integers (provided as a list or NumPy array).
The transformation rule depends on the value of the first element:
1. If the first element is 0:
   - The element at index 0 is moved to the end of the sequence.
2. If the first element is not 0:
   - Find the index of the first occurrence of 0.
   - The element immediately *preceding* the first 0 is moved to the end of the sequence.
The modified sequence is returned as a list of integers.
"""

def find_first_zero_index(sequence):
    """Finds the index of the first occurrence of 0 in the sequence."""
    try:
        # Convert to list just in case input is numpy array, as index works easily
        return list(sequence).index(0)
    except ValueError:
        # Return -1 or raise an error if 0 is not found, based on expected behavior.
        # Based on examples, 0 seems guaranteed. Returning -1 for now.
        return -1 

def move_element_to_end(sequence, index_to_move):
    """Moves the element at the specified index to the end of the sequence."""
    # Convert to list for easier manipulation (handles both list and ndarray input)
    list_sequence = list(sequence)
    
    # Check if index is valid
    if 0 <= index_to_move < len(list_sequence):
        # Remove the element at the specified index
        element_to_move = list_sequence.pop(index_to_move)
        # Append the removed element to the end
        list_sequence.append(element_to_move)
        return list_sequence
    else:
        # If index is invalid, return the original sequence unchanged
        # Or potentially raise an error depending on requirements
        return list_sequence


def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    
    # Handle empty input sequence
    if len(input_sequence) == 0:
        return [] # Return an empty list for empty input

    # Convert input to list to ensure consistent handling
    working_list = list(input_sequence)
    
    # Get the value of the first element
    first_element = working_list[0]
    
    target_index = -1 # Initialize target index

    # Determine the index of the element to move
    if first_element == 0:
        # Case 1: First element is 0
        target_index = 0
    else:
        # Case 2: First element is not 0
        first_zero_idx = find_first_zero_index(working_list)
        
        # Ensure 0 was found and it's not the very first element (which contradicts this case)
        if first_zero_idx > 0:
            target_index = first_zero_idx - 1
        else:
            # Handle unexpected cases: 
            # - 0 not found (first_zero_idx == -1)
            # - 0 is the first element (first_zero_idx == 0, but first_element != 0 check already failed)
            # In these unlikely scenarios based on examples, we might return the list unchanged.
            return working_list # Return original list if rule cannot be applied as expected

    # Move the identified element to the end
    output_list = move_element_to_end(working_list, target_index)

    return output_list
