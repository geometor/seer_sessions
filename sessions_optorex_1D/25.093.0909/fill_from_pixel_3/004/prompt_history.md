
## train_1

**input:**
```
0 0 3 8 8 8 0 0 0 0 0 0
```


**output:**
```
3 3 3 8 8 8 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 4 4 4 4 4 0 0 0 0 0
```


**output:**
```
2 2 4 4 4 4 4 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 5 6 6 6 0 0
```


**output:**
```
5 5 5 5 5 5 5 6 6 6 0 0
```


## train_4

**input:**
```
0 0 0 0 5 7 7 7 7 0 0 0
```


**output:**
```
5 5 5 5 5 7 7 7 7 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 7 7 7 7 8 0 0
```


**output:**
```
0 0 0 0 0 7 7 7 7 8 8 8
```


## train_6

**input:**
```
0 2 3 3 3 3 3 3 0 0 0 0
```


**output:**
```
2 2 3 3 3 3 3 3 0 0 0 0
```


## train_7

**input:**
```
0 5 5 5 5 5 5 9 0 0 0 0
```


**output:**
```
0 5 5 5 5 5 5 9 9 9 9 9
```

*   **Perception of Elements:**
    *   The task operates on sequences (lists) of single-digit integers.
    *   Each sequence has a fixed length (12 in the examples).
    *   The sequences contain blocks of non-zero digits, often bordered by zeros (value 0).
    *   The transformation modifies either the leading zeros or the trailing zeros, but not both.
    *   The modification involves replacing these zeros with a specific non-zero digit derived from the sequence itself.

*   **YAML Facts:**
    
```yaml
    elements:
      - sequence: list of integers (typically 0-9)
      - zero: integer value 0
      - non_zero_digit: integer value 1-9
    
    objects:
      - input_sequence:
          type: sequence
          description: The initial list of integers provided.
      - output_sequence:
          type: sequence
          description: The final list of integers after transformation.
      - first_non_zero:
          type: object
          properties:
            value: non_zero_digit
            index: integer (position in sequence)
          relation: The non-zero digit appearing earliest (smallest index) in the input_sequence. Null if sequence contains only zeros.
      - last_non_zero:
          type: object
          properties:
            value: non_zero_digit
            index: integer (position in sequence)
          relation: The non-zero digit appearing latest (largest index) in the input_sequence. Null if sequence contains only zeros.
      - leading_zeros_segment:
          type: sequence_segment
          relation: The subsequence from index 0 up to (but not including) first_non_zero.index. Empty if first_non_zero.index is 0.
      - trailing_zeros_segment:
          type: sequence_segment
          relation: The subsequence from index last_non_zero.index + 1 to the end of the sequence. Empty if last_non_zero.index is the last index.
    
    conditions_and_actions:
      - condition: input_sequence contains no non_zero_digit
        action: Set output_sequence to be identical to input_sequence.
      - condition: input_sequence contains non_zero_digits
        action: 
          - Identify first_non_zero (value `F_val`, index `F_idx`).
          - Identify last_non_zero (value `L_val`, index `L_idx`).
          - Calculate sum `S = F_val + L_val`.
          - if S >= 14:
              action: (Right Expansion) Modify a copy of input_sequence by replacing elements in the trailing_zeros_segment with `L_val`. Result is output_sequence.
          - else (S < 14):
              action: (Left Expansion) Modify a copy of input_sequence by replacing elements in the leading_zeros_segment with `F_val`. Result is output_sequence.

    ```


*   **Natural Language Program:**
    
```text
    1. Start with the input sequence of integers.
    2. Find the first non-zero integer (`first_val`) and its position (`first_idx`).
    3. Find the last non-zero integer (`last_val`) and its position (`last_idx`).
    4. If no non-zero integers are found (the sequence is all zeros), the output is the same as the input.
    5. Otherwise, calculate the sum `S = first_val + last_val`.
    6. Create a copy of the input sequence to modify.
    7. If `S` is greater than or equal to 14:
        a. Change all elements in the copied sequence from position `last_idx + 1` to the end of the sequence to the value `last_val`.
    8. Else (if `S` is less than 14):
        a. Change all elements in the copied sequence from the beginning (position 0) up to (but not including) position `first_idx` to the value `first_val`.
    9. The modified sequence is the output.
    ```
```python
import math

"""
Find the first and last non-zero integers in the input sequence. If the sequence contains only zeros, return it unchanged. Otherwise, calculate the sum of the first and last non-zero integers. If the sum is 14 or greater, replace all trailing zeros (after the last non-zero integer) with the value of the last non-zero integer. If the sum is less than 14, replace all leading zeros (before the first non-zero integer) with the value of the first non-zero integer.
"""

def find_first_non_zero(sequence):
    """Finds the value and index of the first non-zero element."""
    for i, val in enumerate(sequence):
        if val != 0:
            return val, i
    return None, -1 # No non-zero element found

def find_last_non_zero(sequence):
    """Finds the value and index of the last non-zero element."""
    last_val = None
    last_idx = -1
    for i, val in enumerate(sequence):
        if val != 0:
            last_val = val
            last_idx = i
    return last_val, last_idx # Returns None, -1 if no non-zero element found

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """

    # Find the first non-zero element and its index
    first_val, first_idx = find_first_non_zero(input_sequence)

    # Handle the case where the sequence is all zeros
    if first_val is None:
        return list(input_sequence) # Return a copy

    # Find the last non-zero element and its index
    last_val, last_idx = find_last_non_zero(input_sequence)
    # Note: If first_val is not None, last_val will also not be None.

    # Calculate the sum
    s = first_val + last_val

    # Create a copy of the input sequence to modify
    output_sequence = list(input_sequence)

    # Apply the transformation based on the sum
    if s >= 14:
        # Right Expansion: Change trailing zeros
        # Iterate from the position after the last non-zero element to the end
        for i in range(last_idx + 1, len(output_sequence)):
            output_sequence[i] = last_val
    else:
        # Left Expansion: Change leading zeros
        # Iterate from the beginning up to the first non-zero element
        for i in range(first_idx):
            output_sequence[i] = first_val

    return output_sequence
```
```python
import numpy as np

"""
Transforms a 1D sequence of integers based on its first and last non-zero elements.

1.  Find the first non-zero integer (`first_val`) and its position (`first_idx`).
2.  Find the last non-zero integer (`last_val`) and its position (`last_idx`).
3.  If no non-zero integers are found (the sequence is all zeros), return a copy of the input.
4.  Otherwise, calculate the sum `S = first_val + last_val`.
5.  If `S` is greater than or equal to 14:
    a. Change all elements in a copy of the sequence from position `last_idx + 1` to the end to the value `last_val` (Right Expansion).
6.  Else (if `S` is less than 14):
    a. Change all elements in a copy of the sequence from the beginning (position 0) up to (but not including) position `first_idx` to the value `first_val` (Left Expansion).
7.  Return the modified sequence.
"""

def find_first_last_non_zero(sequence):
    """
    Finds the value and index of the first and last non-zero elements in a NumPy array.

    Args:
        sequence: A 1D NumPy array of integers.

    Returns:
        A tuple: (first_val, first_idx, last_val, last_idx).
        Returns (None, -1, None, -1) if no non-zero elements are found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(sequence)[0]

    # Check if any non-zero elements exist
    if non_zero_indices.size == 0:
        return None, -1, None, -1

    # Get the first and last indices
    first_idx = non_zero_indices[0]
    last_idx = non_zero_indices[-1]

    # Get the values at these indices
    first_val = sequence[first_idx]
    last_val = sequence[last_idx]

    return first_val, first_idx, last_val, last_idx


def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_sequence: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a numpy array for consistency
    if not isinstance(input_sequence, np.ndarray):
        input_sequence = np.array(input_sequence) # convert list to numpy

    # Find the first and last non-zero elements and their indices
    first_val, first_idx, last_val, last_idx = find_first_last_non_zero(input_sequence)

    # Handle the case where the sequence is all zeros
    if first_val is None:
        return input_sequence.copy() # Return a copy

    # Calculate the sum
    s = first_val + last_val

    # Create a copy of the input sequence to modify
    output_sequence = input_sequence.copy()

    # Apply the transformation based on the sum
    if s >= 14:
        # Right Expansion: Change trailing zeros
        # Use slicing to modify elements from last_idx + 1 to the end
        if last_idx + 1 < len(output_sequence): # Check if there are trailing elements
            output_sequence[last_idx + 1:] = last_val
    else:
        # Left Expansion: Change leading zeros
        # Use slicing to modify elements from the beginning up to first_idx
        if first_idx > 0: # Check if there are leading elements
             output_sequence[:first_idx] = first_val

    return output_sequence
```
