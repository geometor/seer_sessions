```python
"""
Transforms a sequence of 12 integers (provided as a list or NumPy array). It identifies the 
first non-zero integer ('active_digit') in the input sequence. It then initializes an output 
sequence as a copy of the input. It iterates through the input sequence from index 3 to 10. 
If an element at index 'i' in the input matches the 'active_digit', it sets the elements at 
indices i-1, i, and i+1 in the output sequence to the 'active_digit'. Finally, it returns 
the modified output sequence, maintaining the original input type (list or NumPy array).
"""

import numpy as np

def find_active_digit(sequence):
    """ 
    Finds the first non-zero digit in the input sequence (list or NumPy array).
    Returns the digit or None if all elements are zero.
    """
    for digit in sequence:
        if digit != 0:
            return digit
    return None

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence (list or NumPy array).
    """
    # Determine the input type to return the same type
    input_is_numpy = isinstance(input_sequence, np.ndarray)

    # Work with a NumPy array for efficient copying and element access
    # Convert if input is a list
    if not input_is_numpy:
        input_array = np.array(input_sequence, dtype=int)
    else:
        input_array = input_sequence.astype(int) # Ensure integer type

    # Validate sequence length
    if input_array.shape != (12,):
         raise ValueError(f"Input sequence must have exactly 12 elements, found shape {input_array.shape}")

    # Initialize the output sequence as a modifiable copy of the input
    output_array = input_array.copy()

    # Identify the non-zero "active digit" using the helper function
    active_digit = find_active_digit(input_array)

    # If no active digit is found (input is all zeros), return the original sequence unchanged
    # Ensure the return type matches the input type
    if active_digit is None:
        return input_sequence # Return the original input object

    # Iterate through the *input* array indices where a trigger might occur.
    # The rule applies for triggers at index i > 2 (indices 3 to 10).
    # This range ensures indices i-1 (min 2) and i+1 (max 11) are valid for a length-12 array.
    for i in range(3, 11):
        # Check if the element at the current index 'i' in the *original input* array
        # matches the identified active digit.
        if input_array[i] == active_digit:
            # If a trigger is found, modify the *output* array.
            # Set the elements at index i-1, i, and i+1 to the active digit.
            output_array[i - 1] = active_digit
            output_array[i] = active_digit
            output_array[i + 1] = active_digit

    # Return the modified output sequence in the same format as the input
    if input_is_numpy:
        return output_array
    else:
        # Convert back to list if the original input was a list
        return output_array.tolist()
```