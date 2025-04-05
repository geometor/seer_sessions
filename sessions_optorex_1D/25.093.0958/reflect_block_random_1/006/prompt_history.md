
## train_1

**input:**
```
0 6 8 6 5 8 4 4 5 5 3 8
```


**output:**
```
0 8 3 5 5 4 4 8 5 6 8 6
```


## train_2

**input:**
```
0 7 1 4 1 1 6 3 1 9 3 0
```


**output:**
```
0 3 9 1 3 6 1 1 4 1 7 0
```


## train_3

**input:**
```
0 0 0 0 0 0 6 7 8 5 4 0
```


**output:**
```
0 0 0 0 0 0 4 5 8 7 6 0
```


## train_4

**input:**
```
0 0 0 0 8 3 8 9 9 3 6 0
```


**output:**
```
0 0 0 0 6 3 9 9 8 3 8 0
```


## train_5

**input:**
```
6 6 5 2 9 1 4 2 9 4 6 0
```


**output:**
```
6 4 9 2 4 1 9 2 5 6 6 0
```


## train_6

**input:**
```
0 0 0 0 1 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 7 1 0 0 0 0 0 0
```


## train_7

**input:**
```
6 8 2 1 8 5 5 0 0 0 0 0
```


**output:**
```
5 5 8 1 2 8 6 0 0 0 0 0
```

Okay, let's break down the transformation.

**Perception of Elements:**

*   The input and output are sequences of single digits.
*   The length of the sequence remains constant between input and output.
*   The core transformation involves reversing a part of the sequence.
*   Leading and trailing zeros in the input sequence appear to maintain their positions relative to the start and end of the sequence.
*   The segment of the sequence that lies *between* the contiguous block of leading zeros and the contiguous block of trailing zeros is reversed. If there are no leading or trailing zeros, the entire sequence (or the relevant part determined by the first/last non-zero element) is reversed.

**YAML Facts:**


```yaml
task_elements:
  - object: sequence
    properties:
      - type: list_of_integers
      - length: fixed (12 in examples)
      - contains: single digits (0-9)
  - object: leading_zeros
    properties:
      - type: sub-sequence
      - location: start_of_sequence
      - content: only_zeros
      - relationship: precedes the core_segment
  - object: trailing_zeros
    properties:
      - type: sub-sequence
      - location: end_of_sequence
      - content: only_zeros
      - relationship: follows the core_segment
  - object: core_segment
    properties:
      - type: sub-sequence
      - location: between leading_zeros and trailing_zeros
      - content: contains all non-zero digits and any zeros interspersed within them
      - bounds: starts at the first non-zero digit, ends at the last non-zero digit
      - relationship: is acted upon by the primary transformation
actions:
  - action: identify_boundaries
    inputs: input_sequence
    outputs:
      - index_first_non_zero
      - index_last_non_zero
    description: Find the start and end indices of the core_segment. Handle cases where the sequence might be all zeros.
  - action: segment_sequence
    inputs:
      - input_sequence
      - index_first_non_zero
      - index_last_non_zero
    outputs:
      - leading_zeros_segment
      - core_segment
      - trailing_zeros_segment
    description: Split the input sequence into three parts based on the identified boundaries.
  - action: reverse_segment
    inputs: core_segment
    outputs: reversed_core_segment
    description: Reverse the order of elements within the core_segment.
  - action: concatenate_segments
    inputs:
      - leading_zeros_segment
      - reversed_core_segment
      - trailing_zeros_segment
    outputs: output_sequence
    description: Combine the segments in order (leading, reversed core, trailing) to form the final output sequence.
relationships:
  - type: positional_invariance
    elements: [leading_zeros, trailing_zeros]
    description: The leading and trailing zero segments maintain their position and content in the output relative to the sequence boundaries.
  - type: transformation
    elements: [core_segment]
    action: reverse_segment
    description: The core_segment is the target of the reversal operation.
```


**Natural Language Program:**

1.  Receive the input sequence of digits.
2.  Identify the index of the first non-zero digit (`start_index`). If no non-zero digits exist, the sequence remains unchanged; return the original sequence.
3.  Identify the index of the last non-zero digit (`end_index`).
4.  Extract the sub-sequence from the beginning of the input up to (but not including) `start_index`. This is the `prefix` (leading zeros).
5.  Extract the sub-sequence from `start_index` up to and including `end_index`. This is the `middle` segment.
6.  Extract the sub-sequence from the element after `end_index` to the end of the input. This is the `suffix` (trailing zeros).
7.  Reverse the order of the elements within the `middle` segment.
8.  Construct the output sequence by concatenating the `prefix`, the reversed `middle` segment, and the `suffix` in that order.
9.  Return the constructed output sequence.
```python
import math

def find_first_non_zero_index(data_list):
    """Finds the index of the first non-zero element."""
    for i, val in enumerate(data_list):
        if val != 0:
            return i
    return -1 # Return -1 if all are zeros

def find_last_non_zero_index(data_list):
    """Finds the index of the last non-zero element."""
    for i in range(len(data_list) - 1, -1, -1):
        if data_list[i] != 0:
            return i
    return -1 # Return -1 if all are zeros

def transform(input_str: str) -> str:
    """
    Reverses the sub-sequence of digits located between the first and last
    non-zero digits in the input sequence, leaving any leading and trailing
    zeros in their original positions.

    1.  Parses the input string into a list of integers.
    2.  Finds the index of the first non-zero digit (`start_index`).
    3.  Finds the index of the last non-zero digit (`end_index`).
    4.  If no non-zero digits are found (all zeros), returns the original string.
    5.  Otherwise, extracts the prefix (leading zeros before `start_index`).
    6.  Extracts the middle segment (from `start_index` to `end_index`, inclusive).
    7.  Extracts the suffix (trailing zeros after `end_index`).
    8.  Reverses the middle segment.
    9.  Concatenates the prefix, reversed middle segment, and suffix.
    10. Formats the result back into a space-separated string.
    """
    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]

    # 2. Find the index of the first non-zero digit.
    start_index = find_first_non_zero_index(input_list)

    # 4. If no non-zero digits are found (all zeros), return the original string.
    if start_index == -1:
        return input_str

    # 3. Find the index of the last non-zero digit.
    end_index = find_last_non_zero_index(input_list)

    # 5. Extract the prefix (leading zeros before start_index).
    prefix = input_list[:start_index]

    # 6. Extract the middle segment (from start_index to end_index, inclusive).
    middle = input_list[start_index : end_index + 1]

    # 7. Extract the suffix (trailing zeros after end_index).
    suffix = input_list[end_index + 1:]

    # 8. Reverse the middle segment.
    reversed_middle = middle[::-1]

    # 9. Concatenate the prefix, reversed middle segment, and suffix.
    output_list = prefix + reversed_middle + suffix

    # 10. Format the result back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str

```
```python
import numpy as np
import math # Although not used in the final code, included as per template allowance

"""
Reverses the sub-sequence of digits located between the first and last
non-zero digits in the input sequence, leaving any leading and trailing
zeros in their original positions. If the sequence contains only zeros,
it remains unchanged.
"""

def _find_first_non_zero_index(data_list):
    """Finds the index of the first non-zero element."""
    for i, val in enumerate(data_list):
        if val != 0:
            return i
    return -1 # Return -1 if all are zeros or list is empty

def _find_last_non_zero_index(data_list):
    """Finds the index of the last non-zero element."""
    n = len(data_list)
    for i in range(n - 1, -1, -1):
        if data_list[i] != 0:
            return i
    return -1 # Return -1 if all are zeros or list is empty

def transform(input_data):
    """
    Applies the transformation rule to the input data.

    Args:
        input_data: A list or numpy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a list for consistent processing
    if isinstance(input_data, np.ndarray):
        input_list = input_data.tolist()
    else:
        # Assume it's already list-like or directly usable as a list
        input_list = list(input_data)

    # Handle empty list case
    if not input_list:
        return []

    # Find the index of the first non-zero digit.
    start_index = _find_first_non_zero_index(input_list)

    # If no non-zero digits are found (all zeros), return the original list.
    if start_index == -1:
        return input_list # Return a copy or the original list

    # Find the index of the last non-zero digit.
    # Since we know there's at least one non-zero digit, this will also find an index.
    end_index = _find_last_non_zero_index(input_list)

    # Extract the prefix (leading zeros before start_index).
    prefix = input_list[:start_index]

    # Extract the middle segment (from start_index to end_index, inclusive).
    middle = input_list[start_index : end_index + 1]

    # Extract the suffix (trailing zeros after end_index).
    suffix = input_list[end_index + 1:]

    # Reverse the middle segment.
    reversed_middle = middle[::-1]

    # Concatenate the prefix, reversed middle segment, and suffix.
    output_list = prefix + reversed_middle + suffix

    # Return the transformed list
    return output_list
```
```python
import numpy as np
import math # Although not used in the final code, included as per template allowance

"""
Reverses the sub-sequence of digits located between the first and last
non-zero digits in the input sequence, leaving any leading and trailing
zeros in their original positions. If the sequence contains only zeros,
it remains unchanged.
"""

def _find_first_non_zero_index(data_list):
    """
    Helper function to find the index of the first non-zero element in a list.
    Returns -1 if no non-zero element is found.
    """
    for i, val in enumerate(data_list):
        if val != 0:
            return i
    return -1 # Return -1 if all are zeros or list is empty

def _find_last_non_zero_index(data_list):
    """
    Helper function to find the index of the last non-zero element in a list.
    Returns -1 if no non-zero element is found.
    """
    n = len(data_list)
    for i in range(n - 1, -1, -1):
        if data_list[i] != 0:
            return i
    return -1 # Return -1 if all are zeros or list is empty

def transform(input_list):
    """
    Applies the transformation rule to the input list of integers.

    Args:
        input_list: A list of integers representing the sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a list for consistent processing (though the caller should provide a list)
    # This handles potential numpy array inputs if needed, converting them to lists.
    if isinstance(input_list, np.ndarray):
        work_list = input_list.tolist()
    else:
        # Create a copy to avoid modifying the original input list if it's mutable
        work_list = list(input_list)

    # Handle empty list case - return empty list
    if not work_list:
        return []

    # 1. Determine the index of the first non-zero element
    start_index = _find_first_non_zero_index(work_list)

    # 2. If no non-zero element is found (all zeros), return the original list unchanged.
    if start_index == -1:
        return work_list

    # 3. Determine the index of the last non-zero element.
    #    (We know at least one non-zero exists, so this will find an index >= start_index)
    end_index = _find_last_non_zero_index(work_list)

    # 4. Extract the prefix sub-sequence (leading zeros).
    prefix = work_list[:start_index]

    # 5. Extract the core sub-sequence (from first to last non-zero, inclusive).
    core = work_list[start_index : end_index + 1]

    # 6. Extract the suffix sub-sequence (trailing zeros).
    suffix = work_list[end_index + 1:]

    # 7. Reverse the order of the elements within the core sub-sequence.
    reversed_core = core[::-1]

    # 8. Construct the final output sequence by concatenating the parts.
    output_list = prefix + reversed_core + suffix

    # 9. Return the constructed output list.
    return output_list
```
