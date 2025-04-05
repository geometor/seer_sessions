
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
```python
import numpy as np

"""
Transformation Rule:
1. Find the index (`idx_2`) of the digit '2' (boundary_marker) in the input sequence.
2. If '2' is not found, return the original sequence.
3. Process the left side:
    a. Check if there is an element to the left (`idx_2 > 0`) and if this element is '0' (fillable_space).
    b. If both conditions are true, scan leftwards from `idx_2 - 2` to find the index (`idx_left`) and value (`X_left`) of the first non-zero digit.
    c. If such a digit `X_left` is found and it's not '2', replace all elements in the range `[idx_left + 1, idx_2 - 1]` (inclusive) with `X_left`.
4. Process the right side:
    a. Check if there is an element to the right (`idx_2 < length - 1`) and if this element is '0'.
    b. If both conditions are true, scan rightwards from `idx_2 + 2` to find the index (`idx_right`) and value (`X_right`) of the first non-zero digit.
    c. If such a digit `X_right` is found and it's not '2', replace all elements in the range `[idx_2 + 1, idx_right - 1]` (inclusive) with `X_right`.
5. Return the modified sequence. The left and right side processing are independent.
"""

def _find_boundary_marker(sequence: np.ndarray, marker: int = 2) -> int:
    """Finds the index of the first occurrence of the marker in the sequence."""
    indices = np.where(sequence == marker)[0]
    return indices[0] if len(indices) > 0 else -1

def _find_nearest_non_zero_left(sequence: np.ndarray, start_scan_idx: int) -> tuple[int, int]:
    """
    Scans leftwards from start_scan_idx to find the index and value
    of the first non-zero digit encountered.
    Returns (-1, -1) if no non-zero digit is found.
    """
    for i in range(start_scan_idx, -1, -1):
        if sequence[i] != 0:
            return i, sequence[i] # index, value
    return -1, -1 # index, value

def _find_nearest_non_zero_right(sequence: np.ndarray, start_scan_idx: int) -> tuple[int, int]:
    """
    Scans rightwards from start_scan_idx to find the index and value
    of the first non-zero digit encountered.
    Returns (-1, -1) if no non-zero digit is found.
    """
    n = len(sequence)
    for i in range(start_scan_idx, n):
        if sequence[i] != 0:
            return i, sequence[i] # index, value
    return -1, -1 # index, value

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the refined transformation rule to the input NumPy array sequence.
    """
    # Create a modifiable copy
    output_sequence = np.copy(input_sequence)
    n = len(output_sequence)
    boundary_marker = 2
    fillable_space = 0

    # 1. Find the index of the boundary marker '2'
    idx_2 = _find_boundary_marker(output_sequence, boundary_marker)

    # 2. If '2' is not found, return the original sequence
    if idx_2 == -1:
        return output_sequence

    # 3. Process Left Side
    # 3a. Check adjacent left element
    if idx_2 > 0 and output_sequence[idx_2 - 1] == fillable_space:
        # 3b. Scan left for the first non-zero digit
        left_source_idx, left_source_value = _find_nearest_non_zero_left(output_sequence, idx_2 - 2)

        # 3c. If a non-zero source is found and it's not the boundary marker itself
        if left_source_idx != -1 and left_source_value != boundary_marker:
            # Fill the region between the source and the boundary marker
            fill_start_left = left_source_idx + 1
            fill_end_left = idx_2 # Slice goes up to, but not including, idx_2
            if fill_start_left < fill_end_left:
                output_sequence[fill_start_left:fill_end_left] = left_source_value

    # 4. Process Right Side
    # 4a. Check adjacent right element
    if idx_2 < n - 1 and output_sequence[idx_2 + 1] == fillable_space:
        # 4b. Scan right for the first non-zero digit
        right_source_idx, right_source_value = _find_nearest_non_zero_right(output_sequence, idx_2 + 2)

        # 4c. If a non-zero source is found and it's not the boundary marker itself
        if right_source_idx != -1 and right_source_value != boundary_marker:
            # Fill the region between the boundary marker and the source
            fill_start_right = idx_2 + 1
            fill_end_right = right_source_idx # Slice goes up to, but not including, idx_right
            if fill_start_right < fill_end_right:
                output_sequence[fill_start_right:fill_end_right] = right_source_value

    # 5. Return the modified sequence
    return output_sequence
```

Previous Code:
```python
import numpy as np

"""
Transformation Rule:
1. Find the index (`idx_2`) of the digit '2' (boundary_marker) in the input sequence.
2. If '2' is not found, return the original sequence.
3. Process the left side:
    a. Check if there is an element to the left (`idx_2 > 0`) and if this element is '0' (fillable_space).
    b. If both conditions are true, scan leftwards from `idx_2 - 2` to find the index (`idx_left`) and value (`X_left`) of the first non-zero digit.
    c. If such a digit `X_left` is found and it's not '2', replace all elements in the range `[idx_left + 1, idx_2 - 1]` (inclusive) with `X_left`.
4. Process the right side:
    a. Check if there is an element to the right (`idx_2 < length - 1`) and if this element is '0'.
    b. If both conditions are true, scan rightwards from `idx_2 + 2` to find the index (`idx_right`) and value (`X_right`) of the first non-zero digit.
    c. If such a digit `X_right` is found and it's not '2', replace all elements in the range `[idx_2 + 1, idx_right - 1]` (inclusive) with `X_right`.
5. Return the modified sequence. The left and right side processing are independent.
"""

def _find_boundary_marker(sequence: np.ndarray, marker: int = 2) -> int:
    """Finds the index of the first occurrence of the marker in the sequence."""
    indices = np.where(sequence == marker)[0]
    return indices[0] if len(indices) > 0 else -1

def _find_nearest_non_zero_left(sequence: np.ndarray, start_scan_idx: int) -> tuple[int, int]:
    """
    Scans leftwards from start_scan_idx to find the index and value
    of the first non-zero digit encountered.
    Returns (-1, -1) if no non-zero digit is found.
    """
    for i in range(start_scan_idx, -1, -1):
        if sequence[i] != 0:
            return i, sequence[i] # index, value
    return -1, -1 # index, value

def _find_nearest_non_zero_right(sequence: np.ndarray, start_scan_idx: int) -> tuple[int, int]:
    """
    Scans rightwards from start_scan_idx to find the index and value
    of the first non-zero digit encountered.
    Returns (-1, -1) if no non-zero digit is found.
    """
    n = len(sequence)
    for i in range(start_scan_idx, n):
        if sequence[i] != 0:
            return i, sequence[i] # index, value
    return -1, -1 # index, value

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the refined transformation rule to the input NumPy array sequence.
    """
    # Create a modifiable copy
    output_sequence = np.copy(input_sequence)
    n = len(output_sequence)
    boundary_marker = 2
    fillable_space = 0

    # 1. Find the index of the boundary marker '2'
    idx_2 = _find_boundary_marker(output_sequence, boundary_marker)

    # 2. If '2' is not found, return the original sequence
    if idx_2 == -1:
        return output_sequence

    # 3. Process Left Side
    # 3a. Check adjacent left element
    if idx_2 > 0 and output_sequence[idx_2 - 1] == fillable_space:
        # 3b. Scan left for the first non-zero digit
        left_source_idx, left_source_value = _find_nearest_non_zero_left(output_sequence, idx_2 - 2)

        # 3c. If a non-zero source is found and it's not the boundary marker itself
        if left_source_idx != -1 and left_source_value != boundary_marker:
            # Fill the region between the source and the boundary marker
            fill_start_left = left_source_idx + 1
            fill_end_left = idx_2 # Slice goes up to, but not including, idx_2
            if fill_start_left < fill_end_left:
                output_sequence[fill_start_left:fill_end_left] = left_source_value

    # 4. Process Right Side
    # 4a. Check adjacent right element
    if idx_2 < n - 1 and output_sequence[idx_2 + 1] == fillable_space:
        # 4b. Scan right for the first non-zero digit
        right_source_idx, right_source_value = _find_nearest_non_zero_right(output_sequence, idx_2 + 2)

        # 4c. If a non-zero source is found and it's not the boundary marker itself
        if right_source_idx != -1 and right_source_value != boundary_marker:
            # Fill the region between the boundary marker and the source
            fill_start_right = idx_2 + 1
            fill_end_right = right_source_idx # Slice goes up to, but not including, idx_right
            if fill_start_right < fill_end_right:
                output_sequence[fill_start_right:fill_end_right] = right_source_value

    # 5. Return the modified sequence
    return output_sequence
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 3 3 3 3 2 0 0 0
```
Expected Output:
```
0 0 0 0 3 3 3 3 2 0 0 0
```
Transformed Output:
```
0 0 0 0 3 3 3 3 2 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
2 0 0 0 7 7 7 7 7 0 0 0
```
Expected Output:
```
2 7 7 7 7 7 7 7 7 0 0 0
```
Transformed Output:
```
2 0 0 0 7 7 7 7 7 0 0 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0

## Example 3:
Input:
```
0 0 0 0 0 0 0 6 6 6 0 2
```
Expected Output:
```
0 0 0 0 0 0 0 6 6 6 6 2
```
Transformed Output:
```
0 0 0 0 0 0 0 6 6 6 0 2
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.666666666666686

## Example 4:
Input:
```
8 8 8 2 0 0 0 0 0 0 0 0
```
Expected Output:
```
8 8 8 2 0 0 0 0 0 0 0 0
```
Transformed Output:
```
8 8 8 2 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 5:
Input:
```
0 0 0 2 0 0 0 7 7 7 7 7
```
Expected Output:
```
0 0 0 2 7 7 7 7 7 7 7 7
```
Transformed Output:
```
0 0 0 2 0 0 0 7 7 7 7 7
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0

## Example 6:
Input:
```
0 0 0 4 4 4 4 0 0 0 2 0
```
Expected Output:
```
0 0 0 4 4 4 4 4 4 4 2 0
```
Transformed Output:
```
0 0 0 4 4 4 4 0 0 0 2 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0

## Example 7:
Input:
```
3 3 3 3 3 3 3 3 3 0 2 0
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 2 0
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 0 2 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.666666666666686

Test Set Results:

## Example 1:
Input:
```
2 8 8 8 8 0 0 0 0 0 0 0
```
Expected Output:
```
2 8 8 8 8 0 0 0 0 0 0 0
```
Transformed Output:
```
2 8 8 8 8 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
**General Assessment and Strategy**

The initial code (`code_00.py`) failed on 5 out of 7 training examples and 0 out of 1 test example provided (implicitly, as test results weren't shown for failed train cases, but the logic is consistent). The successful examples (train_1, train_4, test_1) were those where no filling operation was required around the '2'. The failures occurred specifically when sequences of '0's adjacent to the '2' *should* have been filled by a nearby non-zero, non-'2' digit.

The core issue in the failed code was an incorrect condition or procedure for identifying the fill region and the source value. The analysis revealed that the correct logic requires:
1.  Identifying the boundary marker '2'.
2.  Checking the *immediately adjacent* cell (left or right).
3.  If the adjacent cell is '0' (fillable space), then scanning outwards (away from '2') to find the *nearest* non-zero digit (source digit), provided it's not '2'.
4.  If such a source digit is found, filling the *entire* range of cells between the source digit's position (exclusive) and the '2' (exclusive) with the source digit's value.

The strategy is to refine the natural language program to precisely reflect this sequence of checks and actions, ensuring clarity on the role of the adjacent '0' and the extent of the fill operation. The YAML facts will be updated to better define the relationships and actions involved in this refined logic.

**Metrics**

The following metrics were gathered for the examples where `code_00.py` failed, confirming the specific locations and expected values for the required filling:



*code_execution:*
```python
import numpy as np

def analyze_sequence(input_str, expected_str, actual_str):
    inp = np.array([int(x) for x in input_str.split()])
    exp = np.array([int(x) for x in expected_str.split()])
    act = np.array([int(x) for x in actual_str.split()])
    n = len(inp)
    idx_2 = np.where(inp == 2)[0]
    idx_2 = idx_2[0] if len(idx_2) > 0 else -1

    report = {
        "input": input_str,
        "expected_output": expected_str,
        "actual_output": actual_str,
        "index_of_2": idx_2,
        "mismatch_indices": [],
        "expected_fill_left": None,
        "expected_fill_right": None
    }

    if idx_2 != -1:
        # Left side analysis
        if idx_2 > 0 and inp[idx_2 - 1] == 0:
            source_idx_left = -1
            source_val_left = -1
            for i in range(idx_2 - 2, -1, -1):
                if inp[i] != 0:
                    source_idx_left = i
                    source_val_left = inp[i]
                    break
            if source_idx_left != -1 and source_val_left != 2:
                 report["expected_fill_left"] = {
                     "value": source_val_left,
                     "source_index": source_idx_left,
                     "fill_indices": list(range(source_idx_left + 1, idx_2))
                 }

        # Right side analysis
        if idx_2 < n - 1 and inp[idx_2 + 1] == 0:
            source_idx_right = -1
            source_val_right = -1
            for i in range(idx_2 + 2, n):
                if inp[i] != 0:
                    source_idx_right = i
                    source_val_right = inp[i]
                    break
            if source_idx_right != -1 and source_val_right != 2:
                 report["expected_fill_right"] = {
                     "value": source_val_right,
                     "source_index": source_idx_right,
                     "fill_indices": list(range(idx_2 + 1, source_idx_right))
                 }

    diff_indices = np.where(exp != act)[0]
    report["mismatch_indices"] = list(diff_indices)

    return report

failed_examples = [
    ("2 0 0 0 7 7 7 7 7 0 0 0", "2 7 7 7 7 7 7 7 7 0 0 0", "2 0 0 0 7 7 7 7 7 0 0 0"),
    ("0 0 0 0 0 0 0 6 6 6 0 2", "0 0 0 0 0 0 0 6 6 6 6 2", "0 0 0 0 0 0 0 6 6 6 0 2"),
    ("0 0 0 2 0 0 0 7 7 7 7 7", "0 0 0 2 7 7 7 7 7 7 7 7", "0 0 0 2 0 0 0 7 7 7 7 7"),
    ("0 0 0 4 4 4 4 0 0 0 2 0", "0 0 0 4 4 4 4 4 4 4 2 0", "0 0 0 4 4 4 4 0 0 0 2 0"),
    ("3 3 3 3 3 3 3 3 3 0 2 0", "3 3 3 3 3 3 3 3 3 3 2 0", "3 3 3 3 3 3 3 3 3 0 2 0"),
]

analysis_results = [analyze_sequence(*ex) for ex in failed_examples]

# Print a summary
for i, result in enumerate(analysis_results):
    print(f"--- Analysis Example {i+1} ---")
    print(f"Input:           {result['input']}")
    print(f"Expected:        {result['expected_output']}")
    print(f"Actual (Code00): {result['actual_output']}")
    print(f"Index of 2:      {result['index_of_2']}")
    print(f"Mismatch Idx:    {result['mismatch_indices']}")
    print(f"Exp. Fill Left:  {result['expected_fill_left']}")
    print(f"Exp. Fill Right: {result['expected_fill_right']}")
    print("-" * 20)

# Aggregate Mismatch Count
total_mismatches = sum(len(r['mismatch_indices']) for r in analysis_results)
print(f"\nTotal Mismatched Cells Across Failed Examples: {total_mismatches}")

# Verification of successful examples (no fill expected)
success_examples = [
    ("0 0 0 0 3 3 3 3 2 0 0 0", "0 0 0 0 3 3 3 3 2 0 0 0", "0 0 0 0 3 3 3 3 2 0 0 0"),
    ("8 8 8 2 0 0 0 0 0 0 0 0", "8 8 8 2 0 0 0 0 0 0 0 0", "8 8 8 2 0 0 0 0 0 0 0 0"),
    # Test Example 1 (assuming previous success was correct)
    ("2 8 8 8 8 0 0 0 0 0 0 0", "2 8 8 8 8 0 0 0 0 0 0 0", "2 8 8 8 8 0 0 0 0 0 0 0"),
]

success_analysis = [analyze_sequence(*ex) for ex in success_examples]

for i, result in enumerate(success_analysis):
    print(f"--- Analysis Success Example {i+1} ---")
    print(f"Input:           {result['input']}")
    print(f"Index of 2:      {result['index_of_2']}")
    print(f"Mismatch Idx:    {result['mismatch_indices']}")
    print(f"Exp. Fill Left:  {result['expected_fill_left']}")
    print(f"Exp. Fill Right: {result['expected_fill_right']}")
    print("-" * 20)

all_fills_expected_none = all(r['expected_fill_left'] is None and r['expected_fill_right'] is None for r in success_analysis)
print(f"\nAll Successful Examples Correctly Had No Expected Fills: {all_fills_expected_none}")

```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Analysis Example 1 ---
Input:           2 0 0 0 7 7 7 7 7 0 0 0
Expected:        2 7 7 7 7 7 7 7 7 0 0 0
Actual (Code00): 2 0 0 0 7 7 7 7 7 0 0 0
Index of 2:      0
Mismatch Idx:    [np.int64(1), np.int64(2), np.int64(3)]
Exp. Fill Left:  None
Exp. Fill Right: {'value': np.int64(7), 'source_index': 4, 'fill_indices': [1, 2, 3]}
--------------------
--- Analysis Example 2 ---
Input:           0 0 0 0 0 0 0 6 6 6 0 2
Expected:        0 0 0 0 0 0 0 6 6 6 6 2
Actual (Code00): 0 0 0 0 0 0 0 6 6 6 0 2
Index of 2:      11
Mismatch Idx:    [np.int64(10)]
Exp. Fill Left:  {'value': np.int64(6), 'source_index': 9, 'fill_indices': [10]}
Exp. Fill Right: None
--------------------
--- Analysis Example 3 ---
Input:           0 0 0 2 0 0 0 7 7 7 7 7
Expected:        0 0 0 2 7 7 7 7 7 7 7 7
Actual (Code00): 0 0 0 2 0 0 0 7 7 7 7 7
Index of 2:      3
Mismatch Idx:    [np.int64(4), np.int64(5), np.int64(6)]
Exp. Fill Left:  None
Exp. Fill Right: {'value': np.int64(7), 'source_index': 7, 'fill_indices': [4, 5, 6]}
--------------------
--- Analysis Example 4 ---
Input:           0 0 0 4 4 4 4 0 0 0 2 0
Expected:        0 0 0 4 4 4 4 4 4 4 2 0
Actual (Code00): 0 0 0 4 4 4 4 0 0 0 2 0
Index of 2:      10
Mismatch Idx:    [np.int64(7), np.int64(8), np.int64(9)]
Exp. Fill Left:  {'value': np.int64(4), 'source_index': 6, 'fill_indices': [7, 8, 9]}
Exp. Fill Right: None
--------------------
--- Analysis Example 5 ---
Input:           3 3 3 3 3 3 3 3 3 0 2 0
Expected:        3 3 3 3 3 3 3 3 3 3 2 0
Actual (Code00): 3 3 3 3 3 3 3 3 3 0 2 0
Index of 2:      10
Mismatch Idx:    [np.int64(9)]
Exp. Fill Left:  {'value': np.int64(3), 'source_index': 8, 'fill_indices': [9]}
Exp. Fill Right: None
--------------------

Total Mismatched Cells Across Failed Examples: 11
--- Analysis Success Example 1 ---
Input:           0 0 0 0 3 3 3 3 2 0 0 0
Index of 2:      8
Mismatch Idx:    []
Exp. Fill Left:  None
Exp. Fill Right: None
--------------------
--- Analysis Success Example 2 ---
Input:           8 8 8 2 0 0 0 0 0 0 0 0
Index of 2:      3
Mismatch Idx:    []
Exp. Fill Left:  None
Exp. Fill Right: None
--------------------
--- Analysis Success Example 3 ---
Input:           2 8 8 8 8 0 0 0 0 0 0 0
Index of 2:      0
Mismatch Idx:    []
Exp. Fill Left:  None
Exp. Fill Right: None
--------------------

All Successful Examples Correctly Had No Expected Fills: True

```
**Facts (YAML)**


```yaml
objects:
  - sequence: A list or array of single-digit integers.
  - boundary_marker: The integer 2, acting as a reference point.
  - fillable_space: The integer 0, representing cells that can potentially be filled.
  - source_digit: An integer X, where X is not 0 and X is not 2. This digit provides the value for filling.

properties:
  - sequence: has ordered elements with indices.
  - boundary_marker: has a specific index (`idx_2`) within the sequence. Can occur at most once (based on examples).
  - fillable_space: Defined by the value 0.
  - source_digit: Defined by values other than 0 and 2.

actions:
  - find_boundary: Locate the index `idx_2` of the `boundary_marker` (2).
  - check_adjacency: Examine the element immediately to the left (`idx_2 - 1`) and right (`idx_2 + 1`) of the `boundary_marker`.
  - scan_outwards_left: If the left adjacent cell is `fillable_space` (0), search leftwards starting from `idx_2 - 2` to find the first `source_digit`.
  - scan_outwards_right: If the right adjacent cell is `fillable_space` (0), search rightwards starting from `idx_2 + 2` to find the first `source_digit`.
  - fill_region_left: If a `source_digit` is found to the left (at `idx_left`), replace all elements from `idx_left + 1` up to `idx_2 - 1` (inclusive) with the `source_digit` value.
  - fill_region_right: If a `source_digit` is found to the right (at `idx_right`), replace all elements from `idx_2 + 1` up to `idx_right - 1` (inclusive) with the `source_digit` value.

relationships:
  - Filling occurs *only* if the cell immediately adjacent (left or right) to the `boundary_marker` (2) is a `fillable_space` (0).
  - The value used for filling (`source_digit`) is determined by the *first* non-zero, non-`boundary_marker` digit encountered when scanning outwards from the `boundary_marker` *past* the adjacent `fillable_space`.
  - The fill operation replaces *all* cells between the identified `source_digit` and the `boundary_marker`.
  - Left and right side filling operations are independent.
```


**Natural Language Program**

1.  Read the input sequence of digits. Create a modifiable copy.
2.  Find the index (`idx_2`) of the `boundary_marker` (the digit '2'). If '2' is not present, return the original sequence unchanged.
3.  **Process Left Side:**
    a.  Check if an element exists immediately to the left of `idx_2` (i.e., `idx_2 > 0`).
    b.  If it exists, check if this adjacent left element (at `idx_2 - 1`) is a `fillable_space` (the digit '0').
    c.  If both conditions (a and b) are true, then scan leftwards starting from index `idx_2 - 2` down to index 0. Find the index (`idx_left`) and value (`value_left`) of the *first* digit encountered that is not '0'.
    d.  If such a digit is found (`idx_left` is valid) *and* its value (`value_left`) is not the `boundary_marker` ('2'), then replace all elements in the sequence copy from index `idx_left + 1` up to (and including) index `idx_2 - 1` with `value_left`.
4.  **Process Right Side:**
    a.  Check if an element exists immediately to the right of `idx_2` (i.e., `idx_2 < length - 1`).
    b.  If it exists, check if this adjacent right element (at `idx_2 + 1`) is a `fillable_space` (the digit '0').
    c.  If both conditions (a and b) are true, then scan rightwards starting from index `idx_2 + 2` up to the end of the sequence. Find the index (`idx_right`) and value (`value_right`) of the *first* digit encountered that is not '0'.
    d.  If such a digit is found (`idx_right` is valid) *and* its value (`value_right`) is not the `boundary_marker` ('2'), then replace all elements in the sequence copy from index `idx_2 + 1` up to (and including) index `idx_right - 1` with `value_right`.
5.  Return the modified sequence.
