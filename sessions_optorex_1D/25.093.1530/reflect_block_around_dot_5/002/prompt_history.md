
## train_1

**input:**
```
0 0 0 0 2 0 0 0 6 0 0 0
```


**output:**
```
6 0 0 0 2 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 7 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 7 0
```


## train_3

**input:**
```
5 5 0 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 0 5 5 0 0 0 0 0
```


## train_4

**input:**
```
0 0 2 0 9 0 0 0 0 0 0 0
```


**output:**
```
9 0 2 0 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 3 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 0 0 3
```


## train_6

**input:**
```
0 0 4 4 4 4 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 4 4 4 4 0
```


## train_7

**input:**
```
0 0 0 8 8 8 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 8 8 8 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are single lists (or sequences) of integers.
2.  **Key Values:** The integers `0` and `2` appear frequently. Other non-zero integers (`3, 4, 5, 6, 7, 8, 9`) also appear.
3.  **Role of Zero:** Zeros seem to act as background or empty space.
4.  **Role of Two:** The number `2` appears exactly once in every input and output, and its index (position) remains the same from input to output. It seems to function as a fixed pivot or boundary marker.
5.  **Other Non-Zero Numbers (Payload):** Other non-zero numbers often appear in contiguous blocks of identical values (e.g., `5 5`, `4 4 4 4`, `8 8 8 8`). These blocks (or single non-zero numbers) seem to be the elements that are moved. Let's call these the "payload".
6.  **Transformation:** The core transformation involves moving the payload relative to the fixed position of the pivot `2`. The destination of the payload depends on whether it was originally located before or after the pivot `2`.

**YAML Fact Documentation:**


```yaml
Task: Move a block of numbers relative to a fixed pivot '2'.

Input:
  Type: List[int]
  Properties:
    - Contains zeros.
    - Contains exactly one '2' (the pivot).
    - Contains at least one other non-zero number (the payload).
    - Payloads can be single numbers or contiguous blocks of identical non-zero numbers.

Output:
  Type: List[int]
  Properties:
    - Same length as the input list.
    - Contains the same pivot '2' at the same index as in the input.
    - Contains the same payload numbers as in the input, but potentially at a different location.
    - Contains zeros filling the remaining positions.

Transformation:
  Action: Relocate the 'payload' block.
  Pivot: The number '2'. Its position remains fixed.
  Payload: The contiguous block of identical non-zero numbers other than '2'.
  Rule:
    Condition: Payload is originally located *before* the pivot '2'.
      Result: Payload is moved to the portion of the list *after* the pivot '2'. Its specific position preserves the number of zeros originally between the payload and the pivot.
    Condition: Payload is originally located *after* the pivot '2'.
      Result: Payload is moved to the beginning of the list (index 0).
  Relationships:
    - The position of '2' dictates the separation point for analyzing payload location.
    - The relative order (before/after '2') determines the destination region (after '2' / before '2').
    - Zeros act as spacers, and the number of zeros between payload and pivot (when payload is before pivot) influences the final placement.
```


**Natural Language Program:**

1.  Locate the index of the pivot element `2` in the input list.
2.  Identify the contiguous block of identical non-zero numbers that are not `2`; this is the payload. Note its value, starting index, and ending index.
3.  Create a new list of the same length as the input, filled entirely with zeros.
4.  Place the pivot element `2` into the new list at its original index.
5.  Compare the starting index of the payload with the index of the pivot `2`.
6.  If the payload's starting index is less than the pivot's index (payload was before the pivot):
    a.  Count the number of zeros in the input list strictly between the end of the payload block and the pivot `2`.
    b.  Calculate the target starting index in the new list for the payload: `pivot_index + 1 + count_of_intermediate_zeros`.
    c.  Place the payload block into the new list starting at this target index.
7.  If the payload's starting index is greater than the pivot's index (payload was after the pivot):
    a.  Place the payload block into the new list starting at index 0.
8.  Return the newly constructed list.
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms an input list of integers based on the following rules:
1.  Identifies a fixed 'pivot' element, which is the number 2. The pivot's position remains unchanged.
2.  Identifies a contiguous block of identical non-zero numbers other than 2, referred to as the 'payload'.
3.  Creates an output list of the same size, initially filled with zeros.
4.  Places the pivot '2' in the output list at its original index.
5.  Determines the new location for the 'payload' based on its original position relative to the pivot:
    a.  If the payload was originally *before* the pivot, it is moved to the section *after* the pivot. The number of zeros originally between the payload and the pivot is preserved as spacing after the pivot before the payload starts in the output.
    b.  If the payload was originally *after* the pivot, it is moved to the beginning of the output list (index 0).
6.  Fills the remaining positions in the output list with zeros.
"""

def find_pivot(grid: List[int]) -> Optional[int]:
    """Finds the index of the pivot element (2)."""
    try:
        return grid.index(2)
    except ValueError:
        return None # Should not happen based on problem description

def find_payload(grid: List[int], pivot_index: Optional[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the payload block (value, start_index, end_index_inclusive).
    Returns None if no payload is found (excluding the pivot).
    """
    payload_value = None
    payload_start_index = -1
    payload_end_index = -1

    for i, val in enumerate(grid):
        if val == 0 or (pivot_index is not None and i == pivot_index):
            # If we were tracking a payload, it ends here
            if payload_start_index != -1:
                payload_end_index = i - 1
                return payload_value, payload_start_index, payload_end_index
            continue # Skip zeros and pivot

        # Found a potential start of a payload
        if payload_start_index == -1:
            payload_value = val
            payload_start_index = i
        # If the current value is different from the start of the potential payload
        elif val != payload_value:
             # The previous block was the payload
             payload_end_index = i - 1
             return payload_value, payload_start_index, payload_end_index

    # If the loop finished and we were tracking a payload (it extends to the end)
    if payload_start_index != -1:
        payload_end_index = len(grid) - 1
        return payload_value, payload_start_index, payload_end_index

    return None # No payload found

def count_intermediate_zeros(grid: List[int], payload_end_index: int, pivot_index: int) -> int:
    """Counts zeros strictly between the end of the payload and the pivot."""
    count = 0
    # Ensure the range is valid and payload is before pivot
    if payload_end_index < pivot_index -1:
         for i in range(payload_end_index + 1, pivot_index):
              if grid[i] == 0:
                   count += 1
    return count

def transform(input_grid: List[int]) -> List[int]:
    """Applies the described transformation rule to the input list."""
    n = len(input_grid)
    # Initialize output_grid with zeros
    output_grid = [0] * n

    # 1. Locate the pivot index
    pivot_index = find_pivot(input_grid)
    if pivot_index is None:
        # Handle error or return input if pivot is missing (though problem implies it's always there)
        return input_grid # Or raise an error

    # 2. Place the pivot in the output grid
    output_grid[pivot_index] = 2

    # 3. Identify the payload
    payload_info = find_payload(input_grid, pivot_index)
    if payload_info is None:
        # Handle error or return grid if no payload found (problem implies payload exists)
        return output_grid # Pivot is placed, rest are zeros

    payload_value, payload_start_index, payload_end_index = payload_info
    payload_len = payload_end_index - payload_start_index + 1
    payload_block = [payload_value] * payload_len

    # 4. Determine payload placement based on relative position to pivot
    if payload_start_index < pivot_index:
        # Payload was before pivot
        # a. Count intermediate zeros
        intermediate_zeros = count_intermediate_zeros(input_grid, payload_end_index, pivot_index)
        # b. Calculate target start index
        target_start_index = pivot_index + 1 + intermediate_zeros
        # c. Place payload, ensuring it fits within bounds
        if target_start_index + payload_len <= n:
            output_grid[target_start_index : target_start_index + payload_len] = payload_block
        else:
            # Handle case where it might theoretically overflow (adjust logic if needed based on examples)
             # Place as much as possible if overflow happens (or error)
             place_len = n - target_start_index
             if place_len > 0:
                output_grid[target_start_index:] = payload_block[:place_len]


    else: # payload_start_index > pivot_index
        # Payload was after pivot
        # a. Place payload at the beginning
        if payload_len <= n:
             output_grid[0 : payload_len] = payload_block
        else:
             # Handle case where payload is longer than grid (place as much as possible)
             output_grid[0 : n] = payload_block[:n]


    return output_grid
```
