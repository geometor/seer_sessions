
## train_1

**input:**
```
2 9 9 9 9 9 0 0 0 0 0 0
```


**output:**
```
2 9 9 9 9 9 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 1 1 1 1 1 1 0 0 0
```


**output:**
```
4 4 4 1 1 1 1 1 1 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 3 3 3 3 1 0
```


**output:**
```
0 0 0 0 0 0 3 3 3 3 1 1
```


## train_4

**input:**
```
0 0 0 0 0 0 0 6 6 6 3 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 3 3
```


## train_5

**input:**
```
0 5 5 5 2 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 2 2 2 2 2 2 2 2
```


## train_6

**input:**
```
0 1 8 8 8 8 8 8 0 0 0 0
```


**output:**
```
1 1 8 8 8 8 8 8 0 0 0 0
```


## train_7

**input:**
```
0 0 2 8 8 8 8 0 0 0 0 0
```


**output:**
```
2 2 2 8 8 8 8 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The task operates on sequences of 12 digits.
    *   The core elements are digits, specifically distinguishing between zero (`0`) and non-zero digits (1-9).
    *   The transformation involves changing some zero digits to non-zero values based on their neighbors.
    *   Positional adjacency is crucial.
    *   Contiguous blocks of identical digits (both zeros and non-zeros) play a role. Specifically, whether a non-zero digit is part of a repeating block or stands alone seems important.

*   **YAML Facts:**
    ```
yaml
    elements:
      - type: sequence
        description: A fixed-length sequence of 12 digits (0-9).
        length: 12
      - type: digit
        value_range: 0-9
        properties:
          - is_zero: boolean (true if value is 0)
          - is_non_zero: boolean (true if value is 1-9)

    objects:
      - name: input_sequence
        type: sequence
      - name: output_sequence
        type: sequence
      - name: non_zero_digit
        type: digit
        properties:
          - is_non_zero: true
      - name: single_non_zero_digit
        type: non_zero_digit
        description: A non-zero digit whose immediate left and right neighbors (if they exist within the sequence boundaries) have different values from it.
      - name: zero_digit
        type: digit
        properties:
          - is_zero: true
      - name: contiguous_zero_block
        type: sequence
        description: A subsequence consisting only of one or more adjacent zero digits.

    relationships:
      - type: adjacency
        description: The property of digits being immediately next to each other (left or right) in the sequence.
      - type: context
        description: The value of neighboring digits determines if a non-zero digit is "single".
      - type: propagation
        description: The value of a "single" non-zero digit propagates into adjacent blocks of zeros.

    actions:
      - name: identify_singles
        description: Iterate through the input sequence to find non-zero digits that are not identical to their immediate left or right neighbors.
        input: input_sequence
        output: list of indices and values of single non-zero digits
      - name: fill_adjacent_zeros
        description: For each single non-zero digit, find contiguous blocks of zeros immediately to its left and right, and replace those zeros with the single digit's value.
        input: index and value of a single non-zero digit, sequence (initially input, progressively modified)
        output: modified sequence
    
```python
import math
import numpy as np # Although not strictly needed for list manipulation, good practice to import common libraries

"""
Identifies "single" non-zero digits in a sequence and propagates their value into adjacent blocks of zeros.
A non-zero digit is considered "single" if its immediate left and right neighbors (if they exist within the sequence bounds) have different values from it. In other words, it's a non-zero digit that is not part of a contiguous block of the same non-zero digit.
The value of each identified single digit replaces the zeros in the contiguous block(s) of zeros immediately to its left and/or right. Propagation stops when a non-zero digit or the boundary of the sequence is encountered.
"""

def is_single(input_list, index):
    """
    Checks if the digit at the given index in the input list is a 'single' non-zero digit.

    A digit is 'single' if it's non-zero and its immediate neighbors (if they exist)
    have different values.

    Args:
        input_list: The list of integers representing the sequence.
        index: The index of the digit to check.

    Returns:
        True if the digit at the index is single, False otherwise.
    """
    n = len(input_list)
    value = input_list[index]

    # Rule 1: Must be non-zero
    if value == 0:
        return False

    # Rule 2: Check left neighbor (if it exists) must be different
    left_different = (index == 0) or (input_list[index - 1] != value)

    # Rule 3: Check right neighbor (if it exists) must be different
    right_different = (index == n - 1) or (input_list[index + 1] != value)

    # Satisfies all rules if non-zero and different from existing neighbors
    return left_different and right_different

def transform(input_str: str) -> str:
    """
    Transforms an input sequence string based on the single digit propagation rule.

    It finds non-zero digits not part of a block of identical digits and propagates
    their value into adjacent zero blocks.

    Args:
        input_str: A string of space-separated digits (e.g., "0 0 4 1 1 0").

    Returns:
        A string of space-separated digits representing the transformed sequence.
    """
    # Parse input string into a list of integers
    input_list = [int(d) for d in input_str.split()]
    n = len(input_list)

    # Initialize output_list as a copy of the input list.
    # Modifications will be made to this list.
    output_list = list(input_list)

    # --- Identify single non-zero digits ---
    # Iterate through the original input list to find digits that meet the 'single' criteria.
    singles = []
    for i in range(n):
        if is_single(input_list, i):
            # Store the index and value of each single digit found.
            singles.append({"index": i, "value": input_list[i]})

    # --- Propagate values into adjacent zeros ---
    # Iterate through the identified single digits.
    for single in singles:
        idx = single["index"]
        val = single["value"]

        # Propagate to the left:
        # Start from the position immediately left of the single digit.
        j = idx - 1
        # Move leftwards as long as we are within bounds and encounter zeros in the *original* input.
        # Checking the original input prevents propagation into areas filled by other singles in this step.
        while j >= 0 and input_list[j] == 0:
            # Update the corresponding position in the output list with the single digit's value.
            output_list[j] = val
            j -= 1 # Move one step further left.

        # Propagate to the right:
        # Start from the position immediately right of the single digit.
        j = idx + 1
        # Move rightwards as long as we are within bounds and encounter zeros in the *original* input.
        while j < n and input_list[j] == 0:
            # Update the corresponding position in the output list with the single digit's value.
            output_list[j] = val
            j += 1 # Move one step further right.

    # Format the final output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))
    return output_str
```
