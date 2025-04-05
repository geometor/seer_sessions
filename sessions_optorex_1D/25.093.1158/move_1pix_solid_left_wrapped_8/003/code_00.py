"""
Transforms an input sequence (represented as a 1D NumPy array) by performing a left rotation.
The first element (at index 0) of the input sequence is moved to the last position, 
and all other elements are shifted one position to the left.
"""

import collections
import numpy as np

def transform(input_grid: np.ndarray) -> list:
    """
    Rotates the elements of the input 1D NumPy array one position to the left.

    Args:
        input_grid: A 1D NumPy array of numbers.

    Returns:
        A new list representing the left-rotated sequence.
    """
    
    # Check if the input array is empty. Use .size for NumPy arrays.
    if input_grid.size == 0:
        # Return an empty list if the input is empty
        return []
        
    # Check if the input array has only one element, rotation has no effect.
    if input_grid.size < 2:
        # Return a list copy of the single-element array
        return input_grid.tolist()

    # Create a deque from the input NumPy array.
    # Deques efficiently handle adding/removing elements from both ends.
    d = collections.deque(input_grid)
    
    # Perform one left rotation.
    # The rotate(-1) method moves the leftmost element to the rightmost position.
    d.rotate(-1) 
    
    # Convert the deque back to a standard Python list for the output.
    output_sequence = list(d)

    return output_sequence