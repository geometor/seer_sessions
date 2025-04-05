"""
Transforms an input sequence of integers by performing a right cyclic shift 
by one position. The last element of the input sequence becomes the first 
element of the output sequence, and all other elements are shifted one 
position to the right, maintaining their relative order.
"""

from collections import deque
import numpy as np # Import numpy as input might be an ndarray

def transform(input_sequence):
    """
    Performs a right cyclic shift by one position on the input sequence.
    
    Args:
        input_sequence (list or numpy.ndarray): A sequence of integers.
        
    Returns:
        list or numpy.ndarray: The transformed sequence, with the last element
                               moved to the first position. The return type
                               matches the input type.
    """

    # Store the original type to ensure the output type matches the input type
    input_type = type(input_sequence)
    original_dtype = None # Store dtype for numpy arrays

    # Handle different input types and convert to a list for processing
    if isinstance(input_sequence, np.ndarray):
        # Check for empty array case first
        if input_sequence.size == 0:
            return np.array([]) # Return empty ndarray
        original_dtype = input_sequence.dtype # Store original dtype
        sequence_list = input_sequence.tolist()
    elif isinstance(input_sequence, (list, tuple)):
        # Check for empty list/tuple case
        if not input_sequence:
             # Return empty list for either list or tuple input
            return [] 
        sequence_list = list(input_sequence) # Convert tuple to list if necessary
    else:
        # Raise an error if the input type is not supported
        raise TypeError(f"Unsupported input type: {input_type}. Expected list, tuple, or numpy.ndarray.")

    # Use deque for efficient rotation operations
    # 1. Receive the input sequence of integers (converted to list).
    d = deque(sequence_list)

    # Perform the rotation only if there's more than one element
    if len(d) > 1:
        # 2. Identify the element at the last position (implicitly done by rotate).
        # 3. Identify the subsequence excluding the last element (implicitly done by rotate).
        # 4. Place the identified last element at the beginning.
        # 5. Append the identified subsequence.
        # Steps 2-5 are efficiently handled by deque.rotate(1)
        d.rotate(1) # Rotates the deque 1 step to the right in-place

    # Convert the deque back to the original input type
    # 6. Return the resulting output sequence.
    if input_type == np.ndarray:
        # Convert deque back to numpy array, preserving original dtype if possible
        output_sequence = np.array(d, dtype=original_dtype) 
    else:
        # Convert deque back to a list (handles original list/tuple inputs)
        output_sequence = list(d) 

    return output_sequence