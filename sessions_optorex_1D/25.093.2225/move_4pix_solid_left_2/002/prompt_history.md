
## train_1

**input:**
```
0 0 0 0 0 0 0 0 5 5 5 0
```


**output:**
```
0 0 0 0 5 5 5 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 9 9 9 9 0 0 0 0
```


**output:**
```
9 9 9 9 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 7 7 7
```


**output:**
```
0 0 0 0 0 7 7 7 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 3 3 0 0 0
```


**output:**
```
0 0 0 3 3 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 6
```


**output:**
```
0 0 0 0 0 0 0 6 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 7 7 7 7 7 7 0
```


**output:**
```
0 7 7 7 7 7 7 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 5 5 5 5 5 5 5 0
```


**output:**
```
5 5 5 5 5 5 5 0 0 0 0 0
```

**Perception of Elements:**

The task involves manipulating sequences of digits. Each input and output is a string of 12 digits separated by spaces. The core element within each sequence is a contiguous block of identical non-zero digits, surrounded by zeros. The transformation rule consistently alters the position of this non-zero block within the sequence, while keeping the block's content (the specific digit and its repetition count) and the overall sequence length unchanged. The surrounding elements are always zeros.

**Facts:**


```yaml
Task: Shift a block of non-zero digits within a fixed-length sequence.

Input:
  Type: String
  Format: Space-separated sequence of 12 digits.
  Content: Contains a single contiguous block of identical non-zero digits, padded with zeros.
  Example_Structure: '0 ... 0 X X ... X 0 ... 0' where X is a non-zero digit.

Output:
  Type: String
  Format: Space-separated sequence of 12 digits.
  Content: The non-zero block from the input, shifted to a new position, padded with zeros.

Objects:
  - Name: Sequence
    Properties:
      - Type: List of integers (derived from input/output string)
      - Length: 12
  - Name: NonZeroBlock
    Properties:
      - Type: Sub-sequence of identical non-zero integers
      - Digit: The non-zero digit composing the block (e.g., 5, 9, 7)
      - Length: Number of times the digit repeats (variable)
      - Position: Start and end indices within the sequence.

Action:
  - Name: ShiftLeft
  - Target: NonZeroBlock
  - Parameter: ShiftAmount = 4 positions
  - Description: The start index of the NonZeroBlock in the output sequence is 4 less than its start index in the input sequence.

Relationships:
  - The output sequence is a transformation of the input sequence.
  - The NonZeroBlock's digit and length are preserved from input to output.
  - The position of the NonZeroBlock changes predictably (shifted left by 4).
  - Zeros fill the positions not occupied by the shifted NonZeroBlock.
```


**Natural Language Program:**

1.  Read the input string and convert it into a list of 12 integers.
2.  Identify the contiguous block of identical non-zero digits within the list. Record the non-zero digit itself, the length of the block, and its starting index in the input list.
3.  Create a new list of 12 integers, initializing all elements to zero.
4.  Calculate the target starting index for the non-zero block in the new list by subtracting 4 from its starting index in the original input list.
5.  Place the identified non-zero block (using the recorded digit and length) into the new list, starting at the calculated target index.
6.  Convert the new list of integers back into a space-separated string to produce the output.
```python
import re # Using regex to find the block might be slightly cleaner

"""
Identifies a contiguous block of identical non-zero digits within a 12-element sequence of space-separated digits. 
Shifts this block 4 positions to the left, preserving the block's digit and length. 
Fills the remaining positions with zeros. 
Outputs the resulting sequence as a space-separated string.
"""

def _parse_input(input_str: str) -> list[int]:
    """Converts the space-separated input string into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def _find_non_zero_block(data: list[int]) -> tuple[int | None, int, int]:
    """
    Finds the first contiguous block of identical non-zero digits.
    Returns the digit, its count (length), and the starting index.
    Returns (None, 0, -1) if no block is found.
    """
    start_index = -1
    block_digit = None
    block_length = 0

    for i, digit in enumerate(data):
        if digit != 0:
            if block_digit is None: # Start of a potential block
                block_digit = digit
                start_index = i
                block_length = 1
            elif digit == block_digit: # Continuing the block
                block_length += 1
            else: # Found a different non-zero digit, should not happen based on examples
                # Or end of the block if the previous was the block digit
                if data[i-1] == block_digit:
                    break # Found the end of the block we were tracking
                else: # This case implies adjacent different non-zero digits, reset
                     block_digit = digit
                     start_index = i
                     block_length = 1

        elif block_digit is not None: # Found a zero after a block started
            break # End of the block

    if block_digit is None:
        return None, 0, -1 # No non-zero block found

    return block_digit, block_length, start_index


def _format_output(output_list: list[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))


def transform(input_str: str) -> str:
    """
    Transforms the input sequence by shifting the non-zero block 4 positions to the left.

    Args:
        input_str: A string representing the input sequence (e.g., "0 0 0 0 5 5 5 0 0 0 0 0").

    Returns:
        A string representing the transformed sequence.
    """
    # 1. Read the input string and convert it into a list of 12 integers.
    input_list = _parse_input(input_str)
    n = len(input_list) # Should be 12 based on examples

    # 2. Identify the contiguous block of identical non-zero digits.
    block_digit, block_length, start_index = _find_non_zero_block(input_list)

    # Handle case where no block is found (though not expected based on examples)
    if block_digit is None:
        return input_str # Or return "0 " * n trimmed? Stick to input format.

    # 3. Create a new list of 12 integers, initializing all elements to zero.
    output_list = [0] * n

    # 4. Calculate the target starting index for the non-zero block.
    # Subtract 4 from its starting index in the original input list.
    # Ensure the index doesn't go below 0, although examples don't show this edge case.
    target_start_index = max(0, start_index - 4)

    # 5. Place the identified non-zero block into the new list.
    for i in range(block_length):
        # Check bounds to prevent errors if the shift causes overrun (unlikely with length 12 and shift 4)
        if target_start_index + i < n:
            output_list[target_start_index + i] = block_digit

    # 6. Convert the new list of integers back into a space-separated string.
    output_str = _format_output(output_list)

    return output_str
```
