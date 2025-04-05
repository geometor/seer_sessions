
## train_1

**input:**
```
0 3 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 4 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 4 1 1 2 6 0 0 0 0
```


**output:**
```
0 0 0 0 4 1 1 2 6 0 0 0
```


## train_3

**input:**
```
8 1 2 1 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 1 2 1 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 5 9 6 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 5 9 6 0 0
```


## train_5

**input:**
```
0 2 5 2 8 7 1 7 9 6 1 0
```


**output:**
```
0 0 2 5 2 8 7 1 7 9 6 1
```


## train_6

**input:**
```
0 0 0 4 2 6 8 4 5 7 0 0
```


**output:**
```
0 0 0 0 4 2 6 8 4 5 7 0
```


## train_7

**input:**
```
0 0 0 0 0 5 5 9 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 5 5 9 0 0 0
```

## Perception

The input and output are sequences (lists) of single-digit integers, always of the same length (12 in the examples). The transformation involves shifting a specific sub-sequence within the list one position to the right.

1.  **Identify Key Elements:** The core elements are the sequence itself and a sub-sequence within it. This sub-sequence appears to be defined by the positions of the first and last non-zero numbers. Zeros within this sub-sequence are treated as part of the sub-sequence.
2.  **Identify the Action:** The primary action is a 'shift right' operation applied to the identified sub-sequence.
3.  **Identify Invariants:** The length of the sequence remains constant. The relative order and values of the elements *within* the shifted sub-sequence are preserved. Elements *before* the sub-sequence also remain in their original positions.
4.  **Identify Changes:** The sub-sequence moves one position to the right. The position immediately preceding the original start of the sub-sequence becomes 0. Elements originally after the sub-sequence might be overwritten or effectively dropped if the shift extends to the end of the list's bounds.

## Facts


```yaml
task_elements:
  - item: sequence
    type: list
    subtype: integer
    properties:
      - length: fixed (e.g., 12 in examples)
      - elements: single digits (0-9)
  - item: active_subsequence
    type: sublist
    derivation: determined by the span from the first non-zero element to the last non-zero element in the input sequence.
    properties:
      - includes all elements within its start and end indices, including any zeros.
      - If the input sequence contains only zeros, this subsequence is considered empty or non-existent.
relationships:
  - input sequence contains the active_subsequence.
  - output sequence is derived from the input sequence.
actions:
  - identify: find the start and end indices of the active_subsequence in the input.
  - shift: move the active_subsequence one position to the right.
  - insert: place a zero at the original starting position of the active_subsequence.
  - preserve: maintain the original elements located before the active_subsequence.
  - maintain_length: ensure the output sequence has the same length as the input sequence (elements shifted beyond the original boundary are implicitly dropped).
transformation:
  - condition: If an active_subsequence exists (i.e., at least one non-zero element is present).
    steps:
      - Locate the index of the first non-zero element (`start_index`).
      - Locate the index of the last non-zero element (`end_index`).
      - Construct the output sequence by:
        - Copying elements from index 0 to `start_index - 1` from the input to the output at the same indices.
        - Placing a 0 at `start_index` in the output.
        - Copying elements from `start_index` to `end_index` from the input to the output, starting at index `start_index + 1` and ending at `end_index + 1`.
        - Filling any remaining positions in the output (after `end_index + 1`) with zeros, up to the original sequence length.
  - condition: If no active_subsequence exists (input is all zeros).
    steps:
      - The output sequence is identical to the input sequence.

```


## Natural Language Program

1.  Examine the input sequence of numbers.
2.  Find the index of the first non-zero number (`first_nz`).
3.  Find the index of the last non-zero number (`last_nz`).
4.  If no non-zero numbers are found (the sequence is all zeros), the output is identical to the input.
5.  Otherwise:
    a.  Create a new output sequence of the same length as the input, initially filled with zeros.
    b.  Copy the elements from the input sequence from index 0 up to (but not including) `first_nz` into the output sequence at the same positions.
    c.  Copy the elements from the input sequence starting at index `first_nz` up to and including index `last_nz` into the output sequence, starting at index `first_nz + 1` and ending at index `last_nz + 1`.
6.  Return the newly constructed output sequence.
```python
import math
import numpy as np # Commonly used for array/grid operations

"""
Transformation Rule:
Find the subsequence bounded by the first and last non-zero elements in the input sequence. 
Shift this entire subsequence one position to the right. 
Place a zero at the original starting position of the subsequence. 
Elements before the subsequence remain unchanged. Elements after the subsequence are effectively shifted or replaced by zeros to maintain the original sequence length. 
If the input sequence contains only zeros, return it unchanged.
"""

def find_first_non_zero(seq):
    """Finds the index of the first non-zero element."""
    for i, x in enumerate(seq):
        if x != 0:
            return i
    return -1 # Indicate not found

def find_last_non_zero(seq):
    """Finds the index of the last non-zero element."""
    last_idx = -1
    for i, x in enumerate(seq):
        if x != 0:
            last_idx = i
    return last_idx # Returns -1 if no non-zeros found

def transform(input_str: str) -> str:
    """
    Applies the described transformation to the input sequence string.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the transformed space-separated integers.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Find the start and end indices of the active subsequence
    first_nz = find_first_non_zero(input_list)
    last_nz = find_last_non_zero(input_list)

    # Handle the case where the input is all zeros
    if first_nz == -1:
        return input_str # No non-zeros, return original

    # Initialize the output list with zeros
    output_list = [0] * n

    # Copy elements before the active subsequence
    for i in range(first_nz):
        output_list[i] = input_list[i]

    # The position where the subsequence originally started becomes 0
    # This is handled by the initialization unless first_nz is 0,
    # but explicitly setting it is clearer for the logic.
    # If first_nz > 0, output_list[first_nz] will be 0.
    # if first_nz == 0, the element at index 0 will be overwritten
    # by the shifted sequence starting at index 1.

    # Copy the active subsequence shifted one position to the right
    # Ensure we don't write past the end of the output list
    for i in range(first_nz, last_nz + 1):
        target_index = i + 1
        if target_index < n: # Check boundary
            output_list[target_index] = input_list[i]
        # else: element is shifted out of bounds

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str

# Example usage with one of the provided test cases:
# input_example = "0 3 4 0 0 0 0 0 0 0 0 0"
# output_example = transform(input_example)
# print(f"Input:  {input_example}")
# print(f"Output: {output_example}")

# input_example_2 = "0 0 0 4 1 1 2 6 0 0 0 0"
# output_example_2 = transform(input_example_2)
# print(f"Input:  {input_example_2}")
# print(f"Output: {output_example_2}")

# input_example_3 = "8 1 2 1 0 0 0 0 0 0 0 0"
# output_example_3 = transform(input_example_3)
# print(f"Input:  {input_example_3}")
# print(f"Output: {output_example_3}")

# input_example_all_zeros = "0 0 0 0 0 0 0 0 0 0 0 0"
# output_example_all_zeros = transform(input_example_all_zeros)
# print(f"Input:  {input_example_all_zeros}")
# print(f"Output: {output_example_all_zeros}")
```
