```python
"""
Identifies a contiguous block of identical non-zero integers (foreground object)
in the input sequence. Shifts this block 4 positions to the left within a
sequence of the same length, filling the remaining positions with zeros.
"""

import math # Not strictly needed for this logic, but included as per template availability
import numpy as np # Useful for array manipulation, though lists work too

BACKGROUND_VALUE = 0
SHIFT_AMOUNT = 4

def find_foreground_object(input_sequence):
    """
    Finds the first contiguous block of identical non-zero values.

    Args:
        input_sequence: A list of integers.

    Returns:
        A tuple (value, start_index, length) if an object is found,
        otherwise None.
    """
    start_index = -1
    value = -1
    length = 0

    for i, current_value in enumerate(input_sequence):
        if current_value != BACKGROUND_VALUE:
            # Found the start of a potential object
            if start_index == -1:
                start_index = i
                value = current_value
                length = 1
            # Continuing an existing object
            elif current_value == value:
                length += 1
            # Found a different non-zero value (shouldn't happen based on examples)
            # or reached the end of the object
            else:
                # This case isn't expected based on the examples provided,
                # where only one contiguous block exists. If it did, we'd stop here.
                 break # Found the end of the first object
        elif start_index != -1:
            # We were tracking an object, but hit a background value, so the object ends
            break

    if start_index != -1:
        return value, start_index, length
    else:
        # No non-zero object found
        return None

def transform(input_grid):
    """
    Transforms the input sequence by shifting the foreground object left.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # 1. Initialize an output sequence of the same length, filled with zeros.
    sequence_length = len(input_grid)
    output_grid = [BACKGROUND_VALUE] * sequence_length

    # 2. & 3. Scan the input sequence to find the foreground object details.
    object_info = find_foreground_object(input_grid)

    if object_info:
        value, start_index, length = object_info

        # 4. Calculate the new start index.
        new_start_index = start_index - SHIFT_AMOUNT

        # Ensure the new start index is within bounds (optional based on examples)
        # new_start_index = max(0, new_start_index) # Prevent negative indices

        # 5. Place the identified foreground object into the output sequence.
        for i in range(length):
            # Calculate the index in the output grid
            output_index = new_start_index + i
            # Place the value if the index is within the grid boundaries
            if 0 <= output_index < sequence_length:
                output_grid[output_index] = value
            # else: handle cases where the shifted object goes out of bounds if necessary

    # 6. Return the modified output sequence.
    return output_grid
```