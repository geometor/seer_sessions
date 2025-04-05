import math
import numpy as np # Import numpy as the input might be an array

"""
Transforms an input sequence (list or NumPy array) of numbers by performing 
a cyclic shift (rotation) of all elements two positions to the left. 
The element originally at index i moves to index (i - 2) mod L, where L 
is the length of the sequence.
"""

def transform(input_grid):
    """
    Applies a left cyclic shift of 2 positions to the input sequence.

    Args:
        input_grid: A list or NumPy array representing the sequence of integers.

    Returns:
        A list or NumPy array (matching input type if possible) representing 
        the transformed sequence.
    """
    
    # Determine the length of the input sequence
    try:
        length = len(input_grid)
    except TypeError:
        # Handle cases where len() might not be directly applicable, though unlikely for lists/arrays
        print("Error: Input does not have a defined length.")
        return None # Or raise an error

    # Handle empty input case
    if length == 0:
        # Return an empty structure matching the input type if possible
        if isinstance(input_grid, np.ndarray):
            return np.array([])
        else:
            return []
        
    # Initialize the output grid. Using a list initially is simpler.
    # We can convert back to numpy array at the end if needed.
    output_list = [0] * length 
    
    # Perform the cyclic shift
    for i in range(length):
        # Calculate the new index after shifting 2 positions left, wrapping around
        # The modulo operator handles the wrap-around logic correctly
        new_index = (i - 2) % length 
        
        # Place the element from the original index i into the new index
        output_list[new_index] = input_grid[i]
        
    # If the input was a NumPy array, convert the output list back to a NumPy array
    if isinstance(input_grid, np.ndarray):
        output_grid = np.array(output_list)
    else:
        # Otherwise, keep it as a list
        output_grid = output_list
    
    return output_grid