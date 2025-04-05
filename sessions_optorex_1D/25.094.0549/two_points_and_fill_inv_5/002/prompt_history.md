
## train_1

**input:**
```
1 1 1 1 0 0 0 0 0 0 0 0
```


**output:**
```
1 0 0 1 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 3 3 3 3 3 0 0 0
```


**output:**
```
0 0 0 0 3 0 0 0 3 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 3 3 3 3
```


**output:**
```
0 0 0 0 0 0 0 0 3 0 0 3
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 1 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 1 1
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 1 1 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 0 1 0
```


## train_6

**input:**
```
0 0 0 0 9 9 9 9 9 9 0 0
```


**output:**
```
0 0 0 0 9 0 0 0 0 9 0 0
```


## train_7

**input:**
```
9 9 9 9 9 9 9 9 0 0 0 0
```


**output:**
```
9 0 0 0 0 0 0 9 0 0 0 0
```

**Perception:**

The task involves transforming a sequence of single-digit integers. The input sequence consists of digits separated by spaces. The output sequence also consists of digits separated by spaces, maintaining the same overall length as the input.

The core transformation logic appears to operate on contiguous blocks (runs) of identical non-zero digits within the input sequence.

-   Zero digits ('0') in the input seem to remain unchanged in the output.
-   Runs of identical non-zero digits are treated differently based on their length:
    -   If a run has a length of 1 or 2, it remains unchanged in the output (e.g., `1 1` in train\_4).
    -   If a run has a length of 3 or more, it is modified: the first digit and the last digit of the run are kept, while all the digits in between are replaced with '0's. The number of '0's inserted is equal to the length of the original run minus 2. (e.g., `1 1 1 1` becomes `1 0 0 1`, `3 3 3 3 3` becomes `3 0 0 0 3`).
-   The transformation applies independently to each such block within the sequence.

**Facts:**


```yaml
task_elements:
  - type: input_data
    description: A sequence of single-digit integers, represented as space-separated strings.
    properties:
      - contains_zeros: boolean
      - contains_non_zeros: boolean
      - has_blocks_of_identical_non_zeros: boolean
      - block_length: integer (variable)

  - type: output_data
    description: A sequence of single-digit integers, corresponding to the transformed input.
    properties:
      - same_length_as_input: boolean

  - type: transformation_rule
    description: Modifies blocks of identical non-zero digits based on block length.
    actions:
      - identify_blocks: Locate contiguous sequences of identical non-zero digits.
      - check_block_length: Determine the number of digits in each identified block.
      - apply_modification:
          condition: block_length >= 3
          steps:
            - Keep the first digit of the block.
            - Replace the middle (block_length - 2) digits with '0'.
            - Keep the last digit of the block.
      - preserve_elements:
          condition: digit is '0' OR block_length < 3
          steps:
            - Keep the digit or the block unchanged.
    relationships:
      - Zeros in the input map directly to zeros in the output at the same position.
      - Non-zero blocks in the input map to potentially modified blocks in the output, preserving overall sequence length.
```


**Natural Language Program:**

1.  Initialize an empty output sequence.
2.  Iterate through the input sequence, identifying consecutive blocks of identical digits.
3.  For each block identified:
    a.  Determine the digit value and the length of the block.
    b.  If the digit is '0', append the entire block of '0's to the output sequence.
    c.  If the digit is non-zero:
        i.  Check the length of the block.
        ii. If the length is less than 3, append the original block to the output sequence.
        iii. If the length is 3 or greater:
            1.  Append the first digit of the block to the output sequence.
            2.  Append `length - 2` zeros ('0') to the output sequence.
            3.  Append the last digit of the block (which is the same as the first) to the output sequence.
4.  Combine the processed blocks to form the final output sequence.
5.  Format the output sequence as space-separated digits.
```python
import re
from typing import List

"""
Transforms a sequence of space-separated single-digit integers.
It identifies contiguous blocks (runs) of identical non-zero digits.
If a run of a non-zero digit has a length of 3 or more, the first and last digits
of the run are kept, and all digits in between are replaced with '0'.
Runs of non-zero digits with length 1 or 2, and all runs of '0's, remain unchanged.
The overall length of the sequence is preserved.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing the transformed space-separated sequence.
    """
    # Parse the input string into a list of digit strings
    digits = input_str.split(' ')
    n = len(digits)
    output_digits = []
    i = 0

    # Iterate through the digits to find blocks
    while i < n:
        current_digit = digits[i]
        # Find the end of the current block of identical digits
        j = i + 1
        while j < n and digits[j] == current_digit:
            j += 1

        # Calculate the length of the block
        block_length = j - i
        block = digits[i:j]

        # Apply transformation logic based on the digit and block length
        if current_digit == '0':
            # Keep blocks of '0's as they are
            output_digits.extend(block)
        else:
            # Handle non-zero blocks
            if block_length < 3:
                # Keep short blocks (length 1 or 2) as they are
                output_digits.extend(block)
            else:
                # Modify blocks of length 3 or more
                # Keep the first digit
                output_digits.append(current_digit)
                # Add '0's in the middle
                output_digits.extend(['0'] * (block_length - 2))
                # Keep the last digit
                output_digits.append(current_digit)

        # Move the index to the start of the next block
        i = j

    # Join the processed digits back into a space-separated string
    return ' '.join(output_digits)

```
