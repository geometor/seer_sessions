```python
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
    
    # Handle potential numpy array input by converting to list for deque
    if isinstance(input_sequence, np.ndarray):
        # Check for empty array case first
        if input_sequence.size == 0:
            return np.array([]) # Return empty ndarray
        sequence_list = input_sequence.tolist()
    # Handle list or tuple input
    elif isinstance(input_sequence, (list, tuple)):
        # Check for empty list/tuple case
        if not input_sequence:
             # Return empty list for either list or tuple input
            return [] 
        sequence_list = list(input_sequence) # Convert tuple to list if necessary
    else:
        # Raise an error if the input type is not supported
        raise TypeError(f"Unsupported input type: {input_type}. Expected list or numpy.ndarray.")

    # Use deque for efficient rotation operations
    d = deque(sequence_list)

    # Only rotate if there's more than one element
    if len(d) > 1:
        # Perform the right cyclic rotation by 1 position
        # deque.rotate(n) rotates right by n steps for positive n
        d.rotate(1)

    # Convert the deque back to the original input type
    if input_type == np.ndarray:
        # Convert deque back to numpy array
        output_sequence = np.array(d, dtype=input_sequence.dtype) # Preserve original dtype if possible
    else:
        # Convert deque back to a list (handles original list/tuple inputs)
        output_sequence = list(d) 

    return output_sequence
```