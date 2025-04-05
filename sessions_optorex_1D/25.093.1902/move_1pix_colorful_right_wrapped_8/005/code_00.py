"""
Transforms an input sequence by moving the element at the last index to the 
first index (index 0) and shifting all preceding elements one position to 
the right. This is equivalent to a right circular shift.
"""

import numpy as np # Import numpy as input might be an array

def transform(input_sequence: list[int] or np.ndarray) -> list[int]:
    """
    Performs a right circular shift on the input sequence.

    Args:
        input_sequence: A list of integers or a NumPy array representing the 
                        input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """

    # Check if the input sequence has less than 2 elements.
    # If so, rotation doesn't change the sequence.
    # Using len() works for both standard lists and NumPy arrays.
    if len(input_sequence) < 2:
        # Return a copy if it's a list, or convert to list if it's NumPy
        if isinstance(input_sequence, np.ndarray):
            return input_sequence.tolist() 
        else:
            # Return a slice copy to avoid modifying the original list
            return input_sequence[:] 

    # Identify the number located at the very end (last position)
    # Slicing works similarly for lists and NumPy arrays.
    last_element = input_sequence[-1]

    # Get all the numbers from the input sequence, starting from the first 
    # number up to, but not including, the last number.
    remaining_elements = input_sequence[:-1]

    # Ensure remaining_elements is a list for concatenation, 
    # regardless of input type.
    if isinstance(remaining_elements, np.ndarray):
        remaining_elements_list = remaining_elements.tolist()
    else:
        # Use list() to handle potential tuples or other sequence types
        remaining_elements_list = list(remaining_elements) 

    # Construct the output sequence:
    # Start with the last element (as a single-item list).
    # Append the remaining elements.
    output_sequence = [last_element] + remaining_elements_list

    # The resulting sequence is the output.
    return output_sequence