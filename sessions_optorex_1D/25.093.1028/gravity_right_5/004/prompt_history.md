
## train_1

**input:**
```
0 0 4 2 0 1 7 9 9 0 6 0
```


**output:**
```
0 0 0 0 0 4 2 1 7 9 9 6
```


## train_2

**input:**
```
4 0 0 8 2 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 4 8 2 2
```


## train_3

**input:**
```
6 0 8 0 0 0 0 6 0 2 7 0
```


**output:**
```
0 0 0 0 0 0 0 6 8 6 2 7
```


## train_4

**input:**
```
0 6 0 0 7 0 0 0 7 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 6 7 7 6
```


## train_5

**input:**
```
0 9 1 0 0 0 0 0 0 6 9 1
```


**output:**
```
0 0 0 0 0 0 0 9 1 6 9 1
```


## train_6

**input:**
```
0 4 6 4 0 0 5 2 3 0 0 2
```


**output:**
```
0 0 0 0 0 4 6 4 5 2 3 2
```


## train_7

**input:**
```
9 2 5 0 0 0 6 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 2 5 6 8
```

*   **Perception of Elements:**
    *   The input and output are sequences (strings) of space-separated single digits.
    *   Both input and output sequences have a fixed length (12 digits in the examples).
    *   The core elements are the individual digits within the sequence.
    *   Digits can be categorized into 'zero' and 'non-zero'.
    *   The transformation involves rearranging the digits based on whether they are zero or non-zero.

*   **YAML Facts:**
    
```yaml
    task_description: "Rearrange digits in a sequence, moving all zeros to the beginning while preserving the relative order of non-zero digits."
    input_format:
      type: string
      description: "A sequence of space-separated single digits."
      length: 12
      element_type: digit (0-9)
    output_format:
      type: string
      description: "A sequence of space-separated single digits, rearranged according to the rule."
      length: 12
      element_type: digit (0-9)
    transformation:
      action: partition
      elements: digits
      partition_key: "is zero"
      order_preservation:
        - group: non-zero digits
          preserve: relative order from input
        - group: zero digits
          order: does not matter (all are '0')
      concatenation_order:
        - group: zero digits
        - group: non-zero digits
      output_structure: "Concatenated groups formatted as space-separated digits."
    examples_summary:
      count: 7
      consistency: "All examples follow the same rearrangement pattern."
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of individual digits.
    2.  Create two new lists: one for zero digits (`zeros_list`) and one for non-zero digits (`non_zeros_list`).
    3.  Iterate through the input list of digits:
        *   If a digit is '0', append it to the `zeros_list`.
        *   If a digit is not '0', append it to the `non_zeros_list`.
    4.  Concatenate the `zeros_list` and the `non_zeros_list` in that order to form the final list of digits.
    5.  Join the digits in the final list with spaces to create the output string.
```python
"""
Rearrange digits in a sequence, moving all zeros to the beginning while preserving the relative order of non-zero digits.
"""

import re

def transform(input_str: str) -> str:
    """
    Moves all '0' digits to the beginning of the sequence while maintaining 
    the relative order of the non-zero digits.

    Args:
        input_str: A string containing space-separated single digits.

    Returns:
        A string with digits rearranged according to the rule, 
        also space-separated.
    """
    
    # 1. Parse the input string into a list of individual digits (as strings).
    # We keep them as strings to easily check for '0'.
    digits = input_str.split(' ')

    # 2. Create two new lists: one for zero digits and one for non-zero digits.
    zeros_list = []
    non_zeros_list = []

    # 3. Iterate through the input list of digits:
    for digit in digits:
        # *   If a digit is '0', append it to the zeros_list.
        if digit == '0':
            zeros_list.append(digit)
        # *   If a digit is not '0', append it to the non_zeros_list.
        else:
            non_zeros_list.append(digit)

    # 4. Concatenate the zeros_list and the non_zeros_list in that order.
    final_list = zeros_list + non_zeros_list

    # 5. Join the digits in the final list with spaces to create the output string.
    output_str = ' '.join(final_list)

    return output_str

```
```python
"""
Rearrange elements in a 1D NumPy array, moving all zero elements to the beginning while preserving the relative order of non-zero elements, and return the result as a space-separated string.
"""

import numpy as np

def transform(input_array: np.ndarray) -> str:
    """
    Moves all 0 elements to the beginning of a NumPy array while maintaining 
    the relative order of the non-zero elements, returning a space-separated string.

    Args:
        input_array: A 1-dimensional NumPy array of integers.

    Returns:
        A string with elements rearranged according to the rule, 
        space-separated.
    """
    
    # 1. Initialize lists to store zero and non-zero elements.
    zeros_list = []
    non_zeros_list = []

    # 2. Iterate through each element in the input NumPy array.
    for element in input_array:
        # 3. Check if the element is zero.
        if element == 0:
            # If zero, append to the zeros_list.
            zeros_list.append(element)
        else:
            # If non-zero, append to the non_zeros_list, preserving relative order.
            non_zeros_list.append(element)

    # 4. Concatenate the lists: zeros first, then non-zeros.
    final_list = zeros_list + non_zeros_list

    # 5. Convert each integer element in the final list to its string representation.
    string_list = [str(num) for num in final_list]

    # 6. Join the list of strings with spaces.
    output_str = ' '.join(string_list)

    # 7. Return the final space-separated string.
    return output_str

```
