
## train_1

**input:**
```
0 2 3 3 3 3 0 0 0 0 0 0
```


**output:**
```
2 2 3 3 3 3 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 9 9 9 9 6 0 0 0
```


**output:**
```
0 0 0 0 9 9 9 9 6 6 6 6
```


## train_3

**input:**
```
0 0 7 3 3 3 3 3 0 0 0 0
```


**output:**
```
7 7 7 3 3 3 3 3 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 3 3 3 3 8 0 0 0
```


**output:**
```
0 0 0 0 3 3 3 3 8 8 8 8
```


## train_5

**input:**
```
0 9 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
9 9 4 4 4 4 4 4 0 0 0 0
```


## train_6

**input:**
```
0 0 0 4 8 8 8 8 8 0 0 0
```


**output:**
```
4 4 4 4 8 8 8 8 8 0 0 0
```


## train_7

**input:**
```
0 0 8 6 6 6 6 6 0 0 0 0
```


**output:**
```
8 8 8 6 6 6 6 6 0 0 0 0
```

Okay, let's break down the transformation logic based on the provided examples.

**Perception of Task Elements:**

The task involves manipulating sequences of 12 single-digit integers. The core operation seems to be propagating a non-zero digit into adjacent blocks of zeros at either the beginning or the end of the sequence. The key elements are:

1.  **Input Sequence:** A list of 12 integers.
2.  **Output Sequence:** A modified list of 12 integers.
3.  **Zero Blocks:** Contiguous sequences of zeros at the start (leading zeros) and end (trailing zeros) of the input sequence.
4.  **Non-Zero Boundaries:** The first non-zero digit encountered when reading from left to right, and the last non-zero digit encountered.
5.  **Propagation Rule:** A decision mechanism determines whether the first non-zero digit propagates leftwards into the leading zeros, or the last non-zero digit propagates rightwards into the trailing zeros. This decision appears to depend on the relative lengths of the leading and trailing zero blocks.

**Facts:**


```yaml
task_elements:
  - object: sequence
    properties:
      - type: list of integers
      - length: 12
      - contains: digits (0-9)
  - object: leading_zeros
    properties:
      - location: start of the sequence
      - value: 0
      - count: number of zeros before the first non-zero digit
  - object: trailing_zeros
    properties:
      - location: end of the sequence
      - value: 0
      - count: number of zeros after the last non-zero digit
  - object: first_non_zero
    properties:
      - value: the digit value of the first non-zero element
      - index: the position of the first non-zero element
  - object: last_non_zero
    properties:
      - value: the digit value of the last non-zero element
      - index: the position of the last non-zero element
relationships:
  - type: comparison
    between: count of leading_zeros
    and: count of trailing_zeros
actions:
  - action: identify_boundaries
    inputs: sequence
    outputs:
      - first_non_zero (value and index)
      - last_non_zero (value and index)
      - count of leading_zeros
      - count of trailing_zeros
  - action: conditional_fill
    condition: count of leading_zeros <= count of trailing_zeros
    operation_if_true: left_fill
    operation_if_false: right_fill
  - action: left_fill
    description: Replace all leading zeros in the sequence with the value of the first_non_zero digit.
    modifies: sequence (leading_zeros part)
  - action: right_fill
    description: Replace all trailing zeros in the sequence with the value of the last_non_zero digit.
    modifies: sequence (trailing_zeros part)

```


**Natural Language Program:**

1.  Receive the input sequence of 12 digits.
2.  Identify the first non-zero digit (FNZ) and its index (`idx_fnz`). If no non-zero digit exists, return the input sequence unchanged.
3.  Identify the last non-zero digit (LNZ) and its index (`idx_lnz`).
4.  Count the number of leading zeros (`num_left_zeros`), which is equal to `idx_fnz`.
5.  Count the number of trailing zeros (`num_right_zeros`), which is equal to `11 - idx_lnz`.
6.  Compare `num_left_zeros` and `num_right_zeros`.
7.  If `num_left_zeros` is less than or equal to `num_right_zeros`, modify the sequence by replacing all digits from index 0 up to (but not including) `idx_fnz` with the value of FNZ.
8.  Otherwise (if `num_left_zeros` is greater than `num_right_zeros`), modify the sequence by replacing all digits from index `idx_lnz + 1` up to index 11 with the value of LNZ.
9.  Return the modified sequence.
```python
import math

"""
Identifies the first and last non-zero digits in a sequence of 12 digits.
Counts the number of leading zeros (before the first non-zero) and trailing zeros (after the last non-zero).
If the count of leading zeros is less than or equal to the count of trailing zeros, replace the leading zeros with the value of the first non-zero digit.
Otherwise, replace the trailing zeros with the value of the last non-zero digit.
If the sequence contains only zeros, return it unchanged.
"""

def find_first_non_zero(seq):
    """Finds the value and index of the first non-zero element."""
    for i, val in enumerate(seq):
        if val != 0:
            return val, i
    return None, -1 # Return None and -1 if all zeros

def find_last_non_zero(seq):
    """Finds the value and index of the last non-zero element."""
    last_val = None
    last_idx = -1
    for i, val in enumerate(seq):
        if val != 0:
            last_val = val
            last_idx = i
    return last_val, last_idx

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_str: A string of 12 space-separated digits.

    Returns:
        A string representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list) # Should be 12 based on examples

    # Find the first non-zero digit and its index
    first_val, first_idx = find_first_non_zero(input_list)

    # Handle the case where the input is all zeros
    if first_val is None:
        return input_str # Return unchanged if all zeros

    # Find the last non-zero digit and its index
    last_val, last_idx = find_last_non_zero(input_list)

    # Calculate the number of leading zeros
    num_left_zeros = first_idx

    # Calculate the number of trailing zeros
    num_right_zeros = (n - 1) - last_idx

    # Create a copy of the input list to modify
    output_list = list(input_list)

    # Compare the number of leading and trailing zeros
    if num_left_zeros <= num_right_zeros:
        # Fill leading zeros with the first non-zero value
        for i in range(first_idx):
            output_list[i] = first_val
    else:
        # Fill trailing zeros with the last non-zero value
        for i in range(last_idx + 1, n):
            output_list[i] = last_val

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
```
```python
import numpy as np

"""
Identifies the first and last non-zero digits in a sequence (list or NumPy array) of 12 digits.
Counts the number of leading zeros (before the first non-zero) and trailing zeros (after the last non-zero).
If the count of leading zeros is less than or equal to the count of trailing zeros, replace the leading zeros with the value of the first non-zero digit.
Otherwise, replace the trailing zeros with the value of the last non-zero digit.
If the sequence contains only zeros, return it unchanged.
"""

def find_first_non_zero(seq):
    """
    Finds the value and index of the first non-zero element in a sequence.

    Args:
        seq: A list or NumPy array of numbers.

    Returns:
        A tuple (value, index) of the first non-zero element.
        Returns (None, -1) if all elements are zero or the sequence is empty.
    """
    for i, val in enumerate(seq):
        if val != 0:
            return val, i
    return None, -1 # Return None and -1 if all zeros or empty

def find_last_non_zero(seq):
    """
    Finds the value and index of the last non-zero element in a sequence.

    Args:
        seq: A list or NumPy array of numbers.

    Returns:
        A tuple (value, index) of the last non-zero element.
        Returns (None, -1) if all elements are zero or the sequence is empty.
    """
    last_val = None
    last_idx = -1
    for i, val in enumerate(seq):
        if val != 0:
            last_val = val
            last_idx = i
    return last_val, last_idx

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_grid: A NumPy array representing the sequence of 12 digits.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Determine the length of the sequence
    n = len(input_grid)
    if n == 0:
        return input_grid # Handle empty input

    # Find the first non-zero digit and its index
    first_val, first_idx = find_first_non_zero(input_grid)

    # Handle the case where the input is all zeros
    if first_val is None:
        return input_grid # Return unchanged if all zeros

    # Find the last non-zero digit and its index
    # (We know there's at least one non-zero element if first_val is not None)
    last_val, last_idx = find_last_non_zero(input_grid)

    # Calculate the number of leading zeros
    num_left_zeros = first_idx

    # Calculate the number of trailing zeros
    # Ensure n-1 calculation is correct for indexing
    num_right_zeros = (n - 1) - last_idx

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Compare the number of leading and trailing zeros
    if num_left_zeros <= num_right_zeros:
        # Fill leading zeros with the first non-zero value
        # Loop from index 0 up to (but not including) first_idx
        for i in range(first_idx):
            output_grid[i] = first_val
    else:
        # Fill trailing zeros with the last non-zero value
        # Loop from index last_idx + 1 up to (but not including) n
        for i in range(last_idx + 1, n):
            output_grid[i] = last_val

    # Return the modified grid
    return output_grid
```
