```python
"""
Transforms an input sequence of 12 integers by shifting its elements 4 positions to the right. 
The first 4 positions of the output sequence are filled with 0. 
The last 4 elements of the original input sequence are discarded.
"""

import numpy as np

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Shifts the elements of a 1D integer sequence (NumPy array) to the right.

    Args:
        input_sequence: A 1D NumPy array containing 12 integers. 
                        (Note: Although the template arg name is 'input_grid', 
                         this function assumes a 1D input based on the examples provided).

    Returns:
        A 1D NumPy array containing the transformed 12 integers.
    """
    
    # Define transformation parameters
    sequence_length = 12  # Expected length of the input sequence
    shift_amount = 4      # Number of positions to shift right
    fill_value = 0        # Value to use for padding
    
    # Validate input shape (optional but good practice)
    if input_sequence.ndim != 1 or input_sequence.shape[0] != sequence_length:
        # If the input isn't the expected 1D array of length 12, 
        # handle appropriately. For now, raise an error or attempt reshape if needed.
        # Based on prior attempts and typical ARC tasks, the test harness might
        # provide the input flattened even if it represents a grid conceptually.
        # Assuming it provides a flat 1D array matching the examples.
        # If it was, e.g., a 3x4 grid flattened, input_sequence.shape[0] would be 12.
        # Let's proceed assuming it's already a 1D array of length 12.
        # Consider adding error handling if strict validation is required.
         pass # No strict validation for now, proceed assuming correct format.


    # Create the prefix array filled with the fill value
    # This array will contain 'shift_amount' number of 'fill_value' elements
    prefix = np.full(shift_amount, fill_value, dtype=input_sequence.dtype) 
    
    # Select the elements from the input sequence that will be kept
    # These are the first 'sequence_length - shift_amount' elements
    # i.e., elements from index 0 up to (but not including) index 8
    elements_to_keep = input_sequence[:sequence_length - shift_amount]
    
    # Construct the output sequence by concatenating the prefix and the kept elements
    output_sequence = np.concatenate((prefix, elements_to_keep))
    
    return output_sequence
```