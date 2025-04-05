
## train_1

**input:**
```
0 0 0 0 3 3 3 3 2 0 0 0
```


**output:**
```
0 0 0 0 3 3 3 3 2 0 0 0
```


## train_2

**input:**
```
2 0 0 0 7 7 7 7 7 0 0 0
```


**output:**
```
2 7 7 7 7 7 7 7 7 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 6 6 6 0 2
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 6 2
```


## train_4

**input:**
```
8 8 8 2 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 2 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 2 0 0 0 7 7 7 7 7
```


**output:**
```
0 0 0 2 7 7 7 7 7 7 7 7
```


## train_6

**input:**
```
0 0 0 4 4 4 4 0 0 0 2 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 4 2 0
```


## train_7

**input:**
```
3 3 3 3 3 3 3 3 3 0 2 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 2 0
```

Okay, let's analyze the provided examples to understand the transformation task.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are sequences of single digits, presented as space-separated strings. They can be interpreted as lists or arrays of integers.
2.  **Key Digit '2':** The digit '2' appears to play a special role. It acts as a boundary or a reference point for the transformation.
3.  **Key Digit '0':** The digit '0' represents empty or fillable space.
4.  **Other Digits (X):** Digits other than '0' and '2' (e.g., 3, 7, 6, 4, 8) seem to be "source" values that can propagate.
5.  **Transformation:** The core transformation involves filling sequences of '0's that are located *between* a non-zero digit `X` (where `X` is not '2') and the digit '2'. The '0's are replaced by the digit `X`.
6.  **Directionality:** The filling action propagates *towards* the '2'.
    *   If the sequence is `... X ... 0 0 0 ... 2 ...`, the '0's are filled with `X` moving rightwards towards '2'. (See train_3, train_6, train_7)
    *   If the sequence is `... 2 ... 0 0 0 ... X ...`, the '0's are filled with `X` moving leftwards towards '2'. (See train_2, train_5)
7.  **No Change Cases:** If there are no zeros between a non-zero digit `X` and the '2', or if the region next to '2' only contains zeros extending to the sequence boundary, no change occurs in that direction. (See train_1, train_4)
8.  **Implicit Assumption:** Based on the examples, there appears to be at most one '2' in any given sequence.

**Facts (YAML):**


```yaml
objects:
  - sequence: a list of single-digit integers.
  - boundary_marker: the integer 2.
  - fillable_space: the integer 0.
  - source_digit: any integer X where X is not 0 and X is not 2.

properties:
  - sequence: has indices and elements.
  - boundary_marker: has a specific index within the sequence.
  - fillable_space: can be replaced by a source_digit.
  - source_digit: determines the value used for filling.

actions:
  - find_boundary: locate the index of the boundary_marker (2).
  - scan_left: search elements to the left of the boundary_marker.
  - scan_right: search elements to the right of the boundary_marker.
  - identify_fill_region: detect consecutive fillable_spaces (0s) adjacent to the boundary_marker.
  - identify_source: find the first source_digit encountered when scanning away from the boundary_marker past a fill_region.
  - fill_region: replace the fillable_spaces (0s) in the identified region with the identified source_digit.

relationships:
  - fillable_space (0) occurs between a source_digit (X) and the boundary_marker (2).
  - filling happens *towards* the boundary_marker (2).
  - source_digit (X) must be the first non-zero digit encountered when moving away from the boundary_marker (2) across a block of zeros.
```


**Natural Language Program:**

1.  Read the input sequence of digits.
2.  Find the index of the digit '2'. If '2' is not present in the sequence, return the original sequence unchanged. Let the index of '2' be `idx_2`.
3.  Create a modifiable copy of the sequence.
4.  **Fill Left:**
    a.  Scan the sequence copy backwards from index `idx_2 - 1` down to index 0.
    b.  Find the first digit `X_left` that is not '0' and not '2'.
    c.  If such a digit `X_left` is found at index `idx_left`:
        i.  Check if all elements between `idx_left + 1` and `idx_2 - 1` (inclusive) are '0'.
        ii. If they are all '0', replace all elements in the sequence copy from `idx_left + 1` to `idx_2 - 1` with `X_left`.
5.  **Fill Right:**
    a.  Scan the sequence copy forwards from index `idx_2 + 1` up to the end of the sequence.
    b.  Find the first digit `X_right` that is not '0' and not '2'.
    c.  If such a digit `X_right` is found at index `idx_right`:
        i.  Check if all elements between `idx_2 + 1` and `idx_right - 1` (inclusive) are '0'.
        ii. If they are all '0', replace all elements in the sequence copy from `idx_2 + 1` to `idx_right - 1` with `X_right`.
6.  Return the modified sequence.
```python
import math
import numpy as np
import re # Using re for potentially more complex string parsing if needed later, though split() is sufficient now.

"""
Transformation Rule:
1. Find the digit '2' in the input sequence.
2. Identify contiguous sequences of '0's immediately adjacent to the '2' on either side.
3. Look for the first non-'0', non-'2' digit encountered when moving away from the '2' past these '0' sequences.
4. If such a digit ('source_digit') is found and the sequence between it and the '2' consists only of '0's, replace those '0's with the 'source_digit'.
5. Perform this check and potential fill operation independently for the left and right sides of the '2'.
6. If '2' is not present, or if the conditions for filling are not met on either side, the sequence remains unchanged in that region.
"""

def _parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def _format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.
    Finds '2', identifies adjacent '0' sequences, finds the nearest
    non-zero/non-2 source digits, and fills the '0's towards the '2'
    if the intermediate region is all '0's.
    """
    input_list = _parse_input(input_str)
    output_list = list(input_list) # Create a modifiable copy
    n = len(output_list)

    # Find the index of the boundary marker '2'
    idx_2 = -1
    try:
        idx_2 = input_list.index(2)
    except ValueError:
        # '2' is not in the list, return the original sequence
        return input_str

    # --- Fill Left ---
    idx_left = -1
    source_left = -1
    # Scan leftwards from idx_2 - 1 to find the first non-0, non-2 digit
    for i in range(idx_2 - 1, -1, -1):
        if output_list[i] != 0 and output_list[i] != 2:
            idx_left = i
            source_left = output_list[i]
            break # Found the first source digit

    # If a potential source digit was found on the left
    if idx_left != -1:
        # Check if all elements between idx_left and idx_2 are '0'
        all_zeros_between = True
        for i in range(idx_left + 1, idx_2):
            if output_list[i] != 0:
                all_zeros_between = False
                break
        
        # If the condition is met, fill the zeros
        if all_zeros_between:
            for i in range(idx_left + 1, idx_2):
                output_list[i] = source_left

    # --- Fill Right ---
    idx_right = -1
    source_right = -1
    # Scan rightwards from idx_2 + 1 to find the first non-0, non-2 digit
    for i in range(idx_2 + 1, n):
        if output_list[i] != 0 and output_list[i] != 2:
            idx_right = i
            source_right = output_list[i]
            break # Found the first source digit

    # If a potential source digit was found on the right
    if idx_right != -1:
        # Check if all elements between idx_2 and idx_right are '0'
        all_zeros_between = True
        for i in range(idx_2 + 1, idx_right):
            if output_list[i] != 0:
                all_zeros_between = False
                break

        # If the condition is met, fill the zeros
        if all_zeros_between:
            for i in range(idx_2 + 1, idx_right):
                output_list[i] = source_right

    # Format the modified list back into a string
    return _format_output(output_list)

```
```python
import numpy as np

"""
Transformation Rule:
1. Find the digit '2' (boundary_marker) in the input sequence (list or array of integers).
2. If '2' is not found, return the original sequence.
3. Scan leftwards from '2' to find the first digit 'X' (source_digit) that is not '0' and not '2'.
4. If such an 'X' is found, check if all elements between 'X' and '2' are '0' (fillable_space).
5. If the condition in step 4 is met, replace those '0's with 'X'.
6. Repeat steps 3-5 scanning rightwards from '2'.
7. Return the modified sequence. Operations on left and right sides are independent.
"""

def _find_boundary_marker(sequence: np.ndarray, marker: int = 2) -> int:
    """Finds the index of the first occurrence of the marker in the sequence."""
    indices = np.where(sequence == marker)[0]
    return indices[0] if len(indices) > 0 else -1

def _find_source_digit_left(sequence: np.ndarray, boundary_idx: int) -> tuple[int, int]:
    """Finds the index and value of the first non-0, non-2 digit to the left of boundary_idx."""
    for i in range(boundary_idx - 1, -1, -1):
        if sequence[i] != 0 and sequence[i] != 2:
            return i, sequence[i] # index, value
    return -1, -1 # index, value

def _find_source_digit_right(sequence: np.ndarray, boundary_idx: int) -> tuple[int, int]:
    """Finds the index and value of the first non-0, non-2 digit to the right of boundary_idx."""
    n = len(sequence)
    for i in range(boundary_idx + 1, n):
        if sequence[i] != 0 and sequence[i] != 2:
            return i, sequence[i] # index, value
    return -1, -1 # index, value

def _check_intermediate_zeros(sequence: np.ndarray, start_idx: int, end_idx: int) -> bool:
    """Checks if all elements in the slice sequence[start_idx:end_idx] are 0."""
    # Ensure indices are valid and start < end for slicing
    if start_idx >= end_idx or start_idx < 0 or end_idx > len(sequence):
        return True # Empty or invalid slice is considered "all zeros" for this logic
    return np.all(sequence[start_idx:end_idx] == 0)

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array sequence.
    """
    # Create a modifiable copy
    output_sequence = np.copy(input_sequence)
    n = len(output_sequence)

    # 1. Find the index of the boundary marker '2'
    idx_2 = _find_boundary_marker(output_sequence, 2)

    # 2. If '2' is not found, return the original sequence
    if idx_2 == -1:
        return output_sequence

    # --- Process Left Side ---
    # 3. Scan left for source digit
    left_source_idx, left_source_value = _find_source_digit_left(output_sequence, idx_2)

    # 4. If source found, check intermediate zeros
    if left_source_idx != -1:
        is_all_zeros_left = _check_intermediate_zeros(output_sequence, left_source_idx + 1, idx_2)

        # 5. If intermediate are zeros, fill the region
        if is_all_zeros_left:
            fill_start_left = left_source_idx + 1
            fill_end_left = idx_2
            if fill_start_left < fill_end_left: # Ensure there's actually a region to fill
                output_sequence[fill_start_left:fill_end_left] = left_source_value

    # --- Process Right Side ---
    # 6. Scan right for source digit
    right_source_idx, right_source_value = _find_source_digit_right(output_sequence, idx_2)

    # 7. If source found, check intermediate zeros
    if right_source_idx != -1:
        is_all_zeros_right = _check_intermediate_zeros(output_sequence, idx_2 + 1, right_source_idx)

        # 8. If intermediate are zeros, fill the region
        if is_all_zeros_right:
            fill_start_right = idx_2 + 1
            fill_end_right = right_source_idx
            if fill_start_right < fill_end_right: # Ensure there's actually a region to fill
                output_sequence[fill_start_right:fill_end_right] = right_source_value

    # Return the modified sequence
    return output_sequence
```
