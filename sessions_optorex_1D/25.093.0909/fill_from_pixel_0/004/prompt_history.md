
## train_1

**input:**
```
0 0 0 0 1 1 1 1 7 0 0 0
```


**output:**
```
0 0 0 0 1 1 1 1 7 7 7 7
```


## train_2

**input:**
```
0 0 9 9 9 9 9 2 0 0 0 0
```


**output:**
```
0 0 9 9 9 9 9 2 2 2 2 2
```


## train_3

**input:**
```
0 2 2 2 2 2 5 0 0 0 0 0
```


**output:**
```
0 2 2 2 2 2 5 5 5 5 5 5
```


## train_4

**input:**
```
0 0 0 0 1 1 1 1 1 1 5 0
```


**output:**
```
0 0 0 0 1 1 1 1 1 1 5 5
```


## train_5

**input:**
```
0 0 0 1 8 8 8 8 8 8 0 0
```


**output:**
```
1 1 1 1 8 8 8 8 8 8 0 0
```


## train_6

**input:**
```
0 0 7 9 9 9 9 9 9 0 0 0
```


**output:**
```
7 7 7 9 9 9 9 9 9 0 0 0
```


## train_7

**input:**
```
0 0 6 6 6 6 9 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 6 9 9 9 9 9 9
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of the Elements:**

1.  **Input/Output Format:** Both input and output are sequences (lists) of single-digit integers.
2.  **Key Objects:** The core objects are the individual digits within the sequence, specifically differentiating between zero (`0`) and non-zero digits (e.g., `1`, `2`, `5`, `6`, `7`, `8`, `9`).
3.  **Observed Pattern:** The transformation primarily involves modifying the zero digits at the beginning and end of the sequence.
    *   Zeros at the *beginning* of the sequence are replaced by the value of the *first* non-zero digit encountered when scanning from left to right.
    *   Zeros at the *end* of the sequence are replaced by the value of the *last* non-zero digit encountered when scanning from left to right (or the first non-zero digit when scanning from right to left).
    *   The non-zero digits and any zeros *between* the first and last non-zero digits remain unchanged.
4.  **Implicit Action:** The process seems to involve identifying the boundaries defined by the first and last non-zero digits and then "filling" the regions outside these boundaries (leading and trailing zeros) with the respective boundary non-zero values.

**YAML Facts:**


```yaml
Objects:
  - Sequence: A list of single-digit integers.
  - Digit: An element within the sequence.
    Properties:
      - Value: The integer value (0-9).
      - IsZero: Boolean (True if value is 0, False otherwise).
      - Position: The index within the sequence.

Relationships:
  - LeftmostNonZero: The first digit in the sequence (from left) whose value is not 0.
  - RightmostNonZero: The last digit in the sequence (from left) whose value is not 0.
  - LeadingZeros: All digits with value 0 preceding the LeftmostNonZero digit.
  - TrailingZeros: All digits with value 0 succeeding the RightmostNonZero digit.

Actions:
  - Identify: Find the LeftmostNonZero and RightmostNonZero digits and their positions/values.
  - Propagate Left: Replace the value of all LeadingZeros with the value of the LeftmostNonZero digit.
  - Propagate Right: Replace the value of all TrailingZeros with the value of the RightmostNonZero digit.
```


**Natural Language Program:**

1.  Take the input sequence of digits.
2.  Find the index and value of the first non-zero digit from the left (LeftmostNonZero). If no non-zero digits exist, the sequence remains unchanged.
3.  Find the index and value of the last non-zero digit from the left (RightmostNonZero).
4.  Create a copy of the input sequence to serve as the output sequence.
5.  Iterate from the beginning of the output sequence up to (but not including) the index of the LeftmostNonZero digit. Set the value of each digit in this range to the value of the LeftmostNonZero digit.
6.  Iterate from the end of the output sequence backwards, starting from the index after the RightmostNonZero digit. Set the value of each digit in this range to the value of the RightmostNonZero digit.
7.  Return the modified output sequence.
```python
import copy

"""
Transforms a sequence of digits by propagating the nearest non-zero digit 
outwards to replace leading and trailing zeros.

1. Find the index and value of the first non-zero digit from the left (LeftmostNonZero).
2. Find the index and value of the last non-zero digit from the left (RightmostNonZero).
3. If no non-zero digits exist, the sequence remains unchanged.
4. Create a copy of the input sequence.
5. Replace all digits from the beginning up to the LeftmostNonZero index with the LeftmostNonZero value.
6. Replace all digits from the index after RightmostNonZero to the end with the RightmostNonZero value.
7. Return the modified sequence.
"""

def find_first_non_zero(sequence):
    """Finds the index and value of the first non-zero element."""
    for index, value in enumerate(sequence):
        if value != 0:
            return index, value
    return None, None # Return None if no non-zero element is found

def find_last_non_zero(sequence):
    """Finds the index and value of the last non-zero element."""
    last_index = -1
    last_value = None
    for index, value in enumerate(sequence):
        if value != 0:
            last_index = index
            last_value = value
    if last_index == -1:
        return None, None # Return None if no non-zero element is found
    return last_index, last_value


def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # Find the first non-zero element
    first_nz_index, first_nz_value = find_first_non_zero(input_sequence)

    # If no non-zero elements exist, return the original sequence
    if first_nz_index is None:
        return input_sequence[:] # Return a copy

    # Find the last non-zero element
    last_nz_index, last_nz_value = find_last_non_zero(input_sequence)

    # Initialize the output sequence as a copy of the input
    output_sequence = list(input_sequence) # Ensure it's a list copy

    # Propagate the first non-zero value to the left (leading zeros)
    for i in range(first_nz_index):
        output_sequence[i] = first_nz_value

    # Propagate the last non-zero value to the right (trailing zeros)
    for i in range(last_nz_index + 1, len(output_sequence)):
        output_sequence[i] = last_nz_value

    # Return the modified sequence
    return output_sequence

```
```python
import numpy as np

"""
Transforms a sequence of digits based on the comparison of its first and last non-zero elements and the counts of leading/trailing zeros.

1. Find the first non-zero element (value F, index Fi) and the last non-zero element (value L, index Li).
2. If no non-zero elements exist, return the sequence unchanged.
3. Count leading zeros (LZ = Fi) and trailing zeros (TZ = length - 1 - Li).
4. Apply the following rules:
    a. If F > L: Fill the trailing zeros (indices > Li) with L.
    b. If F <= L:
        i. If LZ >= TZ: Fill the leading zeros (indices < Fi) with F.
        ii. If LZ < TZ: Fill the trailing zeros (indices > Li) with L.
"""

def find_first_non_zero(arr):
    """Finds the index and value of the first non-zero element in a numpy array."""
    non_zero_indices = np.where(arr != 0)[0]
    if len(non_zero_indices) == 0:
        return None, None  # No non-zero elements found
    first_nz_index = non_zero_indices[0]
    first_nz_value = arr[first_nz_index]
    return first_nz_index, first_nz_value

def find_last_non_zero(arr):
    """Finds the index and value of the last non-zero element in a numpy array."""
    non_zero_indices = np.where(arr != 0)[0]
    if len(non_zero_indices) == 0:
        return None, None  # No non-zero elements found
    last_nz_index = non_zero_indices[-1]
    last_nz_value = arr[last_nz_index]
    return last_nz_index, last_nz_value

def transform(input_arr):
    """
    Applies the transformation rule to the input numpy array.
    """
    # Ensure input is a numpy array (though context suggests it already is)
    if not isinstance(input_arr, np.ndarray):
        input_arr = np.array(input_arr)
        
    # Make a copy to modify
    output_arr = input_arr.copy()
    
    # Find boundaries
    first_nz_idx, first_nz_val = find_first_non_zero(input_arr)
    last_nz_idx, last_nz_val = find_last_non_zero(input_arr)

    # Handle edge case: all zeros or no non-zeros
    if first_nz_idx is None:
        return output_arr # Return the original array copy

    # Calculate zero counts
    leading_zeros = first_nz_idx
    trailing_zeros = len(input_arr) - 1 - last_nz_idx

    # Apply Hypothesis 16 logic
    if first_nz_val > last_nz_val:
        # Rule 1: Fill Trailing Zeros with Last Non-Zero Value
        if trailing_zeros > 0:
             output_arr[last_nz_idx + 1:] = last_nz_val
    else: # first_nz_val <= last_nz_val
        # Rule 2a: Leading Zeros >= Trailing Zeros -> Fill Leading with First Non-Zero Value
        if leading_zeros >= trailing_zeros:
            if leading_zeros > 0:
                output_arr[:first_nz_idx] = first_nz_val
        # Rule 2b: Leading Zeros < Trailing Zeros -> Fill Trailing with Last Non-Zero Value
        else: # leading_zeros < trailing_zeros
             if trailing_zeros > 0:
                output_arr[last_nz_idx + 1:] = last_nz_val

    return output_arr
```
