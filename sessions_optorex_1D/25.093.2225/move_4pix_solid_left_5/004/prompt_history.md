
## train_1

**input:**
```
0 0 0 0 7 7 0 0 0 0 0 0
```


**output:**
```
7 7 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 9 9 9 9 9 9 0
```


**output:**
```
0 9 9 9 9 9 9 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 2 2 0 0 0 0 0 0
```


**output:**
```
2 2 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 7 7 7 7 7 7 7
```


**output:**
```
0 7 7 7 7 7 7 7 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 9 0
```


**output:**
```
0 0 0 0 0 0 9 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 0 7 7
```


**output:**
```
0 0 0 0 0 0 7 7 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 4 0 0 0
```


**output:**
```
0 0 0 0 4 0 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are lists (or sequences) of single-digit integers.
    *   The length of the input and output sequences appears to be constant (12 elements in all examples).
    *   Each input sequence contains a single contiguous block of identical non-zero digits, surrounded by zeros.
    *   The output sequence is formed by shifting this non-zero block to the left by a fixed amount.
    *   The rest of the positions in the output sequence are filled with zeros.
    *   The non-zero digits observed are 2, 4, 7, and 9.
    *   The amount of the left shift appears to be consistently 4 positions.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - type: sequence
        role: input
        properties:
          - data_type: integer
          - element_range: 0-9
          - length: 12
          - structure: contains a single contiguous block of identical non-zero digits surrounded by zeros.
      - type: sequence
        role: output
        properties:
          - data_type: integer
          - element_range: 0-9
          - length: 12
          - structure: derived from input by shifting the non-zero block.
    transformation:
      action: identify_block
      input: input sequence
      target: contiguous block of identical non-zero digits
      parameters:
        - block_value: the non-zero digit
        - start_index: index of the first element of the block
        - end_index: index of the last element of the block
        - length: number of elements in the block
    transformation:
      action: shift_block_left
      input: identified block
      parameters:
        - shift_amount: 4 positions
      output: modified sequence
      details:
        - Create a new sequence of the same length as the input, initialized with zeros.
        - Calculate the new start index for the block: `new_start_index = start_index - 4`.
        - Place the identified block into the new sequence starting at `new_start_index`.
    relationships:
      - The output sequence is a direct transformation of the input sequence.
      - The non-zero block maintains its elements and order but changes its position.
      - The shift amount (4) is constant across all examples.
      - Zeros act as background/padding.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 integers.
    2.  Initialize an output sequence of 12 zeros.
    3.  Iterate through the input sequence to find the first non-zero integer. Record its value (`block_value`) and its index (`start_index`).
    4.  Continue iterating from `start_index` to find the end of the contiguous block of integers equal to `block_value`. Record the index of the last element of the block (`end_index`).
    5.  Calculate the length of the block: `length = end_index - start_index + 1`.
    6.  Calculate the target starting index for the block in the output sequence: `new_start_index = start_index - 4`.
    7.  Copy the identified block (from `start_index` to `end_index` in the input) into the output sequence, starting at `new_start_index` and extending for `length` positions.
    8.  Return the resulting output sequence.
```python
import math
import collections

"""
Transforms an input sequence by identifying a single contiguous block of identical 
non-zero digits and shifting this block 4 positions to the left. The remaining 
positions in the output sequence are filled with zeros.
"""

def find_non_zero_block(sequence):
    """
    Finds the start index, end index, and value of the contiguous non-zero block.
    Returns (None, None, None) if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    block_value = 0

    # Find the start of the block
    for i, val in enumerate(sequence):
        if val != 0:
            start_index = i
            block_value = val
            break
    
    # If no non-zero value found, return None
    if start_index == -1:
        return None, None, None

    # Find the end of the block (where the value changes or sequence ends)
    end_index = start_index
    for i in range(start_index + 1, len(sequence)):
        if sequence[i] == block_value:
            end_index = i
        else:
            break # End of the block

    return start_index, end_index, block_value

def transform(input_sequence):
    """
    Identifies a contiguous block of non-zero identical digits in the input 
    sequence and shifts it 4 positions to the left in the output sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    
    # Initialize output_sequence with zeros, same length as input
    sequence_length = len(input_sequence)
    output_sequence = [0] * sequence_length

    # 1. Find the non-zero block in the input sequence
    start_index, end_index, block_value = find_non_zero_block(input_sequence)

    # Check if a block was found
    if start_index is None:
        # If no block found (e.g., all zeros), return the initialized zero sequence
        return output_sequence 

    # 2. Calculate the length of the block
    block_length = end_index - start_index + 1
    
    # 3. Calculate the new starting index for the block in the output sequence
    #    The shift is 4 positions to the left.
    new_start_index = start_index - 4

    # 4. Copy the identified block to the output sequence at the new position
    #    Ensure indices stay within the bounds of the output sequence.
    for i in range(block_length):
        input_idx = start_index + i
        output_idx = new_start_index + i
        
        # Place the value if the output index is valid
        if 0 <= output_idx < sequence_length:
            output_sequence[output_idx] = input_sequence[input_idx] # or just block_value

    # 5. Return the resulting output sequence
    return output_sequence

```
```python
import math
import collections
import numpy as np # Although not strictly necessary for the core logic, useful for potential array operations or if input is numpy array

"""
Transforms an input sequence of 12 integers by identifying a single contiguous 
block of identical non-zero digits and shifting this block exactly 4 positions 
to the left. Positions outside the shifted block in the output sequence are 
filled with zeros.
"""

def find_non_zero_block(sequence):
    """
    Finds the start index, end index, and value of the single contiguous 
    non-zero block in a sequence. Assumes exactly one such block exists.

    Args:
        sequence: A list or tuple of numbers.

    Returns:
        A tuple (start_index, end_index, block_value). 
        Returns (None, None, None) if no non-zero element is found.
    """
    start_index = -1
    end_index = -1
    block_value = 0

    # Iterate to find the first non-zero element (start of the block)
    for i, val in enumerate(sequence):
        if val != 0:
            start_index = i
            block_value = val
            break
    
    # If no non-zero value was found, return None tuple
    if start_index == -1:
        return None, None, None

    # Iterate from the start index to find the end of the block
    end_index = start_index
    # Check elements after the start_index up to the end of the sequence
    for i in range(start_index + 1, len(sequence)):
        if sequence[i] == block_value:
            end_index = i # Extend the block
        else:
            break # Block ends here

    return start_index, end_index, block_value

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of 12 integers containing one contiguous block
                       of identical non-zero digits.

    Returns:
        A new list of 12 integers representing the transformed sequence.
    """
    
    # Define constants based on the problem description
    sequence_length = 12
    shift_amount = 4 

    # 1. Initialize the output sequence with zeros
    output_sequence = [0] * sequence_length

    # 2. Find the non-zero block in the input sequence
    start_index, end_index, block_value = find_non_zero_block(input_sequence)

    # 3. Check if a block was found (handle edge case, though examples guarantee a block)
    if start_index is None:
        return output_sequence # Return the sequence of zeros if no block found

    # 4. Calculate the length of the block
    block_length = end_index - start_index + 1
    
    # 5. Calculate the target starting index for the block in the output sequence
    #    Shift is 4 positions to the LEFT, so subtract the shift amount.
    new_start_index = start_index - shift_amount

    # 6. Copy the block value into the output sequence at the new position
    #    Iterate for the length of the block
    for i in range(block_length):
        # Calculate the index in the output sequence where the current element of the block should go
        output_idx = new_start_index + i
        
        # Check if the calculated output index is within the valid bounds (0 to sequence_length-1)
        if 0 <= output_idx < sequence_length:
            # Place the block's value at the valid position in the output sequence
            output_sequence[output_idx] = block_value

    # 7. Return the completed output sequence
    return output_sequence
```
