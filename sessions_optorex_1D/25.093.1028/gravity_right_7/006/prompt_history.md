
## train_1

**input:**
```
1 4 0 0 2 7 0 7 9 5 0 2
```


**output:**
```
0 0 0 0 1 4 2 7 7 9 5 2
```


## train_2

**input:**
```
0 0 7 0 8 4 0 8 0 0 0 8
```


**output:**
```
0 0 0 0 0 0 0 7 8 4 8 8
```


## train_3

**input:**
```
6 8 8 0 5 0 1 0 0 0 7 7
```


**output:**
```
0 0 0 0 0 6 8 8 5 1 7 7
```


## train_4

**input:**
```
7 9 3 6 9 0 0 0 0 3 0 0
```


**output:**
```
0 0 0 0 0 0 7 9 3 6 9 3
```


## train_5

**input:**
```
0 0 0 1 8 0 1 0 9 4 6 2
```


**output:**
```
0 0 0 0 0 1 8 1 9 4 6 2
```


## train_6

**input:**
```
6 0 0 6 0 0 7 0 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 6 6 7 1
```


## train_7

**input:**
```
0 0 5 8 0 7 9 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 5 8 7 9 2
```

**Perception of Elements:**

The input and output are both sequences of single-digit numbers, presented as space-separated strings. The length of the output sequence is identical to the length of the input sequence in all examples. The core operation appears to be a rearrangement of the elements within the sequence based on their value (zero or non-zero). The relative order of the non-zero elements is preserved, as is the count of zero elements.

**Facts:**


```yaml
Input:
  type: sequence
  elements: single digits (0-9)
  representation: space-separated string
Output:
  type: sequence
  elements: single digits (0-9)
  representation: space-separated string
  length: same as input length
Properties:
  - digits:
      value: Can be zero (0) or non-zero (1-9)
Relationship:
  - Output is a reordering of the Input sequence.
Transformation:
  action: Partitioning and Concatenation
  rule:
    - Identify all zero digits in the input sequence.
    - Identify all non-zero digits in the input sequence, preserving their original relative order.
    - Construct the output sequence by concatenating all identified zero digits followed by all identified non-zero digits.
```


**Natural Language Program:**

1.  Read the input sequence of digits.
2.  Create two empty lists: one for zero digits (`zeros_list`) and one for non-zero digits (`non_zeros_list`).
3.  Iterate through the input sequence, digit by digit.
4.  For each digit:
    *   If the digit is 0, append it to the `zeros_list`.
    *   If the digit is not 0, append it to the `non_zeros_list`.
5.  Concatenate the `zeros_list` and the `non_zeros_list` to form the final output sequence.
6.  Format the output sequence as a space-separated string of digits.
```python
import math
import numpy as np
import re

"""
Identifies all zero digits and all non-zero digits in the input sequence.
Constructs the output sequence by concatenating all identified zero digits followed by all identified non-zero digits, preserving the original relative order of the non-zero digits.
"""

def transform(input_str: str) -> str:
    """
    Moves all zeros in the input sequence to the beginning, preserving the relative order of non-zero elements.

    Args:
        input_str: A string containing space-separated single digits.

    Returns:
        A string containing space-separated single digits with zeros moved to the front.
    """

    # 1. Read the input sequence of digits.
    # Convert the space-separated string into a list of integers.
    try:
        input_digits = [int(d) for d in input_str.split()]
    except ValueError:
        # Handle potential errors if the input string contains non-digits
        print(f"Error: Input string '{input_str}' contains non-digit characters.")
        return "" # Or raise an exception

    # 2. Create two empty lists: one for zero digits and one for non-zero digits.
    zeros_list = []
    non_zeros_list = []

    # 3. Iterate through the input sequence, digit by digit.
    # 4. For each digit:
    #    *   If the digit is 0, append it to the zeros_list.
    #    *   If the digit is not 0, append it to the non_zeros_list.
    for digit in input_digits:
        if digit == 0:
            zeros_list.append(digit)
        else:
            non_zeros_list.append(digit)

    # 5. Concatenate the zeros_list and the non_zeros_list to form the final output sequence.
    output_digits = zeros_list + non_zeros_list

    # 6. Format the output sequence as a space-separated string of digits.
    output_str = " ".join(map(str, output_digits))

    return output_str

```
```python
import math
import numpy as np
import re # Although not used in the final logic, keeping it for consistency if future regex needed

"""
Moves all zeros in the input sequence to the beginning, while preserving the relative order of the non-zero elements. The input is assumed to be a sequence (like a list or NumPy array) of digits.
"""

def transform(input_sequence):
    """
    Rearranges a sequence of digits by moving all zeros to the front,
    maintaining the relative order of the non-zero digits.

    Args:
        input_sequence: A list or array-like sequence of integers (digits 0-9).

    Returns:
        A new list containing the rearranged sequence of digits.
    """

    # 1. Initialize lists to store zero and non-zero elements
    zeros_list = []
    non_zeros_list = []

    # 2. Iterate through the input sequence
    for digit in input_sequence:
        # 3. Partition elements based on value
        if digit == 0:
            # Append zeros to the zeros list
            zeros_list.append(digit)
        else:
            # Append non-zeros to the non-zeros list, preserving order
            non_zeros_list.append(digit)

    # 4. Concatenate the lists: zeros first, then non-zeros
    output_sequence = zeros_list + non_zeros_list

    # 5. Return the rearranged sequence
    return output_sequence
```
```python
import numpy as np # Import numpy, although standard list operations are sufficient
import math
import re # Import re, although not used in this specific logic

"""
Rearranges a sequence of digits by moving all zero (0) elements to the beginning of the sequence, while preserving the original relative order of all non-zero elements.
"""

def transform(input_sequence):
    """
    Moves all zeros in the input sequence to the beginning, preserving the relative order of non-zero elements.

    Args:
        input_sequence: A list or array-like sequence of integers (digits 0-9).

    Returns:
        A new list containing the rearranged sequence of digits.
    """

    # 1. Initialize lists to store zero and non-zero elements
    zeros_group = []
    non_zeros_group = []

    # 2. Iterate through the input sequence, processing one digit at a time.
    #    This loop correctly handles iterating over elements whether input_sequence
    #    is a list or a NumPy array.
    for digit in input_sequence:
        # 3. For each individual digit examined:
        #    Check if the digit's value is exactly 0.
        if digit == 0:
            # If the digit is 0, append it to the zeros_group.
            zeros_group.append(digit)
        else:
            # If the digit is not 0, append it to the non_zeros_group.
            non_zeros_group.append(digit)

    # 4. Combine the two groups by concatenating the zeros_group
    #    followed by the non_zeros_group.
    output_sequence = zeros_group + non_zeros_group

    # 5. Return the rearranged sequence.
    #    (Formatting to string is assumed to happen outside this function based on problem description)
    return output_sequence
```
