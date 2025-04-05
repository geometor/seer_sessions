
## train_1

**input:**
```
0 0 0 0 3 3 3 0 0 0 0 0
```


**output:**
```
3 3 3 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 7 0 0 0
```


**output:**
```
0 0 0 0 7 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 6 6 6 6 6 0 0 0
```


**output:**
```
6 6 6 6 6 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 6 6 6 6 6 0
```


**output:**
```
0 0 6 6 6 6 6 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 5 0 0 0 0 0 0 0
```


**output:**
```
5 0 0 0 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 2 2 2 2 2 2 2
```


**output:**
```
0 2 2 2 2 2 2 2 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 0 9 9 0
```


**output:**
```
0 0 0 0 0 9 9 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are sequences (or lists) of 12 single-digit integers.
    *   Each input sequence contains a contiguous block of identical non-zero digits, surrounded by zeros.
    *   The output sequence contains the same block of non-zero digits as the input, but its position within the sequence has changed. The remaining elements are zeros.
*   **YAML Facts:**
    
```yaml
    task_elements:
      - type: sequence
        length: 12
        element_type: integer
        range: 0-9
    input_structure:
      - contains: background
        value: 0
      - contains: object
        description: A contiguous block of identical non-zero digits.
        properties:
          - value: non-zero integer (constant within the block)
          - length: variable
          - position: variable
    output_structure:
      - contains: background
        value: 0
      - contains: object
        description: The same object from the input sequence.
        properties:
          - value: same as input object
          - length: same as input object
          - position: shifted relative to input
    transformation:
      - action: identify_object
        target: the contiguous block of non-zero digits
      - action: shift_object
        direction: left
        magnitude: 4 positions
      - action: maintain_background
        value: 0
      - action: handle_boundaries
        description: Positions vacated by the shift are filled with 0. Elements shifted beyond the start boundary are implicitly discarded (though not observed in examples). Elements to the left of the original object remain 0 until potentially overwritten by the shifted object.

    ```

*   **Natural Language Program:**
    1.  Identify the contiguous block of identical non-zero numbers within the input sequence. Note its starting position, length, and the digit value.
    2.  Create a new output sequence of the same length (12), initially filled with zeros.
    3.  Calculate the new starting position for the block by subtracting 4 from its original starting position in the input.
    4.  Place the identified block of non-zero digits into the output sequence, starting at the calculated new position. Ensure the block maintains its original length and digit value.
```python
import math

def find_object(sequence):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (value, start_index, length) if an object is found,
        otherwise (None, -1, 0).
    """
    start_index = -1
    value = None
    length = 0

    for i, digit in enumerate(sequence):
        if start_index == -1:
            # Look for the start of a block
            if digit != 0:
                start_index = i
                value = digit
                length = 1
        else:
            # We are inside a potential block
            if digit == value:
                length += 1
            else:
                # Block ended
                return value, start_index, length

    # Check if the block ended exactly at the end of the sequence
    if start_index != -1:
        return value, start_index, length

    # No non-zero block found
    return None, -1, 0

def transform(input_str):
    """
    Identifies a contiguous block of identical non-zero numbers in the input sequence,
    shifts this block 4 positions to the left, placing it into an output sequence
    of the same length (12) initialized with zeros. Positions vacated by the shift
    or outside the shifted block are filled with zeros.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list) # Should always be 12 based on examples

    # Initialize the output grid (list) with zeros
    output_list = [0] * n

    # Find the contiguous block of non-zero numbers
    value, start_index, length = find_object(input_list)

    # If an object was found, place it in the shifted position
    if value is not None:
        # Calculate the new starting position (shift left by 4)
        new_start_index = start_index - 4

        # Place the object into the output list at the new position
        for i in range(length):
            target_index = new_start_index + i
            # Ensure the target index is within the bounds of the list
            if 0 <= target_index < n:
                output_list[target_index] = value

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str

```
```python
"""
Identifies a single contiguous block of identical non-zero digits within an input sequence of 12 integers. Shifts this block 4 positions to the left, placing it into an output sequence of the same length (12) initialized with zeros. Positions outside the shifted block remain zero. Elements are only placed within the valid bounds (0-11) of the output sequence.
"""

import math # Although not strictly needed for this version, good practice
# import numpy as np # Could be used if input_grid is specifically a numpy array

def find_object(sequence):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        sequence: A list or array of integers.

    Returns:
        A tuple (value, start_index, length) if an object is found,
        otherwise (None, -1, 0).
    """
    start_index = -1
    value = None
    length = 0

    for i, digit in enumerate(sequence):
        if start_index == -1:
            # Look for the start of a potential block
            if digit != 0:
                start_index = i
                value = digit
                length = 1
        else:
            # We are inside a potential block
            if digit == value:
                # Continue the block
                length += 1
            else:
                # Block ended before the end of the sequence
                return value, start_index, length

    # Check if the block ended exactly at the end of the sequence
    if start_index != -1:
        return value, start_index, length

    # No non-zero block found or sequence was empty/all zeros
    return None, -1, 0

def transform(input_grid):
    """
    Transforms the input sequence by shifting the non-zero block left by 4 positions.

    Args:
        input_grid: A list or array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Ensure input is treated as a list (handles numpy arrays too)
    input_list = list(input_grid)
    n = len(input_list)

    # Initialize the output grid (list) with zeros
    output_grid = [0] * n

    # 1. Identify the contiguous block of identical non-zero numbers
    value, start_index, length = find_object(input_list)

    # 2. If an object was found, proceed with transformation
    if value is not None:
        # 3. Calculate the new starting position (shift left by 4)
        new_start_index = start_index - 4

        # 4. Place the object into the output list at the new position
        # Iterate through the length of the identified block
        for i in range(length):
            # Calculate the target index in the output grid for the current element of the block
            target_index = new_start_index + i

            # 5. Ensure the target index is within the valid bounds of the output grid (0 to n-1)
            if 0 <= target_index < n:
                # Place the block's value at the valid target index
                output_grid[target_index] = value

    # Return the transformed grid
    return output_grid
```
