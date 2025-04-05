
## train_1

**input:**
```
0 0 0 0 0 0 7 7 7 7 7 0
```


**output:**
```
0 0 0 0 0 0 7 0 0 0 7 0
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 0 0 0 0
```


**output:**
```
8 0 0 0 0 0 0 8 0 0 0 0
```


## train_3

**input:**
```
0 0 0 9 9 9 9 9 0 0 0 0
```


**output:**
```
0 0 0 9 0 0 0 9 0 0 0 0
```


## train_4

**input:**
```
8 8 8 8 0 0 0 0 0 0 0 0
```


**output:**
```
8 0 0 8 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
5 5 5 5 5 5 5 5 5 5 5 0
```


**output:**
```
5 0 0 0 0 0 0 0 0 0 5 0
```


## train_6

**input:**
```
0 0 0 0 5 5 5 5 5 0 0 0
```


**output:**
```
0 0 0 0 5 0 0 0 5 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 3 3 3 3 3 0 0
```


**output:**
```
0 0 0 0 0 3 0 0 0 3 0 0
```

## Perception of Elements

The task involves transforming a sequence of single digits based on contiguous blocks of identical non-zero digits.
- **Input:** A sequence of single-digit integers.
- **Output:** A sequence of single-digit integers of the same length as the input.
- **Key Elements:** Contiguous blocks (runs) of identical non-zero digits within the input sequence. Zeros act as delimiters or background elements.
- **Transformation:** The core transformation operates on these non-zero blocks. Within each block, only the first and the last digit are preserved in the output. All the digits *between* the first and the last digit of the block are replaced with '0'. Digits that are initially '0' remain '0'. Blocks of length 1 or 2 remain unchanged as there are no elements strictly *between* the first and last.

## YAML Facts


```yaml
objects:
  - name: sequence
    type: list_of_integers
    description: Represents both the input and output data structures.
  - name: block
    type: contiguous_subsequence
    description: A run of identical non-zero digits within the input sequence.
    properties:
      - value: integer (non-zero)
      - start_index: integer
      - end_index: integer
      - length: integer (>= 1)
  - name: digit
    type: integer
    description: Individual element within a sequence. Can be 0-9.

properties:
  - object: sequence
    name: length
    type: integer
  - object: sequence
    name: elements
    type: list_of_digits

actions:
  - name: identify_blocks
    description: Scan the input sequence to find all contiguous blocks of identical non-zero digits.
    inputs:
      - input_sequence: sequence
    outputs:
      - list_of_blocks: list[block]
  - name: modify_sequence
    description: Create the output sequence by applying transformations based on identified blocks.
    inputs:
      - input_sequence: sequence
      - identified_blocks: list[block]
    outputs:
      - output_sequence: sequence

relationships:
  - type: preservation
    description: Input digits that are '0' remain '0' in the output at the same position.
  - type: boundary_preservation
    description: For each identified non-zero block, the digit at the start_index and the digit at the end_index in the input sequence are preserved in the output sequence at the same indices.
  - type: zero_replacement
    description: For each identified non-zero block with length > 2, all digits in the input sequence at indices strictly between start_index and end_index are replaced with '0' in the output sequence.
  - type: length_conservation
    description: The output sequence has the same length as the input sequence.

```


## Natural Language Program

1.  **Initialize** the output sequence as a direct copy of the input sequence.
2.  **Iterate** through the input sequence from left to right to identify contiguous blocks of identical non-zero digits. Keep track of the start index, end index, and the value of each block found.
3.  **For each identified block** where the length (end index - start index + 1) is greater than 2:
    a.  Iterate through the indices starting from `start_index + 1` up to, but not including, `end_index`.
    b.  For each of these intermediate indices, set the value in the **output sequence** at that index to `0`.
4.  **Return** the modified output sequence.
```python
import math
import collections

"""
Transforms a sequence of single-digit integers based on contiguous blocks of identical non-zero digits.

1.  Initialize the output sequence as a direct copy of the input sequence.
2.  Iterate through the input sequence from left to right to identify contiguous blocks (runs) of identical non-zero digits.
3.  For each identified block where the length is greater than 2:
    a.  Iterate through the indices strictly *between* the start and end indices of the block.
    b.  Set the value in the output sequence at these intermediate indices to 0.
4.  Digits that are initially '0' remain '0'. Blocks of length 1 or 2 remain unchanged.
5.  Return the modified output sequence.
"""

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """
    n = len(input_sequence)
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence)

    i = 0
    while i < n:
        # Skip over zeros
        if input_sequence[i] == 0:
            i += 1
            continue

        # Found a non-zero digit, potential start of a block
        start_index = i
        block_value = input_sequence[i]
        end_index = i

        # Find the end of the contiguous block of the same non-zero digit
        j = i + 1
        while j < n and input_sequence[j] == block_value:
            end_index = j
            j += 1

        # Calculate the length of the identified block
        block_length = end_index - start_index + 1

        # If the block length is greater than 2, zero out the middle elements
        if block_length > 2:
            # Iterate through the indices strictly between start_index and end_index
            for k in range(start_index + 1, end_index):
                output_sequence[k] = 0

        # Move the main iterator past the processed block
        i = end_index + 1

    return output_sequence

```
