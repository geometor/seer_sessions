
## train_1

**input:**
```
0 0 0 0 0 0 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 3 0
```


## train_2

**input:**
```
0 0 0 0 7 7 7 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 7 7 7 0
```


## train_3

**input:**
```
8 8 8 8 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 8 8 8 8 8 0 0 0
```


## train_4

**input:**
```
0 0 3 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 3 0 0 0 0
```


## train_5

**input:**
```
0 0 0 8 8 8 8 8 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 8 8 8 8 8
```


## train_6

**input:**
```
6 6 6 6 6 6 6 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 6 6 6 6 6 6 0
```


## train_7

**input:**
```
0 8 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 8 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences (lists) of integers.
    *   Each sequence has a fixed length (12 in all examples).
    *   The sequences primarily contain zeros.
    *   Each input sequence contains exactly one contiguous block of identical non-zero integers (this block can be of length 1).
    *   The output sequence is derived from the input by moving this non-zero block.
    *   The movement is a shift to the right by a fixed number of positions.
    *   The positions previously occupied by the non-zero block become zeros in the output.
    *   The amount of the rightward shift appears to be constant across all examples (+4 positions).

*   **YAML Documentation of Facts:**
    
```yaml
    task_description: Shift a block of non-zero numbers within a sequence.
    elements:
      - object: sequence
        description: A list of integers representing the input and output data.
        properties:
          - length: Fixed (e.g., 12 in the examples)
          - content: Primarily zeros with one contiguous block of identical non-zero integers.
      - object: non_zero_block
        description: A contiguous sub-sequence of identical non-zero integers within the input sequence.
        properties:
          - value: The non-zero integer value.
          - start_index: The starting position (0-based) of the block in the input sequence.
          - end_index: The ending position (0-based) of the block in the input sequence.
          - length: The number of elements in the block.
      - object: zero
        description: The background element (integer 0).
    action:
      - name: shift_block_right
        description: Moves the non_zero_block to a new position in the sequence.
        parameters:
          - shift_amount: The number of positions to shift right (seems fixed at 4).
    relationships:
      - The output sequence is generated from the input sequence by applying the shift_block_right action.
      - The position of the non_zero_block in the output is determined by its start_index in the input plus the shift_amount.
      - The elements in the output sequence at the original position of the non_zero_block are replaced with zeros.
      - The length and the non-zero value of the block remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of the same length as the input sequence, filled entirely with zeros.
    2.  Scan the input sequence to identify the contiguous block of identical non-zero numbers. Determine its value, its starting index, and its ending index.
    3.  Calculate the new starting index for the block in the output sequence by adding 4 to the original starting index found in step 2.
    4.  Copy the identified non-zero block (using its value and length) into the output sequence, starting at the calculated new starting index.
    5.  Return the modified output sequence.
```python
"""
Transforms an input sequence by finding a contiguous block of identical non-zero integers and shifting it 4 positions to the right, filling the original positions with zeros.
"""

import numpy as np

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers.

    Args:
        sequence: A list or numpy array of numbers.

    Returns:
        A tuple (value, start_index, end_index) or None if no block is found.
        value: The non-zero integer value of the block.
        start_index: The starting index of the block.
        end_index: The ending index (inclusive) of the block.
    """
    start_index = -1
    block_value = 0
    for i, val in enumerate(sequence):
        if val != 0:
            if start_index == -1: # Start of a potential block
                start_index = i
                block_value = val
            elif val != block_value: # End of block because value changed
                 return block_value, start_index, i - 1
        elif start_index != -1: # End of block because zero encountered
            return block_value, start_index, i - 1

    # Handle block reaching the end of the sequence
    if start_index != -1:
        return block_value, start_index, len(sequence) - 1

    return None # No non-zero block found

def transform(input_sequence):
    """
    Shifts a contiguous block of non-zero numbers 4 positions to the right.

    Args:
        input_sequence: A list of integers representing the input.

    Returns:
        A list of integers representing the transformed output.
    """
    # Convert to numpy array for easier slicing if needed, though list operations are fine here
    input_arr = np.array(input_sequence)
    n = len(input_arr)
    
    # Initialize output_grid with zeros, same size as input
    output_sequence = [0] * n

    # Find the contiguous block of identical non-zero numbers
    block_info = find_non_zero_block(input_arr)

    if block_info:
        value, start_index, end_index = block_info
        block_length = end_index - start_index + 1
        
        # Calculate the new starting index for the block (shift right by 4)
        new_start_index = start_index + 4
        
        # Ensure the new block stays within bounds
        # (although based on examples, overflow doesn't seem to wrap around, just potentially cut off or error if not handled)
        # We will place it assuming it fits, as per examples.
        
        # Place the block into the output sequence at the new position
        for i in range(block_length):
            output_index = new_start_index + i
            # Check bounds before writing (optional based on exact task rules for overflow)
            if 0 <= output_index < n:
                output_sequence[output_index] = value
            # else: handle overflow if required, e.g., wrap around or discard

    # Return the modified output sequence (as a list)
    return output_sequence
```
