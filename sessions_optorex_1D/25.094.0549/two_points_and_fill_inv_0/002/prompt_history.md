
## train_1

**input:**
```
9 9 9 9 9 9 9 9 9 0 0 0
```


**output:**
```
9 0 0 0 0 0 0 0 9 0 0 0
```


## train_2

**input:**
```
0 0 0 7 7 7 7 7 7 7 7 0
```


**output:**
```
0 0 0 7 0 0 0 0 0 0 7 0
```


## train_3

**input:**
```
0 0 0 0 8 8 8 8 8 8 8 8
```


**output:**
```
0 0 0 0 8 0 0 0 0 0 0 8
```


## train_4

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 0 0 0 0 0 0 0 0 0 0 7
```


## train_5

**input:**
```
0 0 0 7 7 7 7 7 7 0 0 0
```


**output:**
```
0 0 0 7 0 0 0 0 7 0 0 0
```


## train_6

**input:**
```
0 0 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
0 0 3 0 0 0 0 0 0 0 0 3
```


## train_7

**input:**
```
0 1 1 1 1 1 1 1 0 0 0 0
```


**output:**
```
0 1 0 0 0 0 0 1 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences of single digits, represented as space-separated strings.
    *   The length of the sequences appears fixed (12 digits in the examples).
    *   The core operation involves identifying the span of non-zero digits within the sequence.
    *   Digits outside this span (leading and trailing zeros) seem unchanged.
    *   Digits *within* the span, excluding the very first and very last non-zero digits, are changed to zero.
    *   The first non-zero digit and the last non-zero digit in the sequence retain their original positions and values.

*   **YAML Fact Document:**
    
```yaml
    task_description: Modifying a sequence of digits based on the positions of non-zero elements.
    input_data:
      type: string
      format: space-separated single digits (0-9)
      elements: sequence of numbers
      length: 12 (observed in examples)
    output_data:
      type: string
      format: space-separated single digits (0-9)
      elements: sequence of numbers, modified from input
      length: 12 (observed in examples)
    objects:
      - sequence: The list of digits.
      - digit: Individual element within the sequence.
      - non_zero_digit: A digit with a value > 0.
    properties:
      - index: Position of a digit within the sequence.
      - value: The numerical value of a digit (0-9).
      - first_non_zero: The non-zero digit with the lowest index.
      - last_non_zero: The non-zero digit with the highest index.
    actions:
      - identify: Find the indices of the first and last non-zero digits.
      - preserve: Keep the original value of certain digits (leading/trailing zeros, first/last non-zero).
      - replace: Change the value of digits between the first and last non-zero digits to 0.
    relationships:
      - between: The concept of digits located strictly between the index of the first non-zero digit and the index of the last non-zero digit.
      - boundary: The first and last non-zero digits define the boundaries for the replacement action.
    invariants:
      - Sequence length remains constant.
      - Digits outside the span from the first non-zero to the last non-zero digit are unchanged.
      - The values and positions of the first and last non-zero digits themselves are unchanged.
    special_cases:
      - If the sequence contains no non-zero digits, the output is identical to the input.
      - If the sequence contains only one non-zero digit, the output is identical to the input (as the first and last non-zero digit are the same).
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of digits.
    2.  Find the index of the first non-zero digit in the list. If no non-zero digit exists, proceed to step 6.
    3.  Find the index of the last non-zero digit in the list.
    4.  Create a copy of the input list to serve as the initial output list.
    5.  Iterate through the indices of the output list starting from the index *after* the first non-zero digit's index, up to (but *not including*) the last non-zero digit's index. For each index in this range, set the corresponding digit in the output list to 0.
    6.  Convert the final output list back into a space-separated string.
```python
import numpy as np
import math # Note: math isn't strictly needed for this specific problem, but included as per instructions

"""
Transforms a sequence of digits by finding the first and last non-zero digits. 
All digits strictly between these two boundary digits are changed to zero, while 
the boundary digits themselves and any leading/trailing zeros remain unchanged.
"""

def find_first_non_zero_index(digit_list):
  """Finds the index of the first non-zero digit in a list."""
  for i, digit in enumerate(digit_list):
    if digit != 0:
      return i
  return None # Return None if no non-zero digit is found

def find_last_non_zero_index(digit_list):
  """Finds the index of the last non-zero digit in a list."""
  last_idx = None
  for i, digit in enumerate(digit_list):
    if digit != 0:
      last_idx = i
  return last_idx # Returns None if no non-zero digit is found, or the index of the last one

def transform(input_str):
    """
    Applies the transformation rule to the input string of digits.

    Args:
      input_str: A string of space-separated single digits.

    Returns:
      A string of space-separated single digits representing the transformed sequence.
    """
    # 1. Parse the input string into a list of digits (integers).
    input_digits = [int(d) for d in input_str.split()]

    # 2. Find the index of the first non-zero digit.
    first_idx = find_first_non_zero_index(input_digits)

    # If no non-zero digit exists, return the original string.
    if first_idx is None:
        return input_str

    # 3. Find the index of the last non-zero digit.
    #    (We know at least one exists if first_idx is not None)
    last_idx = find_last_non_zero_index(input_digits)

    # 4. Create a copy of the input list to serve as the initial output list.
    output_digits = list(input_digits) # Use list() to ensure a copy

    # 5. Iterate through the indices *between* the first and last non-zero digits.
    #    The range starts one *after* the first index and goes up to, but
    #    *not including*, the last index.
    #    If first_idx == last_idx (only one non-zero), the range will be empty.
    for i in range(first_idx + 1, last_idx):
        # Set the corresponding digit in the output list to 0.
        output_digits[i] = 0

    # 6. Convert the final output list back into a space-separated string.
    output_str = " ".join(map(str, output_digits))

    return output_str

```
