"""
Transforms an input sequence by performing a cyclic shift (rotation) 
of all elements two positions to the left. The element originally at index i 
moves to index (i - 2) mod L, where L is the length of the sequence.
"""

import numpy as np # Using numpy for efficient array operations like roll

def transform(input_grid):
    """
    Applies a left cyclic shift of 2 positions to the input sequence.

    Args:
        input_grid: A list or NumPy array representing the sequence of integers.

    Returns:
        A list or NumPy array (matching input type if possible) representing 
        the transformed sequence.
    """
    
    # Determine if the input is a NumPy array to return the same type
    is_numpy = isinstance(input_grid, np.ndarray)
    
    # Convert input to a NumPy array for easier shifting, handle potential errors
    try:
        input_array = np.array(input_grid)
    except Exception as e:
        raise TypeError(f"Input could not be converted to a NumPy array: {e}")

    # Get the length of the sequence
    length = len(input_array)

    # Handle empty input case
    if length == 0:
        # Return an empty structure matching the input type if possible
        return np.array([]) if is_numpy else []
        
    # Perform the left cyclic shift by 2 positions
    # np.roll shifts elements to the right by default, so use a negative shift value for left shift
    output_array = np.roll(input_array, -2)
    
    # Convert back to a list if the original input was a list
    if not is_numpy:
        output_grid = output_array.tolist()
    else:
        # Keep it as a NumPy array if the input was an array
        output_grid = output_array
    
    return output_grid
