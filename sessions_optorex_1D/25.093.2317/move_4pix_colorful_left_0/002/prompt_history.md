
## train_1

**input:**
```
0 0 0 0 9 3 2 5 0 0 0 0
```


**output:**
```
9 3 2 5 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 6 8 3 4 9 8 0
```


**output:**
```
0 6 8 3 4 9 8 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 4 6 3 4 0 0
```


**output:**
```
0 0 4 6 3 4 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 8 1 7 0 0 0
```


**output:**
```
0 0 8 1 7 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 3 4 2 1 2 7 1
```


**output:**
```
0 3 4 2 1 2 7 1 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 0 8 1
```


**output:**
```
0 0 0 0 0 0 8 1 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 2 8 7 0 0 0 0
```


**output:**
```
0 2 8 7 0 0 0 0 0 0 0 0
```

*   **Perception of the elements:**
    *   The input and output are sequences of single-digit integers, separated by spaces.
    *   Each sequence has a fixed length (12 digits in the examples).
    *   The sequences contain both zero and non-zero digits.
    *   The core transformation involves repositioning a contiguous block of digits within the sequence.
    *   This block is defined by the first and last non-zero digits in the input sequence, including any zeros that fall between them.
    *   The block of digits is shifted to the left by a fixed amount.
    *   The positions outside the shifted block in the output are filled with zeros.

*   **Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          - type: list of integers
          - length: 12 (based on examples)
          - elements: single digits (0-9)
      - object: digit_block
        properties:
          - content: contiguous subsequence from the input sequence
          - definition: starts at the index of the first non-zero digit, ends at the index of the last non-zero digit
          - includes: all digits (zero and non-zero) within its start and end indices
      - object: index
        properties:
          - type: integer
          - role: indicates position within the sequence (0-based)
    relationships:
      - type: identification
        description: Identify the first non-zero digit and its index (input_start_index).
      - type: identification
        description: Identify the last non-zero digit and its index (input_end_index).
      - type: extraction
        description: Extract the digit_block from input_start_index to input_end_index.
      - type: calculation
        description: Calculate the target start index for the block in the output sequence (output_start_index).
        formula: output_start_index = input_start_index - 4
      - type: construction
        description: Create the output sequence.
        steps:
          - Initialize an output sequence of the same length as the input, filled with zeros.
          - Place the extracted digit_block into the output sequence starting at the calculated output_start_index.
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of digits.
    2.  Find the index of the first non-zero digit in the input sequence (let this be `first_nz_idx`). If no non-zero digit exists, the output is the same as the input (or a sequence of all zeros, depending on interpretation - examples suggest a block always exists).
    3.  Find the index of the last non-zero digit in the input sequence (let this be `last_nz_idx`).
    4.  Extract the contiguous sub-sequence (the "block") from the input sequence starting at `first_nz_idx` and ending at `last_nz_idx` (inclusive).
    5.  Calculate the target starting index for this block in the output sequence by subtracting 4 from `first_nz_idx` (let this be `output_start_idx`).
    6.  Create a new sequence of the same length as the input, initially filled entirely with zeros.
    7.  Place the extracted block into this new sequence, starting at `output_start_idx`.
    8.  The resulting sequence is the output.
```python
import numpy as np
import math

"""
Transforms an input sequence of digits by identifying the contiguous block 
between the first and last non-zero digits, and shifting this block 4 positions 
to the left within a sequence of the same length, padding with zeros.
"""

def find_first_nonzero_index(data):
    """Finds the index of the first non-zero element in a list."""
    for i, x in enumerate(data):
        if x != 0:
            return i
    return None  # Return None if no non-zero element is found

def find_last_nonzero_index(data):
    """Finds the index of the last non-zero element in a list."""
    for i in range(len(data) - 1, -1, -1):
        if data[i] != 0:
            return i
    return None # Return None if no non-zero element is found

def transform(input_str):
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string of space-separated single digits.

    Returns:
        A string of space-separated single digits representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_sequence = [int(d) for d in input_str.split()]
    n = len(input_sequence)

    # Initialize the output sequence with zeros
    output_sequence = [0] * n

    # Find the indices of the first and last non-zero digits
    first_nz_idx = find_first_nonzero_index(input_sequence)
    last_nz_idx = find_last_nonzero_index(input_sequence)

    # If no non-zero digits are found, return the sequence of zeros
    if first_nz_idx is None:
        return " ".join(map(str, output_sequence))

    # Extract the contiguous block including zeros between the first and last non-zero digits
    digit_block = input_sequence[first_nz_idx : last_nz_idx + 1]

    # Calculate the target starting index for the block in the output
    # Shift is 4 positions to the left
    output_start_idx = first_nz_idx - 4

    # Ensure the start index is not negative (although examples suggest it won't be)
    # It seems the minimum first_nz_idx allowing a valid shift is 4 (e.g., train_1)
    # If first_nz_idx were less than 4, the logic might need adjustment,
    # but based on examples, we assume first_nz_idx >= 4 if non-zeros exist.
    # Or more accurately, the calculation output_start_idx >= 0 holds for the examples.
    output_start_idx = max(0, output_start_idx) # safeguard, though likely not needed for provided examples

    # Calculate the end index for placing the block in the output
    output_end_idx = output_start_idx + len(digit_block)

    # Place the extracted block into the output sequence
    # Ensure the block fits within the output sequence bounds
    if output_start_idx < n and output_end_idx <= n:
        output_sequence[output_start_idx:output_end_idx] = digit_block
    # Handle cases where the block might theoretically go out of bounds (if input rules change)
    elif output_start_idx < n:
         # Place as much of the block as fits
         length_to_copy = n - output_start_idx
         output_sequence[output_start_idx:] = digit_block[:length_to_copy]


    # Format the output sequence back into a space-separated string
    output_str = " ".join(map(str, output_sequence))

    return output_str
```
