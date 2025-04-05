
## train_1

**input:**
```
0 0 0 0 0 1 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 0 0 0 0
```


## train_3

**input:**
```
0 0 0 6 2 7 1 5 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 6 2 7 1 5 4
```


## train_4

**input:**
```
0 0 0 0 6 5 7 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 5 7 2 0
```


## train_5

**input:**
```
0 4 2 6 9 3 6 7 1 0 0 0
```


**output:**
```
0 0 0 0 4 2 6 9 3 6 7 1
```


## train_6

**input:**
```
0 0 0 0 0 0 9 7 6 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 9 7 6
```


## train_7

**input:**
```
0 0 0 0 0 3 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 1 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences (lists or arrays) of integers.
    *   All sequences appear to have a fixed length (12 in the examples).
    *   The core operation involves locating a contiguous block of non-zero numbers within the input sequence.
    *   This block of non-zero numbers is then shifted exactly 3 positions to the right in the output sequence.
    *   The positions vacated by the shift and the positions before the original block (if any) are filled with zeros.
    *   The positions after the shifted block are also filled with zeros up to the fixed length of the sequence.
    *   If the input contains only zeros, the output remains all zeros (implied, though no example shows this).

*   **Facts:**
    
```yaml
    objects:
      - name: input_sequence
        type: list of integers
        properties:
          - length: 12
          - contains: a contiguous block of non-zero integers surrounded by zeros
      - name: output_sequence
        type: list of integers
        properties:
          - length: 12
          - contains: the same contiguous block of non-zero integers as the input, shifted
      - name: non_zero_block
        type: sub-sequence of integers
        properties:
          - extracted from: input_sequence
          - contains only: integers > 0
          - contiguous: yes
      - name: shift_amount
        type: integer
        value: 3
        description: The fixed number of positions the non_zero_block is moved to the right.
    actions:
      - name: locate_block
        actor: system
        input: input_sequence
        output: start_index, end_index, non_zero_block
        description: Finds the start and end indices of the contiguous non-zero block and extracts it.
      - name: calculate_new_position
        actor: system
        input: start_index, shift_amount
        output: new_start_index
        description: Calculates the starting position for the block in the output sequence.
      - name: construct_output
        actor: system
        input: non_zero_block, new_start_index, sequence_length
        output: output_sequence
        description: Creates a new sequence of the target length, places the non_zero_block at the new_start_index, and pads the rest with zeros.
    relationships:
      - The output_sequence is a transformation of the input_sequence.
      - The non_zero_block in the output_sequence starts at an index exactly 3 positions greater than its starting index in the input_sequence.
      - The relative order and values of the numbers within the non_zero_block remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous subsequence of non-zero numbers within the input sequence. Determine its starting and ending indices.
    2.  If no non-zero numbers are found, return the input sequence as is.
    3.  Create a new sequence of the same length as the input, initialized entirely with zeros.
    4.  Calculate the new starting index for the non-zero subsequence by adding 3 to its original starting index.
    5.  Copy the identified non-zero subsequence into the new sequence, beginning at the calculated new starting index.
    6.  Return the newly constructed sequence.
```python
import math  # Although not strictly needed for this logic, good practice to include common libs

"""
Transforms an input sequence of integers by identifying a contiguous block of non-zero numbers 
and shifting this block exactly 3 positions to the right within a sequence of the same fixed length, 
padding the remaining positions with zeros.
"""

def find_non_zero_block(sequence):
    """
    Finds the start index, end index (exclusive), and the block of contiguous non-zero numbers.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (start_index, end_index, block) if a block is found, otherwise None.
    """
    start_index = -1
    end_index = -1
    for i, val in enumerate(sequence):
        if val != 0:
            if start_index == -1:
                start_index = i
            end_index = i + 1 # Keep track of the position *after* the last non-zero
        elif start_index != -1:
            # We found a zero *after* finding non-zeros, the block has ended
            break 
            # If the non-zero block goes to the very end, the loop finishes naturally

    if start_index != -1:
        block = sequence[start_index:end_index]
        return start_index, end_index, block
    else:
        # No non-zero numbers found
        return None


def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # Define sequence length and shift amount
    sequence_length = len(input_sequence)
    shift_amount = 3

    # Initialize the output sequence with zeros
    output_sequence = [0] * sequence_length

    # Find the contiguous block of non-zero numbers in the input
    block_info = find_non_zero_block(input_sequence)

    # If a non-zero block was found
    if block_info:
        start_index, end_index, non_zero_block = block_info
        
        # Calculate the new starting position for the block
        new_start_index = start_index + shift_amount
        
        # Calculate the new ending position (exclusive)
        # Ensure the block fits within the sequence length (optional based on problem constraints, but safer)
        new_end_index = new_start_index + len(non_zero_block)
        
        # Place the non_zero_block into the output sequence at the new position
        # Check boundaries to prevent errors if the shifted block would exceed the length
        if new_start_index < sequence_length:
             # Determine how much of the block actually fits
            effective_block_length = min(len(non_zero_block), sequence_length - new_start_index)
            output_sequence[new_start_index : new_start_index + effective_block_length] = non_zero_block[:effective_block_length]
            
    # If no non-zero block was found, the output sequence remains all zeros, which is already initialized.
    
    return output_sequence

```
