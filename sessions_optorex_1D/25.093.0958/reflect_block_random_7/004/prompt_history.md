
## train_1

**input:**
```
5 9 3 6 2 6 6 1 6 2 3 3
```


**output:**
```
3 3 2 6 1 6 6 2 6 3 9 5
```


## train_2

**input:**
```
0 0 2 4 9 5 9 2 7 8 2 0
```


**output:**
```
0 0 2 8 7 2 9 5 9 4 2 0
```


## train_3

**input:**
```
9 4 7 7 8 9 3 3 4 8 3 0
```


**output:**
```
3 8 4 3 3 9 8 7 7 4 9 0
```


## train_4

**input:**
```
3 2 4 1 7 1 2 3 5 3 3 9
```


**output:**
```
9 3 3 5 3 2 1 7 1 4 2 3
```


## train_5

**input:**
```
4 8 6 4 7 4 4 8 1 5 0 0
```


**output:**
```
5 1 8 4 4 7 4 6 8 4 0 0
```


## train_6

**input:**
```
0 0 0 0 7 9 2 5 2 1 0 0
```


**output:**
```
0 0 0 0 1 2 5 2 9 7 0 0
```


## train_7

**input:**
```
9 1 2 4 5 6 1 2 2 5 3 6
```


**output:**
```
6 3 5 2 2 1 6 5 4 2 1 9
```

Okay, let's analyze the transformation.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both inputs and outputs are strings representing sequences of single digits separated by spaces.
2.  **Sequence Length:** The length of the output sequence is always the same as the length of the input sequence (12 digits in all examples).
3.  **Element Conservation:** The digits present in the output are the same digits present in the input, just potentially in a different order. This suggests a rearrangement or reversal operation.
4.  **Role of Zeros:** Zeros at the beginning and end of the sequence appear to maintain their positions relative to the start and end. For instance, in `train_2`, `0 0` at the start and `0` at the end remain. In `train_6`, `0 0 0 0` at the start and `0 0` at the end remain.
5.  **Core Transformation:** The digits *between* the leading and trailing zeros (the contiguous block of non-zero digits, or the block including non-zeros if there are no leading/trailing zeros) seem to be reversed.
    *   `train_1`: `5 9 3 6 2 6 6 1 6 2 3 3` (no leading/trailing zeros) -> reversed `3 3 2 6 1 6 6 2 6 3 9 5`.
    *   `train_2`: `0 0 [2 4 9 5 9 2 7 8 2] 0` -> `0 0 [2 8 7 2 9 5 9 4 2] 0` (block `2...2` is reversed).
    *   `train_5`: `[4 8 6 4 7 4 4 8 1 5] 0 0` -> `[5 1 8 4 4 7 4 6 8 4] 0 0` (block `4...5` is reversed).
    *   `train_6`: `0 0 0 0 [7 9 2 5 2 1] 0 0` -> `0 0 0 0 [1 2 5 2 9 7] 0 0` (block `7...1` is reversed).

**Facts Documentation:**


```yaml
objects:
  - name: input_sequence
    type: list of integers
    description: The sequence of digits provided as input.
  - name: output_sequence
    type: list of integers
    description: The sequence of digits produced as output.
  - name: leading_zeros
    type: list of integers
    description: A sublist containing zeros from the beginning of the input sequence, up to the first non-zero digit. Can be empty.
  - name: trailing_zeros
    type: list of integers
    description: A sublist containing zeros from the end of the input sequence, starting after the last non-zero digit. Can be empty.
  - name: core_block
    type: list of integers
    description: The contiguous sublist of the input sequence between the leading and trailing zeros (inclusive of the first and last non-zero elements). If there are no zeros, this is the entire input sequence.
properties:
  - object: input_sequence
    name: elements
    type: list of integers
  - object: input_sequence
    name: length
    type: integer
actions:
  - name: parse_input
    description: Convert the input string into a list of integers.
  - name: identify_leading_zeros
    description: Find the sublist of zeros at the start of the sequence.
  - name: identify_trailing_zeros
    description: Find the sublist of zeros at the end of the sequence.
  - name: identify_core_block
    description: Extract the sublist located between the leading and trailing zeros.
  - name: reverse_list
    input: list
    output: list
    description: Reverse the order of elements in a given list.
  - name: concatenate_lists
    input: list_1, list_2, list_3
    output: list
    description: Combine multiple lists into a single list in the specified order.
  - name: format_output
    description: Convert the final list of integers back into a space-separated string.
relationships:
  - type: transformation
    origin: input_sequence
    target: output_sequence
    rule: The output_sequence is formed by concatenating the leading_zeros, the reversed core_block, and the trailing_zeros from the input_sequence.
```


**Natural Language Program:**

1.  Parse the input string of space-separated digits into a list of integers (let's call it `input_list`).
2.  Find the index of the first non-zero element in `input_list`. If all elements are zero, treat the entire list as both leading and trailing zeros, resulting in an identical output list.
3.  Find the index of the last non-zero element in `input_list`.
4.  Extract the sublist of leading zeros: elements from the start of `input_list` up to (but not including) the first non-zero element. Store this as `leading_zeros`.
5.  Extract the sublist of trailing zeros: elements from the position after the last non-zero element to the end of `input_list`. Store this as `trailing_zeros`.
6.  Extract the core sublist: elements from the first non-zero element up to and including the last non-zero element. Store this as `core_block`.
7.  Reverse the order of elements within the `core_block`.
8.  Construct the final output list by concatenating `leading_zeros`, the reversed `core_block`, and `trailing_zeros` in that order.
9.  Format the resulting list back into a string of space-separated digits for the final output.
```python
import math
import numpy as np
import re

"""
Transforms an input sequence of space-separated digits by reversing the order 
of the subsequence located between the leading and trailing zeros, while keeping 
the leading and trailing zeros in their original positions.

1. Parse the input string into a list of integers.
2. Identify the contiguous block of leading zeros (if any).
3. Identify the contiguous block of trailing zeros (if any).
4. Identify the core block of digits between the leading and trailing zeros.
5. Reverse the order of the elements within the core block.
6. Concatenate the leading zeros, the reversed core block, and the trailing zeros.
7. Format the resulting list back into a space-separated string.
"""

def parse_input_string(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output_list(output_list: list[int]) -> str:
    """Converts a list of integers back into a space-separated string."""
    return ' '.join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    """
    # Parse the input string into a list of integers
    input_list = parse_input_string(input_str)
    n = len(input_list)

    # Handle the edge case of an empty input
    if n == 0:
        return ""

    # Find the index of the first non-zero element
    first_non_zero_index = -1
    for i in range(n):
        if input_list[i] != 0:
            first_non_zero_index = i
            break

    # If all elements are zero, return the original list as a string
    if first_non_zero_index == -1:
        return format_output_list(input_list)

    # Find the index of the last non-zero element
    last_non_zero_index = -1
    for i in range(n - 1, -1, -1):
        if input_list[i] != 0:
            last_non_zero_index = i
            break
            
    # Should always find one if first_non_zero_index was found, but check just in case
    if last_non_zero_index == -1: # This case technically covered by first check
         return format_output_list(input_list)


    # Extract leading zeros
    leading_zeros = input_list[:first_non_zero_index]

    # Extract trailing zeros
    # The slice starts *after* the last non-zero index
    trailing_zeros = input_list[last_non_zero_index + 1:]

    # Extract the core block (between first and last non-zero, inclusive)
    core_block = input_list[first_non_zero_index : last_non_zero_index + 1]

    # Reverse the core block
    reversed_core_block = core_block[::-1]

    # Concatenate the parts to form the output list
    output_list = leading_zeros + reversed_core_block + trailing_zeros

    # Format the output list back into a string
    output_str = format_output_list(output_list)

    return output_str

```
```python
import numpy as np
import math # Although not strictly needed for this logic, keeping standard imports
import re # Although not strictly needed for this logic, keeping standard imports

"""
Transforms an input sequence of digits by reversing the order of the subsequence 
located between the first and last non-zero digits, while keeping any leading 
and trailing zeros in their original positions.

1. Convert the input (potentially a NumPy array or string) into a list of integers.
2. Find the index of the first non-zero element.
3. Find the index of the last non-zero element.
4. If no non-zero elements exist, return the original sequence formatted as a string.
5. Extract the sublist of leading zeros (before the first non-zero).
6. Extract the core sublist (from the first non-zero to the last non-zero, inclusive).
7. Extract the sublist of trailing zeros (after the last non-zero).
8. Reverse the order of elements within the core sublist.
9. Concatenate the leading zeros, the reversed core sublist, and the trailing zeros.
10. Format the resulting list back into a space-separated string.
"""

def _list_to_string(int_list: list[int]) -> str:
    """Converts a list of integers to a space-separated string."""
    return ' '.join(map(str, int_list))

def transform(input_data) -> str:
    """
    Applies the transformation rule to the input data.
    """
    # --- Input Handling ---
    # Convert input to a list of integers, handling NumPy array or string
    if isinstance(input_data, str):
        # Handle potential empty string or strings with just spaces
        parts = input_data.split()
        if not parts:
            input_list = []
        else:
             try:
                 input_list = [int(digit) for digit in parts]
             except ValueError:
                 # Handle cases where the string might not contain valid integers
                 # For this problem context, assume valid input as per examples
                 # Or raise an error, or return an empty string/error indicator
                 # Based on examples, assume valid digit strings
                 input_list = [int(digit) for digit in parts] # Redundant but clarifies intent
    elif isinstance(input_data, np.ndarray):
        input_list = input_data.tolist()
    elif isinstance(input_data, list):
        # Assume it's already a list of integers or compatible types
        input_list = list(map(int, input_data)) # Ensure elements are integers
    else:
        raise TypeError(f"Unsupported input type: {type(input_data)}")

    n = len(input_list)

    # Handle empty input list
    if n == 0:
        return ""

    # --- Find Non-Zero Boundaries ---
    first_non_zero_index = -1
    for i in range(n):
        if input_list[i] != 0:
            first_non_zero_index = i
            break

    # Handle case where all elements are zero
    if first_non_zero_index == -1:
        return _list_to_string(input_list)

    last_non_zero_index = -1
    # Search backwards from the end for the last non-zero
    for i in range(n - 1, first_non_zero_index - 1, -1): # Stop search once first non-zero is passed
        if input_list[i] != 0:
            last_non_zero_index = i
            break
            
    # This condition should technically not be needed if first_non_zero_index != -1
    # but included for robustness (though logically covered by the first check)
    if last_non_zero_index == -1:
         return _list_to_string(input_list) # Should not happen if first_non_zero was found

    # --- Extract Subsequences ---
    # Extract leading zeros (elements before the first non-zero index)
    leading_zeros = input_list[:first_non_zero_index]

    # Extract the core block (elements from first non-zero up to and including last non-zero)
    core_block = input_list[first_non_zero_index : last_non_zero_index + 1]

    # Extract trailing zeros (elements after the last non-zero index)
    trailing_zeros = input_list[last_non_zero_index + 1:]

    # --- Reverse Core ---
    # Reverse the order of elements in the core block
    reversed_core_block = core_block[::-1]

    # --- Concatenate ---
    # Combine the parts in the correct order
    output_list = leading_zeros + reversed_core_block + trailing_zeros

    # --- Output Formatting ---
    # Convert the final list back to a space-separated string
    output_str = _list_to_string(output_list)

    return output_str
```
