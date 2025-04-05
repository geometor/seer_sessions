
## train_1

**input:**
```
0 0 4 4 7 7 9 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 4 7 7 9 7
```


## train_2

**input:**
```
0 1 6 4 8 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 6 4 8 2 0 0
```


## train_3

**input:**
```
0 0 0 0 3 6 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 6 8 0
```


## train_4

**input:**
```
0 0 0 0 0 2 9 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 9 0
```


## train_5

**input:**
```
2 7 1 9 9 5 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 7 1 9 9 5 5 0
```


## train_6

**input:**
```
0 0 0 0 3 1 9 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 1 9 0
```


## train_7

**input:**
```
1 3 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 3 4 0 0 0 0 0
```

*   **Perception:** The task involves processing fixed-length sequences of 12 digits. Each input sequence appears to contain a contiguous block defined by the first and last non-zero digits. This block (including any zeros it might contain internally) is shifted 4 positions to the right within the 12-digit frame to produce the output. The positions outside the shifted block in the output are filled with zeros.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - item: input_sequence
        properties:
          - type: list of integers
          - length: 12
          - content: digits (0-9) separated by spaces in string format
      - item: output_sequence
        properties:
          - type: list of integers
          - length: 12
          - content: digits (0-9) separated by spaces in string format
      - item: non_zero_segment
        properties:
          - definition: The sub-sequence starting from the first non-zero digit and ending with the last non-zero digit in the input sequence.
          - may_contain_zeros: true
      - item: shift_operation
        properties:
          - type: right shift
          - amount: 4 positions
          - target: non_zero_segment
      - item: zero_padding
        properties:
          - description: Positions in the output sequence not occupied by the shifted segment are filled with zeros.
          - handling_boundaries: Elements shifted beyond the 12th position are truncated/discarded.
    relationships:
      - input_sequence is transformed into output_sequence by identifying the non_zero_segment, applying the shift_operation, and using zero_padding.
      - If input_sequence contains only zeros, the non_zero_segment is empty, and the output_sequence is identical to the input_sequence.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of 12 integers.
    2.  Identify the index of the first non-zero element (`first_nz`) and the index of the last non-zero element (`last_nz`) in the input list.
    3.  If no non-zero elements are found (i.e., the list contains only zeros), return the original input string.
    4.  Extract the sub-list (segment) from the input list starting at index `first_nz` and ending at index `last_nz` (inclusive).
    5.  Create a new list of 12 zeros, representing the initial state of the output list.
    6.  Calculate the starting index for placing the extracted segment in the output list: `target_start = first_nz + 4`.
    7.  Iterate through the extracted segment. For each element in the segment, calculate its target index in the output list by adding its position relative to the start of the segment to `target_start`.
    8.  If the calculated target index is within the bounds of the output list (0 to 11), place the element at that index in the output list. Otherwise, discard the element (truncation).
    9.  Convert the resulting output list back into a space-separated string of digits.
    10. Return the formatted output string.
```python
import math
import numpy as np # Common library, might be useful though not strictly necessary for this specific logic.

"""
Transforms a sequence of 12 digits by identifying the segment between the first and last non-zero digits (inclusive) and shifting this segment 4 positions to the right within the 12-digit sequence. Positions outside the shifted segment are filled with zeros. If the input sequence contains only zeros, it is returned unchanged.
"""

def _parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def _find_non_zero_indices(int_list: list[int]) -> tuple[int | None, int | None]:
    """
    Finds the index of the first and last non-zero elements.
    Returns (None, None) if no non-zero elements are found.
    """
    first_nz = -1
    last_nz = -1
    for i, digit in enumerate(int_list):
        if digit != 0:
            if first_nz == -1:
                first_nz = i
            last_nz = i
    # Handle case where all elements are zero
    if first_nz == -1:
        return None, None
    return first_nz, last_nz

def _format_output(int_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, int_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Workflow:
    1. Parse the input string into a list of integers.
    2. Identify the first and last non-zero element indices ('first_nz', 'last_nz').
    3. If all elements are zero (first_nz is None), return the original input string.
    4. Extract the segment of the input list from first_nz to last_nz (inclusive).
    5. Initialize an output list of the same length (12) with all zeros.
    6. Calculate the target start index for placing the segment in the output list (first_nz + 4).
    7. Iterate through the extracted segment. For each element and its index 'i' within the segment:
       a. Calculate the corresponding target index in the output list: target_start_index + i.
       b. If the target index is within the bounds of the output list (0 to 11), place the element at that index.
       c. Otherwise (if target index >= 12), the element is shifted out of bounds and ignored (truncated).
    8. Format the resulting output list back into a space-separated string.
    9. Return the formatted output string.
    """
    # Step 1: Parse the input string
    input_list = _parse_input(input_str)
    list_length = 12 # Assuming fixed length based on examples

    # Step 2: Identify the first and last non-zero element indices
    first_nz, last_nz = _find_non_zero_indices(input_list)

    # Step 3: Handle the all-zeros case
    if first_nz is None:
        return input_str # Return original string if no non-zeros found

    # Step 4: Extract the non-zero segment
    # The segment includes elements from first_nz up to and including last_nz
    segment = input_list[first_nz : last_nz + 1]

    # Step 5: Initialize the output list with zeros
    output_list = [0] * list_length

    # Step 6: Calculate the target start position for the shift
    shift_amount = 4
    target_start_index = first_nz + shift_amount

    # Step 7: Place the segment into the output list at the shifted position
    for i, digit in enumerate(segment):
        target_index = target_start_index + i
        # Check bounds: Only place if the target index is within the list length
        if 0 <= target_index < list_length:
            output_list[target_index] = digit
        # Elements shifted beyond the end are implicitly truncated

    # Step 8 & 9: Format the output list back to a string and return
    output_str = _format_output(output_list)
    return output_str
```
