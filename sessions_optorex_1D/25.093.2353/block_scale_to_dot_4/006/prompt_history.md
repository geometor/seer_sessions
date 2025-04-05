
## train_1

**input:**
```
0 0 8 8 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 8 2 0 0 0 0 0
```


## train_2

**input:**
```
0 0 2 1 1 1 1 0 0 0 0 0
```


**output:**
```
0 0 2 1 1 1 1 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 0 0 0 0 0 0 0 2 0
```


**output:**
```
0 1 1 1 1 1 1 1 1 1 2 0
```


## train_4

**input:**
```
2 0 0 0 0 0 0 0 8 8 8 8
```


**output:**
```
2 8 8 8 8 8 8 8 8 8 8 8
```


## train_5

**input:**
```
0 0 0 0 0 8 8 8 8 0 0 2
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 8 2
```


## train_6

**input:**
```
0 0 0 1 1 1 1 1 1 2 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 2 0 0
```


## train_7

**input:**
```
0 0 0 0 2 4 4 4 4 4 4 4
```


**output:**
```
0 0 0 0 2 4 4 4 4 4 4 4
```

*   **Perception:** The task involves transforming a sequence of single-digit integers. The core operation seems to be filling sequences of zeros based on the proximity of a non-zero number to the number `2`. The number `2` acts as a central point or boundary. Zeros located between the number `2` and the nearest non-zero number (either to the left or right) are replaced by that non-zero number. If `2` is adjacent to a non-zero number, or if there are only zeros on one side extending to the end of the sequence, no filling occurs in that direction.

*   **Facts:**
    
```yaml
    task_elements:
      - object: input_sequence
        description: A list of single-digit integers.
      - object: output_sequence
        description: The transformed list of single-digit integers.
      - object: marker_element
        value: 2
        description: Acts as a central reference point for the transformation.
      - object: fill_element
        description: A non-zero integer in the sequence adjacent (or nearest across zeros) to the marker_element.
      - object: zero_element
        value: 0
        description: Elements that are potentially replaced.
      - object: sequence_segment
        description: A contiguous sub-sequence of zeros located between the marker_element (2) and the nearest non-zero element.
    actions:
      - action: locate
        actor: system
        target: marker_element (2)
        result: index of the marker_element
      - action: scan_left
        actor: system
        origin: index of marker_element
        target: first non-zero element encountered
        result: value and index of the left-side non-zero element (if any)
      - action: scan_right
        actor: system
        origin: index of marker_element
        target: first non-zero element encountered
        result: value and index of the right-side non-zero element (if any)
      - action: fill
        actor: system
        target: zero_elements within the identified sequence_segment
        value: value of the corresponding fill_element (left or right)
        condition: A non-zero element is found on that side, and there are zeros between it and the marker_element.
    relationships:
      - type: position
        between: marker_element, fill_element, zero_element
        description: Defines which zeros are candidates for filling based on their location relative to '2' and the nearest non-zero neighbours.
    ```


*   **Natural Language Program:**
    1.  Find the index of the number `2` in the input sequence. If `2` is not present, return the input sequence unchanged.
    2.  Initialize the output sequence as a copy of the input sequence.
    3.  **Left Fill:** Iterate leftwards from the index immediately preceding `2` down to the beginning of the sequence.
        a.  If a non-zero number `L` is encountered at index `idx_L`:
            i.  Iterate from `idx_L + 1` up to (but not including) the index of `2`.
            ii. For each element in this range, if its value is `0`, change its value in the output sequence to `L`.
            iii. Stop the leftward scan.
    4.  **Right Fill:** Iterate rightwards from the index immediately following `2` up to the end of the sequence.
        a.  If a non-zero number `R` is encountered at index `idx_R`:
            i.  Iterate from the index immediately following `2` up to (but not including) `idx_R`.
            ii. For each element in this range, if its value is `0`, change its value in the output sequence to `R`.
            iii. Stop the rightward scan.
    5.  Return the modified output sequence.
```python
import math
import numpy as np

"""
Transforms a sequence of single-digit integers represented as a space-separated string. 
The transformation involves finding the number '2' in the sequence. Zeros located 
between the '2' and the nearest non-zero number to its left are replaced by that 
left non-zero number. Similarly, zeros located between the '2' and the nearest 
non-zero number to its right are replaced by that right non-zero number. If '2' 
is not found, or if there are no non-zero numbers on one side, or if the non-zero 
number is adjacent to '2', no filling occurs on that side.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(x) for x in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Converts a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the fill transformation based on the position of '2'.

    Args:
        input_str: A string representing the input sequence, with digits separated by spaces.

    Returns:
        A string representing the transformed sequence, with digits separated by spaces.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)
    
    # Initialize the output list as a copy of the input list
    output_list = list(input_list)
    n = len(output_list)
    
    # Try to find the index of the number 2
    try:
        index_of_2 = input_list.index(2)
    except ValueError:
        # If 2 is not present, return the original sequence unchanged
        return input_str

    # --- Left Fill ---
    # Iterate leftwards from the index immediately preceding 2
    left_fill_value = -1  # Sentinel value indicating no non-zero found yet
    left_fill_index = -1
    for i in range(index_of_2 - 1, -1, -1):
        if output_list[i] != 0:
            # Found the nearest non-zero number to the left
            left_fill_value = output_list[i]
            left_fill_index = i
            break # Stop the leftward scan

    # If a non-zero number was found to the left and it's not adjacent to 2
    if left_fill_value != -1 and left_fill_index < index_of_2 - 1:
        # Iterate from the non-zero number's position + 1 up to 2's position
        for i in range(left_fill_index + 1, index_of_2):
            # If the element is 0, fill it with the left_fill_value
            if output_list[i] == 0:
                output_list[i] = left_fill_value

    # --- Right Fill ---
    # Iterate rightwards from the index immediately following 2
    right_fill_value = -1 # Sentinel value
    right_fill_index = -1
    for i in range(index_of_2 + 1, n):
        if output_list[i] != 0:
            # Found the nearest non-zero number to the right
            right_fill_value = output_list[i]
            right_fill_index = i
            break # Stop the rightward scan

    # If a non-zero number was found to the right and it's not adjacent to 2
    if right_fill_value != -1 and right_fill_index > index_of_2 + 1:
        # Iterate from 2's position + 1 up to the non-zero number's position
        for i in range(index_of_2 + 1, right_fill_index):
             # If the element is 0, fill it with the right_fill_value
            if output_list[i] == 0:
                output_list[i] = right_fill_value

    # Format the output list back into a space-separated string
    return format_output(output_list)

```
```python
import math # Although not strictly needed for this logic, kept as per template suggestion
from typing import List, Optional, Tuple

"""
Transforms a sequence (list) of single-digit integers. The transformation hinges on 
the location of the integer 2. If 2 is present, the algorithm scans left and right 
for the *first* non-zero integer encountered. All zero elements situated strictly 
*between* the 2 and the found non-zero element are replaced with the value of that 
non-zero element, provided the non-zero element is not immediately adjacent to the 2. 
If 2 is not present, or if no non-zero element exists to the left/right, or if the 
nearest non-zero element is immediately adjacent to 2, no filling occurs on that side. 
The function accepts a list of integers and returns the transformed list of integers.
"""

def _find_first_occurrence(data: List[int], value: int) -> Optional[int]:
    """Finds the index of the first occurrence of a value in a list."""
    try:
        return data.index(value)
    except ValueError:
        return None

def _scan_and_find_non_zero(data: List[int], start_index: int, end_index: int, step: int) -> Optional[Tuple[int, int]]:
    """
    Scans a portion of the list for the first non-zero element.

    Args:
        data: The list to scan.
        start_index: The starting index for the scan (inclusive).
        end_index: The ending index for the scan (exclusive).
        step: The step direction (-1 for left, 1 for right).

    Returns:
        A tuple (value, index) of the first non-zero element found, or None.
    """
    for i in range(start_index, end_index, step):
        if data[i] != 0:
            return data[i], i
    return None

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the fill transformation based on the position of '2'.

    Args:
        input_list: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Initialize the output list as a copy of the input list
    output_list = list(input_list)
    n = len(output_list)

    # 1. Find the index of the number 2
    index_of_2 = _find_first_occurrence(input_list, 2)

    # 2. If 2 is not present, return the original sequence unchanged
    if index_of_2 is None:
        return output_list

    # 3. Left Fill Scan & Fill
    # Scan leftwards from the index immediately preceding 2
    left_scan_result = _scan_and_find_non_zero(input_list, index_of_2 - 1, -1, -1)
    if left_scan_result is not None:
        left_fill_value, left_fill_index = left_scan_result
        # Check if the found non-zero is not adjacent to 2
        if left_fill_index < index_of_2 - 1:
            # Iterate from the non-zero number's position + 1 up to 2's position
            for i in range(left_fill_index + 1, index_of_2):
                 # If the element is 0 (safety check, though implied by logic), fill it
                if output_list[i] == 0:
                    output_list[i] = left_fill_value

    # 4. Right Fill Scan & Fill
    # Scan rightwards from the index immediately following 2
    right_scan_result = _scan_and_find_non_zero(input_list, index_of_2 + 1, n, 1)
    if right_scan_result is not None:
        right_fill_value, right_fill_index = right_scan_result
        # Check if the found non-zero is not adjacent to 2
        if right_fill_index > index_of_2 + 1:
            # Iterate from 2's position + 1 up to the non-zero number's position
            for i in range(index_of_2 + 1, right_fill_index):
                 # If the element is 0 (safety check), fill it
                if output_list[i] == 0:
                    output_list[i] = right_fill_value

    # 5. Return the modified output list
    return output_list
```
```python
import numpy as np
from typing import Optional, Tuple

"""
Transforms a 1D NumPy array of single-digit integers. The transformation hinges on 
the location of the integer 2. If 2 is present, the algorithm scans left and right 
from the position of 2 for the *first* non-zero integer encountered. All zero elements 
situated strictly *between* the 2 and the found non-zero element are replaced with 
the value of that non-zero element, but only if the non-zero element is not 
immediately adjacent to the 2. If 2 is not present, or if no non-zero element 
exists to the left/right, or if the nearest non-zero element is immediately 
adjacent to 2, no filling occurs on that side.
"""

def _find_first_occurrence_np(data: np.ndarray, value: int) -> Optional[int]:
    """Finds the index of the first occurrence of a value in a NumPy array."""
    indices = np.where(data == value)[0]
    if indices.size > 0:
        return indices[0]
    else:
        return None

def _scan_and_find_non_zero_np(data: np.ndarray, start_index: int, end_index: int, step: int) -> Optional[Tuple[int, int]]:
    """
    Scans a portion of the NumPy array for the first non-zero element.

    Args:
        data: The NumPy array to scan.
        start_index: The starting index for the scan (inclusive).
        end_index: The ending index for the scan (exclusive for step=1, inclusive for step=-1). 
                   Note: range needs careful handling for numpy.
        step: The step direction (-1 for left, 1 for right).

    Returns:
        A tuple (value, index) of the first non-zero element found, or None.
    """
    if step == 1:
        # Scan right: start_index to end_index (exclusive)
        indices = np.arange(start_index, end_index)
    elif step == -1:
        # Scan left: start_index down to end_index (inclusive)
        # We want to check indices from start_index down to 0 if end_index is -1
        actual_end = end_index # should be -1 for full left scan
        indices = np.arange(start_index, actual_end, step) 
    else:
        return None # Should not happen

    for i in indices:
        # Check bounds explicitly for safety, although range should handle it
        if 0 <= i < len(data): 
            if data[i] != 0:
                return data[i], i
    return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the fill transformation based on the position of '2'.

    Args:
        input_grid: A 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    n = len(output_grid)

    # 1. Find the index of the number 2
    index_of_2 = _find_first_occurrence_np(input_grid, 2)

    # 2. If 2 is not present, return the original sequence unchanged
    if index_of_2 is None:
        return output_grid

    # 3. Left Fill Scan & Fill
    # Scan leftwards from the index immediately preceding 2 down to index 0
    left_scan_result = _scan_and_find_non_zero_np(input_grid, index_of_2 - 1, -1, -1)
    if left_scan_result is not None:
        left_fill_value, left_fill_index = left_scan_result
        # Check if the found non-zero is not adjacent to 2
        if left_fill_index < index_of_2 - 1:
            # Replace elements from non-zero index + 1 up to (but not including) 2's index
            # Only replace if the element is currently 0 (redundant check if logic correct, but safe)
            fill_slice = output_grid[left_fill_index + 1 : index_of_2]
            fill_slice[fill_slice == 0] = left_fill_value # Apply fill only to zeros in the slice


    # 4. Right Fill Scan & Fill
    # Scan rightwards from the index immediately following 2 up to the end
    right_scan_result = _scan_and_find_non_zero_np(input_grid, index_of_2 + 1, n, 1)
    if right_scan_result is not None:
        right_fill_value, right_fill_index = right_scan_result
        # Check if the found non-zero is not adjacent to 2
        if right_fill_index > index_of_2 + 1:
            # Replace elements from 2's index + 1 up to (but not including) non-zero index
            # Only replace if the element is currently 0
            fill_slice = output_grid[index_of_2 + 1 : right_fill_index]
            fill_slice[fill_slice == 0] = right_fill_value # Apply fill only to zeros in the slice


    # 5. Return the modified output grid
    return output_grid
```
