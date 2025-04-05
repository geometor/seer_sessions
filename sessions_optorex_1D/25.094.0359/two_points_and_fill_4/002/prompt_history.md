
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 8 0 8
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 8
```


## train_2

**input:**
```
0 0 0 8 0 0 0 0 0 0 8 0
```


**output:**
```
0 0 0 8 8 8 8 8 8 8 8 0
```


## train_3

**input:**
```
0 0 0 0 0 8 0 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 0 0
```


## train_4

**input:**
```
8 0 0 0 0 0 0 0 0 0 0 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8
```


## train_5

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 8
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 8 8
```


## train_6

**input:**
```
0 1 0 0 0 0 0 0 0 0 1 0
```


**output:**
```
0 1 1 1 1 1 1 1 1 1 1 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 6 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 6 6 6 0
```

Okay, let's analyze the transformation.

**Perception of Task Elements:**

*   The input and output are both 1-dimensional sequences (lists or arrays) of single-digit integers.
*   The length of the sequence remains constant between input and output.
*   The core transformation involves changing some of the zero (`0`) values in the input sequence to non-zero values in the output sequence.
*   The non-zero values present in the input seem to act as "boundaries" or "sources" for the filling process.
*   The filling occurs specifically *between* the first and the last non-zero elements found in the input sequence.
*   Zeros outside the range defined by the first and last non-zero elements are left unchanged.
*   The value used to fill the zeros seems to propagate from left to right, originating from the nearest non-zero element to the left within the active range.

**YAML Facts:**


```yaml
Data:
  - type: sequence
    format: list of integers
    content: input and output sequences

Objects:
  - name: sequence_element
    properties:
      - value: integer (0 or non-zero)
      - position: index (integer)
  - name: input_sequence
    properties:
      - elements: list of sequence_element
      - length: integer
  - name: output_sequence
    properties:
      - elements: list of sequence_element
      - length: integer (same as input)

Derived_Properties:
  - name: first_nonzero_element
    on: input_sequence
    properties:
      - index: integer (position of the first element with value != 0)
      - value: integer
  - name: last_nonzero_element
    on: input_sequence
    properties:
      - index: integer (position of the last element with value != 0)
      - value: integer
  - name: active_range
    type: range of indices
    definition: from first_nonzero_element.index to last_nonzero_element.index (inclusive)

Actions:
  - name: identify_boundaries
    inputs: input_sequence
    outputs: first_nonzero_element.index, last_nonzero_element.index
  - name: propagate_fill
    inputs:
      - input_sequence
      - first_nonzero_element.index
      - last_nonzero_element.index
    process:
      - Initialize output_sequence as a copy of input_sequence.
      - Initialize current_fill_value with the value of the first_nonzero_element.
      - Iterate from first_nonzero_element.index to last_nonzero_element.index.
      - At each index:
        - If input_sequence[index] is non-zero, update current_fill_value = input_sequence[index].
        - If output_sequence[index] is 0, set output_sequence[index] = current_fill_value.
    outputs: output_sequence

Relationships:
  - Zeros within the active_range are candidates for replacement.
  - Zeros outside the active_range remain unchanged.
  - The replacement value for a zero depends on the value of the most recent non-zero element encountered to its left (including itself) within the active_range.
```


**Natural Language Program:**

1.  Start with the input sequence of digits.
2.  Find the index of the first non-zero digit (`first_idx`) and the index of the last non-zero digit (`last_idx`) in the input sequence.
3.  If no non-zero digits are found, or only one is found, return the original input sequence unchanged.
4.  Create a new sequence (the output sequence) as a copy of the input sequence.
5.  Initialize a variable, `fill_value`, with the value of the digit at `first_idx` in the input sequence.
6.  Iterate through the indices from `first_idx` up to `last_idx` (inclusive). Let the current index be `i`.
7.  Inside the loop, check the digit at index `i` in the *input* sequence. If this digit is non-zero, update `fill_value` to this digit's value.
8.  Still inside the loop, check the digit at index `i` in the *output* sequence. If this digit is 0, change its value to the current `fill_value`.
9.  After the loop finishes, return the modified output sequence.
```python
import math
import numpy as np # Although not strictly necessary for lists, numpy is often useful for grid-like operations

"""
Transforms a sequence of digits by filling the zeros between the first and last non-zero digits. 
The fill value propagates from left to right, starting with the value of the first non-zero digit, 
and updating whenever a new non-zero digit is encountered in the input sequence within that range.
Zeros outside the range defined by the first and last non-zero digits remain unchanged.
"""

def find_first_nonzero_index(sequence):
    """Finds the index of the first non-zero element."""
    for i, val in enumerate(sequence):
        if val != 0:
            return i
    return -1 # Return -1 if no non-zero element is found

def find_last_nonzero_index(sequence):
    """Finds the index of the last non-zero element."""
    for i in range(len(sequence) - 1, -1, -1):
        if sequence[i] != 0:
            return i
    return -1 # Return -1 if no non-zero element is found

def transform(input_sequence: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """

    # Find the index of the first non-zero digit
    first_idx = find_first_nonzero_index(input_sequence)

    # Find the index of the last non-zero digit
    last_idx = find_last_nonzero_index(input_sequence)

    # If no non-zero digits are found, or only one is found, return the original sequence
    if first_idx == -1 or first_idx == last_idx:
        return list(input_sequence) # Return a copy to avoid modifying the original if needed

    # Create a new sequence (the output sequence) as a copy of the input sequence
    output_sequence = list(input_sequence)

    # Initialize fill_value with the value of the digit at first_idx
    fill_value = input_sequence[first_idx]

    # Iterate through the indices from first_idx up to last_idx (inclusive)
    for i in range(first_idx, last_idx + 1):
        # Check the digit at index i in the *input* sequence.
        # If this digit is non-zero, update fill_value
        if input_sequence[i] != 0:
            fill_value = input_sequence[i]

        # Check the digit at index i in the *output* sequence.
        # If this digit is 0, change its value to the current fill_value
        if output_sequence[i] == 0:
            output_sequence[i] = fill_value

    # Return the modified output sequence
    return output_sequence
```
