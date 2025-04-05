```python
"""
Transforms an input sequence of integers by moving the last element 
to the first position, effectively performing a right cyclic rotation 
by one position.

1. Receive the input sequence of integers (represented as a list or array).
2. Identify the element located at the last position of the input sequence.
3. Create a new sequence by taking all elements from the input sequence *except* the last one, maintaining their original relative order.
4. Construct the output sequence by placing the identified last element at the very beginning, followed immediately by the sequence created in step 3.
5. Return the resulting output sequence.
"""

from collections import deque
import numpy as np # Import numpy to handle potential ndarray input

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

    # Store original type to return the same type
    input_type = type(input_sequence)

    # Convert input sequence to a list to handle both list and ndarray uniformly
    # before creating the deque
    if isinstance(input_sequence, np.ndarray):
        sequence_list = input_sequence.tolist()
    elif isinstance(input_sequence, (list, tuple)):
         # Convert tuple to list if necessary, handle list directly
        sequence_list = list(input_sequence)
    else:
        # Raise an error or handle other unexpected types if necessary
        raise TypeError(f"Unsupported input type: {input_type}")

    # Use deque for efficient rotation
    d = deque(sequence_list)

    # Handle empty sequence case
    if not d:
        if input_type == np.ndarray:
            return np.array([]) # Return empty ndarray
        else:
            return [] # Return empty list

    # Perform the right cyclic rotation by 1 position
    # deque.rotate(n) rotates right by n steps (positive n)
    d.rotate(1)

    # Convert the deque back to the original input type
    if input_type == np.ndarray:
        output_sequence = np.array(d)
    else:
        # Default to returning a list for list or tuple input
        output_sequence = list(d) 

    return output_sequence
```