```python
import numpy as np

"""
Transforms a 12-element sequence by shifting all non-zero elements 4 positions 
to the right. Positions vacated by the shift and any new positions at the 
beginning are filled with zeros. Elements shifted beyond the end of the 
sequence (index 11) are discarded.
"""

def transform(input_sequence):
    """
    Applies a right shift transformation to non-zero elements of the input sequence.

    Args:
        input_sequence: A NumPy array or list representing the 12-element input sequence.

    Returns:
        A NumPy array representing the transformed 12-element sequence.
    """
    # Define constants for clarity
    sequence_length = 12
    shift_amount = 4
    fill_value = 0

    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_sequence)

    # Initialize the output sequence with the fill value (zeros)
    # Using NumPy allows for efficient array operations if needed later,
    # and matches the likely input type based on previous errors.
    output_sequence = np.full(sequence_length, fill_value, dtype=input_array.dtype)

    # Iterate through the input sequence using index 'i'
    for i in range(sequence_length):
        # Get the element at the current index
        element = input_array[i]

        # Check if the element is non-zero
        if element != fill_value:
            # Calculate the target index after shifting
            target_index = i + shift_amount

            # Check if the target index is within the bounds of the sequence (0 to 11)
            if 0 <= target_index < sequence_length:
                # Copy the non-zero element to the target position in the output sequence
                output_sequence[target_index] = element
            # Else (target_index is out of bounds): the element is discarded (do nothing)

    # Return the resulting output sequence
    return output_sequence
```