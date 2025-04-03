
## train_1

**input:**
```
0 0 6 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 6 6 6 6 6 6 6 6 0 0
```


**output:**
```
0 0 0 0 6 6 6 6 6 6 6 6
```


## train_3

**input:**
```
0 0 0 0 0 0 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 7 7 0 0
```


## train_4

**input:**
```
0 8 8 8 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 8 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 0
```


## train_6

**input:**
```
0 0 0 9 9 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 9 9 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 7 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 0 0 0 0 0 0
```

**Perception of Task Elements:**

The task involves transforming a one-dimensional sequence of integers. Each input sequence contains mostly zeros and a single contiguous block of a non-zero digit (e.g., 6, 7, 8, 9). The length of this non-zero block varies. The transformation consistently moves this block of non-zero digits to the right within the sequence. The specific non-zero digit itself doesn't seem to affect the transformation logic, only its position and extent. The background remains zeros. The amount of shift appears constant across all examples.

**YAML Facts:**


```yaml
task_description: Shifting a block of non-zero digits within a 1D sequence.
elements:
  - object: sequence
    properties:
      - type: 1D list of integers
      - contains: elements
      - length: fixed (appears to be 12 in examples)
  - object: element
    properties:
      - type: integer
      - value: 0 or a single non-zero digit (e.g., 6, 7, 8, 9)
      - position: index within the sequence
  - object: block
    properties:
      - type: contiguous sub-sequence
      - elements: all elements have the same non-zero value
      - location: defined by start_index and end_index
      - value: the specific non-zero digit comprising the block
actions:
  - action: identify_non_zero_block
    actor: system
    input: input_sequence
    output: block_properties (value, start_index, end_index)
    description: Finds the contiguous segment of non-zero identical digits.
  - action: shift_block
    actor: system
    input: block_properties
    parameters:
      - shift_amount: 2 positions
      - direction: right
    output: new_block_start_index
    description: Calculates the new starting position for the block by adding the shift amount to the original start index.
  - action: generate_output
    actor: system
    input:
      - input_sequence_length
      - original_block_properties
      - new_block_start_index
    output: output_sequence
    description: Creates a new sequence of the same length, initially filled with zeros, then places the identified block at the calculated new position.
relationships:
  - type: transformation
    from: input_sequence
    to: output_sequence
    rule: The single contiguous block of non-zero digits in the input sequence is shifted exactly two positions to the right to produce the output sequence. The positions originally occupied by the block become zeros, unless overwritten by the shifted block itself.
```


**Natural Language Program:**

1.  Initialize an output sequence with the same length as the input sequence, filled entirely with zeros.
2.  Scan the input sequence to find the first occurrence of a non-zero digit. Record its value and its starting index.
3.  Continue scanning from the starting index to find the end of the contiguous block of this non-zero digit. Record the ending index.
4.  Calculate the new starting index for the block by adding 2 to the original starting index found in step 2.
5.  Calculate the new ending index by adding 2 to the original ending index found in step 3.
6.  Iterate from the new starting index to the new ending index (inclusive). For each position in this range within the output sequence, set its value to the non-zero digit value recorded in step 2.
```python
import numpy as np

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of a non-zero digit in the sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (block_value, start_index, end_index) if a block is found,
        otherwise (None, -1, -1).
    """
    start_index = -1
    end_index = -1
    block_value = None

    for i, val in enumerate(sequence):
        if val != 0:
            if start_index == -1:
                # Found the start of the block
                start_index = i
                block_value = val
                end_index = i # Initialize end_index here
            elif val == block_value:
                 # Continue the block
                end_index = i
            else:
                # Found a different non-zero value, stop (assuming only one block type)
                 # or handle multiple blocks if necessary, but examples suggest one block
                 # For this task, we assume the block ends when value changes or hits zero
                break
        elif start_index != -1:
            # Found a zero after the block started, the block has ended
            break

    # Handle case where block goes to the very end
    if start_index != -1 and end_index == -1:
        end_index = start_index # If only one element in block

    return block_value, start_index, end_index


def transform(input_sequence_str):
    """
    Shifts the single contiguous block of non-zero digits in the input sequence 
    exactly two positions to the right. The positions originally occupied by 
    the block become zeros, unless overwritten by the shifted block itself.
    """
    # Parse the input string into a list of integers
    input_sequence = [int(x) for x in input_sequence_str.split()]
    n = len(input_sequence)

    # Initialize output_sequence with zeros
    output_sequence = [0] * n

    # Find the non-zero block in the input sequence
    block_value, start_index, end_index = find_non_zero_block(input_sequence)

    # If a block was found, shift it
    if block_value is not None:
        # Calculate the new starting position for the block
        new_start_index = start_index + 2
        block_length = end_index - start_index + 1

        # Place the block in the output sequence at the new position
        # Ensure we don't write past the end of the sequence (though examples suggest this won't happen)
        for i in range(block_length):
            new_index = new_start_index + i
            if 0 <= new_index < n:
                output_sequence[new_index] = block_value

    # Convert the output list back to a space-separated string
    output_sequence_str = " ".join(map(str, output_sequence))
    return output_sequence_str

```
```python
import numpy as np # Import numpy although not strictly required by the core logic, it handles potential array inputs gracefully.

"""
Shifts the single contiguous block of identical non-zero digits 
found in the input sequence exactly two positions to the right. 
Positions originally occupied by the block become zeros unless 
overwritten by the shifted block. Returns the transformed 
sequence as a space-separated string.
"""

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of a non-zero digit in the sequence.

    Args:
        sequence: A list or array of integers.

    Returns:
        A tuple (block_value, start_index, end_index) if a block is found,
        otherwise (None, -1, -1). Returns -1 for indices if no block is found.
    """
    start_index = -1
    end_index = -1
    block_value = None

    # Iterate through the sequence to find the start of the block
    for i, val in enumerate(sequence):
        if val != 0:
            start_index = i
            block_value = val
            break # Found the start, break the loop

    # If a starting non-zero value was found, find the end of the block
    if start_index != -1:
        end_index = start_index # Initialize end_index
        # Continue from the element *after* the start index
        for i in range(start_index + 1, len(sequence)):
            if sequence[i] == block_value:
                end_index = i # Extend the block
            else:
                break # Block ended (different value or zero)
                
    return block_value, start_index, end_index


def transform(input_sequence):
    """
    Applies the block shifting transformation.

    Args:
        input_sequence: A list or numpy array of integers representing the input.

    Returns:
        A string representing the transformed sequence with elements separated by spaces.
    """
    # Determine the length of the input sequence
    n = len(input_sequence)

    # Initialize output_sequence with zeros of the same length
    output_sequence = [0] * n

    # Find the non-zero block in the input sequence
    block_value, start_index, end_index = find_non_zero_block(input_sequence)

    # If a block was found, proceed to shift it
    if block_value is not None and start_index != -1:
        # Calculate the new starting position for the block (shift right by 2)
        new_start_index = start_index + 2
        
        # Calculate the length of the block
        block_length = end_index - start_index + 1

        # Place the block in the output sequence at the new position
        # Iterate for the length of the block
        for i in range(block_length):
            # Calculate the target index in the output sequence
            new_index = new_start_index + i
            # Check bounds: Ensure the new index is within the sequence limits
            if 0 <= new_index < n:
                # Assign the block's value to the output sequence at the new index
                output_sequence[new_index] = block_value

    # Convert the output list of integers to a space-separated string
    output_sequence_str = " ".join(map(str, output_sequence))
    
    # Return the final string representation
    return output_sequence_str
```
