
## train_1

**input:**
```
0 0 0 4 9 6 6 0 0 0 0 0
```


**output:**
```
0 0 0 6 6 9 4 0 0 0 0 0
```


## train_2

**input:**
```
9 3 3 9 3 7 0 0 0 0 0 0
```


**output:**
```
7 3 9 3 3 9 0 0 0 0 0 0
```


## train_3

**input:**
```
0 7 9 9 4 2 9 8 1 8 1 3
```


**output:**
```
0 3 1 8 1 8 9 2 4 9 9 7
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 3 1 1 6
```


**output:**
```
0 0 0 0 0 0 0 0 6 1 1 3
```


## train_5

**input:**
```
0 7 3 7 1 1 6 5 7 5 5 5
```


**output:**
```
0 5 5 5 7 5 6 1 1 7 3 7
```


## train_6

**input:**
```
0 0 0 0 0 0 4 7 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 7 4 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 1 6 7 6 8 4 0
```


**output:**
```
0 0 0 0 0 4 8 6 7 6 1 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences (lists) of single-digit integers.
    *   The length of the input sequence is preserved in the output sequence.
    *   The core transformation involves reversing a specific portion of the sequence.
    *   The digits '0' act as delimiters or padding around the segment that is reversed. Zeros outside this core segment remain in their original positions.
    *   The segment to be reversed is the contiguous block containing all non-zero digits, starting from the first non-zero digit and ending with the last non-zero digit in the original sequence.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          - type: list of integers
          - contains: digits (0-9)
          - length: variable, but consistent between input and output
      - object: non_zero_segment
        properties:
          - type: sub-sequence
          - location: within the main sequence
          - definition: the contiguous block from the first non-zero digit to the last non-zero digit (inclusive)
          - may_be_empty: false (implied by examples, although an all-zero input isn't shown)
        relationships:
          - contained_within: sequence
      - object: zero_padding
        properties:
          - type: sub-sequence(s)
          - value: consists only of the digit 0
          - location: before the first non-zero digit (leading zeros) and after the last non-zero digit (trailing zeros)
        relationships:
          - surrounds: non_zero_segment (potentially empty leading/trailing padding)
    actions:
      - name: identify_segment
        inputs: sequence
        outputs: start_index, end_index (of the non_zero_segment)
        description: Find the index of the first non-zero digit and the index of the last non-zero digit.
      - name: extract_subsequences
        inputs: sequence, start_index, end_index
        outputs: leading_zeros, non_zero_segment, trailing_zeros
        description: Separate the sequence into three parts based on the identified indices.
      - name: reverse_segment
        inputs: non_zero_segment
        outputs: reversed_segment
        description: Reverse the order of the elements within the non_zero_segment.
      - name: reconstruct_sequence
        inputs: leading_zeros, reversed_segment, trailing_zeros
        outputs: output_sequence
        description: Concatenate the leading zeros, the reversed segment, and the trailing zeros to form the final output.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of digits.
    2.  Identify the index of the first non-zero digit in the sequence. If no non-zero digits exist, return the original sequence.
    3.  Identify the index of the last non-zero digit in the sequence.
    4.  Extract the sub-sequence containing the digits from the first non-zero index up to and including the last non-zero index (the "non-zero segment").
    5.  Extract the sub-sequence of leading zeros (all digits before the first non-zero index).
    6.  Extract the sub-sequence of trailing zeros (all digits after the last non-zero index).
    7.  Reverse the order of the digits within the extracted "non-zero segment".
    8.  Construct the output sequence by concatenating the leading zeros, the reversed non-zero segment, and the trailing zeros in that order.
    9.  Return the constructed output sequence.
```python
import math

"""
Reverses the contiguous sub-sequence of non-zero digits within a sequence of digits, leaving any leading or trailing zeros in their original positions.

1.  Identify the index of the first non-zero digit.
2.  Identify the index of the last non-zero digit.
3.  If no non-zero digits exist, return the original sequence.
4.  Extract the sub-sequence from the first non-zero index to the last non-zero index (inclusive).
5.  Extract any leading zeros (before the first non-zero index).
6.  Extract any trailing zeros (after the last non-zero index).
7.  Reverse the extracted non-zero sub-sequence.
8.  Concatenate the leading zeros, the reversed non-zero sub-sequence, and the trailing zeros to form the output sequence.
"""

def find_first_nonzero_index(sequence):
    """Finds the index of the first non-zero element in a sequence."""
    for i, value in enumerate(sequence):
        if value != 0:
            return i
    return -1 # Indicate no non-zero element found

def find_last_nonzero_index(sequence):
    """Finds the index of the last non-zero element in a sequence."""
    last_index = -1
    for i, value in enumerate(sequence):
        if value != 0:
            last_index = i
    return last_index

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # Convert string input (if provided as space-separated digits) to list of ints
    # Assuming input_sequence is already a list of integers based on examples
    # If it were a string: input_sequence = [int(d) for d in input_str.split()]

    # Find the start and end indices of the non-zero segment
    start_index = find_first_nonzero_index(input_sequence)

    # Handle the case where the sequence contains only zeros
    if start_index == -1:
        return list(input_sequence) # Return a copy of the original sequence

    end_index = find_last_nonzero_index(input_sequence)

    # Extract the three parts: leading zeros, non-zero segment, trailing zeros
    leading_zeros = input_sequence[:start_index]
    non_zero_segment = input_sequence[start_index : end_index + 1]
    trailing_zeros = input_sequence[end_index + 1 :]

    # Reverse the non-zero segment
    reversed_segment = non_zero_segment[::-1]

    # Reconstruct the sequence
    output_sequence = leading_zeros + reversed_segment + trailing_zeros

    return output_sequence

```
