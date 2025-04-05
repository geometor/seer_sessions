
## train_1

**input:**
```
0 0 0 1 0 0 1 1 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 1 1 0 0 0
```


## train_2

**input:**
```
6 0 0 6 0 0 0 6 6 6 6 6
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 6 6
```


## train_3

**input:**
```
1 1 1 1 1 0 1 0 0 0 1 0
```


**output:**
```
1 1 1 1 1 0 0 0 0 0 0 0
```


## train_4

**input:**
```
5 5 5 5 5 5 5 5 5 5 0 5
```


**output:**
```
5 5 5 5 5 5 5 5 5 5 0 0
```


## train_5

**input:**
```
0 0 4 4 4 4 0 0 0 0 0 4
```


**output:**
```
0 0 4 4 4 4 0 0 0 0 0 0
```


## train_6

**input:**
```
0 1 0 1 0 1 1 1 1 1 1 1
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 1 1
```


## train_7

**input:**
```
9 0 0 0 9 9 9 9 9 9 9 9
```


**output:**
```
0 0 0 0 9 9 9 9 9 9 9 9
```

Okay, let's break down the task based on the examples provided.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are strings containing sequences of single digits separated by spaces. The length of the sequence appears consistent (12 digits in all examples).
2.  **Content:** The sequences consist of digits (0-9).
3.  **Transformation:** The core transformation involves changing certain non-zero digits in the input sequence to 0 in the output sequence. Digits that are already 0 remain 0. Not all non-zero digits are changed.
4.  **Pattern:** The key pattern relates to whether a non-zero digit is "isolated" or part of a larger group of identical adjacent digits. Specifically, a non-zero digit seems to be changed to 0 only if it is *not* adjacent to another digit of the *same* value.

**Facts (YAML):**


```yaml
Data:
  Type: Sequence
  Elements: Integers (0-9)
  Format: Space-separated string
  Length: Fixed (12 in examples)

Objects:
  - Name: Digit
    Properties:
      - value: Integer (0-9)
      - position: Index in the sequence (0-based)
  - Name: Block
    Definition: A contiguous sub-sequence of identical non-zero digits.
    Properties:
      - value: The digit composing the block.
      - length: The number of digits in the block.
      - start_index: The index of the first digit in the block.
      - end_index: The index of the last digit in the block.

Transformation:
  Action: Modify digit value
  Target: Non-zero digits within the input sequence.
  Condition: A non-zero digit's value is changed to 0 if and only if it constitutes a Block of length 1.
  Output: A new sequence reflecting these changes.

Relationships:
  - Adjacency: Digits have left and right neighbors (except at the boundaries).
  - Membership: Digits belong to Blocks.
  - Identity: Digits within a Block share the same non-zero value.
```


**Natural Language Program:**

1.  Accept the input sequence of space-separated digits.
2.  Convert the input string into a list of integers.
3.  Create a new list to store the output, initially identical to the input list.
4.  Iterate through the input list by index, from the first element to the last.
5.  For each element at index `i` with value `v`:
    a.  Check if the value `v` is non-zero.
    b.  If `v` is non-zero, determine if this element is part of a block of identical digits with a length greater than 1. This means checking if either the element to the immediate left (at index `i-1`, if it exists) or the element to the immediate right (at index `i+1`, if it exists) has the same value `v`.
    c.  If *neither* the left neighbor (if exists) *nor* the right neighbor (if exists) has the same value `v`, then this element is an "isolated" non-zero digit (forming a block of length 1).
    d.  If the element is identified as isolated according to step 5c, change the corresponding element at index `i` in the output list to 0.
6.  Convert the modified output list back into a string of space-separated digits.
7.  Return the resulting output string.
```python
import math
import numpy as np
import re # Using re for potentially splitting strings if needed, though simple split is likely sufficient

"""
Transformation Rule:
Accepts a sequence of space-separated digits. Converts any non-zero digit to 0 if it is not adjacent (horizontally) to another digit of the same value. Otherwise, the digit remains unchanged. Zeros always remain zero. Returns the modified sequence as a space-separated string.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    Changes isolated non-zero digits to 0.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)
    n = len(input_list)
    
    # Initialize the output list as a copy of the input list
    output_list = list(input_list) 

    # Iterate through the input list to identify isolated non-zero digits
    for i in range(n):
        current_value = input_list[i]

        # Skip if the current digit is zero
        if current_value == 0:
            continue

        # Check the left neighbor
        has_same_left_neighbor = False
        if i > 0: # Check if a left neighbor exists
            if input_list[i-1] == current_value:
                has_same_left_neighbor = True
                
        # Check the right neighbor
        has_same_right_neighbor = False
        if i < n - 1: # Check if a right neighbor exists
            if input_list[i+1] == current_value:
                has_same_right_neighbor = True

        # If neither neighbor has the same value, it's isolated
        if not has_same_left_neighbor and not has_same_right_neighbor:
            # Change the corresponding digit in the output list to 0
            output_list[i] = 0

    # Format the output list back into a space-separated string
    output_str = format_output(output_list)
    
    return output_str

```
