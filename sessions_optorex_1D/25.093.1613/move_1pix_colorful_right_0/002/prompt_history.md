
## train_1

**input:**
```
0 7 6 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 6 9 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 9 8 4 5 8 8 8 2 0
```


**output:**
```
0 0 0 0 9 8 4 5 8 8 8 2
```


## train_3

**input:**
```
3 4 5 4 4 8 6 2 1 0 0 0
```


**output:**
```
0 3 4 5 4 4 8 6 2 1 0 0
```


## train_4

**input:**
```
0 0 7 1 2 3 0 0 0 0 0 0
```


**output:**
```
0 0 0 7 1 2 3 0 0 0 0 0
```


## train_5

**input:**
```
0 8 1 9 5 2 3 9 8 7 5 0
```


**output:**
```
0 0 8 1 9 5 2 3 9 8 7 5
```


## train_6

**input:**
```
5 7 9 2 4 9 5 6 6 9 0 0
```


**output:**
```
0 5 7 9 2 4 9 5 6 6 9 0
```


## train_7

**input:**
```
9 5 5 9 4 1 6 9 5 0 0 0
```


**output:**
```
0 9 5 5 9 4 1 6 9 5 0 0
```

Okay, I will analyze the provided input-output pairs to understand the transformation logic.

**Perception of Elements:**

*   **Objects:** The primary objects are sequences of single digits (0-9). These sequences are represented as strings with space delimiters.
*   **Properties:** Each sequence has a fixed length (12 in all examples). The digits within the sequence can be zero or non-zero. The position (index) of each digit is important. We can identify leading zeros, trailing zeros, and a "core" block of non-zero digits (potentially interspersed with zeros).
*   **Actions:** The core action appears to be a positional shift or insertion/deletion operation based on the location of non-zero digits. Specifically, a '0' seems to be inserted, and an element seems to be removed to maintain the sequence length.
*   **Relationships:** The output sequence is derived directly from the input sequence by rearranging elements based on the position of the first and last non-zero digits. The length of the sequence remains constant.

**Facts:**


```yaml
task_description: "Shift a block of numbers within a sequence and adjust length."
elements:
  - type: sequence
    properties:
      - content: list of single digits (0-9)
      - length: fixed (12 in examples)
      - structure: ordered
      - representation: space-separated string
  - type: digit
    properties:
      - value: 0-9
      - significance: zero vs. non-zero
  - type: sub-sequence
    definition: "The contiguous block starting from the first non-zero digit and ending with the last non-zero digit in the input sequence."
    properties:
      - start_index: index of the first non-zero digit
      - end_index: index of the last non-zero digit
actions:
  - name: identify_first_non_zero_index
    input: input sequence
    output: index (integer) or indicator of none found
  - name: identify_last_non_zero_index
    input: input sequence
    output: index (integer) or indicator of none found
  - name: insert_zero
    target: input sequence
    position: immediately before the index identified by 'identify_first_non_zero_index'
  - name: remove_last_element
    target: modified sequence (after insertion)
    position: the final element
transformation_rule:
  condition: "If the input sequence contains at least one non-zero digit."
  steps:
    - Find the index of the first non-zero digit (`first_nz_idx`).
    - Insert a '0' into the sequence at `first_nz_idx`.
    - Remove the last element from the resulting sequence.
  fallback: "If the input sequence contains only zeros, return the input sequence unchanged."
invariants:
  - The length of the output sequence is the same as the length of the input sequence.
  - The relative order of digits within the identified 'sub-sequence' is preserved.
  - The relative order of leading zeros (before the first non-zero digit) is preserved.
```


**Natural Language Program:**

1.  Read the input sequence of space-separated digits.
2.  Convert the sequence into a list of integers.
3.  Check if the sequence contains any non-zero digits.
    *   If the sequence contains only zeros, return the original sequence as a space-separated string.
    *   If the sequence contains non-zero digits, proceed to step 4.
4.  Find the index of the first non-zero digit in the list.
5.  Insert the integer `0` into the list at this found index.
6.  Remove the last element from the modified list.
7.  Convert the final list back into a sequence of space-separated digits (string).
8.  Return the resulting string.
```python
import math
import numpy as np
import re

"""
Transforms an input sequence of space-separated digits based on the following logic:
1. Convert the input string into a list of integers.
2. Check if the sequence contains any non-zero digits.
   - If all digits are zero, return the original input string.
   - Otherwise, proceed to the next step.
3. Find the index of the first non-zero digit in the list.
4. Insert the integer 0 into the list at this found index.
5. Remove the last element from the modified list to maintain the original length.
6. Convert the final list back into a space-separated string.
7. Return the resulting string.
"""

def _find_first_non_zero_index(data_list):
    """Helper function to find the index of the first non-zero element."""
    for index, value in enumerate(data_list):
        if value != 0:
            return index
    return -1 # Indicate no non-zero element found

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.
    """
    # 1. Convert the input string into a list of integers.
    # Handle potential empty strings or non-integer inputs gracefully if needed,
    # but based on examples, assume valid input format.
    input_list = [int(digit) for digit in input_str.split()]

    # 2. Check if the sequence contains only zeros.
    if all(digit == 0 for digit in input_list):
        # If all digits are zero, return the original input string.
        return input_str

    # 3. Find the index of the first non-zero digit.
    first_nz_idx = _find_first_non_zero_index(input_list)

    # Check if a non-zero index was actually found (handles edge case, though covered by step 2)
    if first_nz_idx != -1:
        # 4. Insert the integer 0 into the list at the found index.
        # Create a copy to avoid modifying the original list if it's needed elsewhere,
        # although in this standalone function, modifying in place is also fine.
        output_list = list(input_list) # Make a copy
        output_list.insert(first_nz_idx, 0)

        # 5. Remove the last element from the modified list.
        output_list.pop() # Removes the last element
    else:
        # This case should technically not be reached if step 2 works correctly
        # for inputs with non-zero numbers, but included for robustness.
        output_list = list(input_list)


    # 6. Convert the final list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    # 7. Return the resulting string.
    return output_str

```
