
## train_1

**input:**
```
5 5 5 5 5 5 5 5 2 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 5 2 0 0 0
```


## train_2

**input:**
```
0 0 4 4 4 4 4 4 4 4 4 2
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 4 2
```


## train_3

**input:**
```
9 9 9 9 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 9 2 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 6 6 6 6 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 6 2
```


## train_5

**input:**
```
0 0 0 6 6 6 6 6 2 0 0 0
```


**output:**
```
0 0 0 6 6 6 6 6 2 0 0 0
```


## train_6

**input:**
```
0 0 0 2 0 0 0 0 5 5 5 5
```


**output:**
```
0 0 0 2 5 5 5 5 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 4 4 4 2 0
```


**output:**
```
0 0 0 0 0 0 0 4 4 4 2 0
```

*   **Perception of Elements:**
    *   The input and output are sequences of 12 single-digit integers.
    *   The digits '0' and '2' appear to have special roles. '0' acts as a filler or space, and '2' appears to be a fixed anchor point.
    *   Each input contains a single contiguous block of identical non-zero digits (other than '2'). For example, `5 5 5 5 5 5 5 5` in `train_1`, `4 4 4 4 4 4 4 4 4` in `train_2`, `9 9 9 9` in `train_3`.
    *   The transformation involves potentially repositioning this block of non-zero digits relative to the '2'.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          - type: list of integers
          - length: 12
      - object: digit_zero
        properties:
          - value: 0
          - role: filler/space, movable
      - object: digit_two
        properties:
          - value: 2
          - role: anchor/pivot, fixed position relative to other non-zero blocks
      - object: digit_block
        properties:
          - type: contiguous sequence of identical digits
          - value: non-zero, not equal to 2
          - count_per_input: 1
          - role: primary movable element
    relationships:
      - type: spatial
        between: [digit_block, digit_two]
        description: The block can be to the left or right of the '2'.
      - type: separation
        between: [digit_block, digit_two]
        medium: digit_zero
        description: Zeroes may exist between the block and the '2'.
    action:
      - type: conditional_swap
        condition: Zeros exist between the digit_block and digit_two.
        elements_involved: [digit_block, sequence of digit_zero between block and two]
        effect: The digit_block and the intermediate sequence of zeros swap positions, moving the block adjacent to the '2'.
        directionality: The block moves towards the '2'.
    invariants:
      - The position of '2' relative to the start/end of the sequence if no swap happens.
      - The position of '2' relative to the *other* digits (not involved in the block or the intermediate zeros) remains the same.
      - The order and values of digits within the `digit_block` remain unchanged.
      - The total count of each digit remains the same.
      - The length of the sequence remains 12.
    ```


*   **Natural Language Program:**
    1.  Identify the single occurrence of the digit '2' and its index within the input sequence.
    2.  Identify the contiguous block of identical digits that are not '0' and not '2'. Record its starting index, ending index, and the digit value.
    3.  Determine if this block is located to the left or right of the '2'.
    4.  If the block is to the left of '2':
        *   Check if all elements between the end of the block (exclusive) and the index of '2' (exclusive) are '0'.
        *   If yes, and if there is at least one such '0', perform a swap: Move the identified block of digits immediately to the left of '2', and move the sequence of intermediate '0's to the original starting position of the block.
    5.  If the block is to the right of '2':
        *   Check if all elements between the index of '2' (exclusive) and the start of the block (exclusive) are '0'.
        *   If yes, and if there is at least one such '0', perform a swap: Move the identified block of digits immediately to the right of '2', and move the sequence of intermediate '0's to the position immediately following the block's original end position.
    6.  If no intermediate '0's exist between the block and '2' (i.e., they are adjacent or separated only by other non-zero numbers not part of the block), make no changes to the sequence.
    7.  Return the potentially modified sequence.
```python
import re
from typing import List, Tuple, Optional

"""
Identifies the location of the digit '2' and a contiguous block of identical digits (not '0' or '2').
If there is a sequence composed entirely of '0's between the block and '2', swaps the block and the sequence of '0's, moving the block adjacent to '2'.
If the block is already adjacent to '2', or if the space between them contains non-zero digits (other than the block itself), no changes are made.
"""

def find_digit_index(data: List[int], digit: int) -> Optional[int]:
    """Finds the index of the first occurrence of a digit."""
    try:
        return data.index(digit)
    except ValueError:
        return None

def find_digit_block(data: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous block of identical digits that are not 0 or 2.
    Returns (digit_value, start_index, end_index) or None if not found.
    """
    block_digit = -1
    start_index = -1
    end_index = -1
    in_block = False

    for i, digit in enumerate(data):
        if digit != 0 and digit != 2:
            if not in_block:
                # Start of a potential block
                block_digit = digit
                start_index = i
                in_block = True
            elif digit == block_digit:
                # Continue the current block
                pass
            else:
                # Found a different non-zero/non-2 digit, meaning the previous block ended
                end_index = i - 1
                return block_digit, start_index, end_index
        elif in_block:
            # End of the block detected (found 0 or 2)
            end_index = i - 1
            return block_digit, start_index, end_index

    # Handle case where block goes to the end of the list
    if in_block:
        end_index = len(data) - 1
        return block_digit, start_index, end_index

    return None # No block found

def is_all_zeros(sub_list: List[int]) -> bool:
    """Checks if a list contains only zeros."""
    if not sub_list: # Empty list doesn't count as all zeros for swapping purpose
        return False
    return all(digit == 0 for digit in sub_list)

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    1. Parses the input string into a list of integers.
    2. Finds the index of '2'.
    3. Finds the contiguous block of identical non-zero, non-'2' digits.
    4. Checks if intermediate zeros exist between the block and '2'.
    5. If yes, swaps the block and the zeros.
    6. Returns the transformed sequence as a string.
    """
    # Parse input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    output_list = list(input_list) # Start with a copy

    # Find the index of '2'
    two_index = find_digit_index(output_list, 2)
    if two_index is None:
        # Should not happen based on examples, but handle defensively
        return input_str # Return original if '2' is missing

    # Find the digit block
    block_info = find_digit_block(output_list)
    if block_info is None:
         # Should not happen based on examples, but handle defensively
        return input_str # Return original if block is missing

    block_digit, block_start, block_end = block_info
    block_len = block_end - block_start + 1

    # Determine relative position and check for intermediate zeros
    if block_end < two_index:
        # Case: Block is to the left of '2'
        intermediate_slice = output_list[block_end + 1 : two_index]
        
        # Check if the intermediate slice consists only of zeros and is not empty
        if is_all_zeros(intermediate_slice):
            # Perform swap: Move block next to '2', zeros to block's original start
            zeros_slice = intermediate_slice
            block_slice = output_list[block_start : block_end + 1]
            
            # Reconstruct the list
            new_list = (output_list[:block_start] + 
                        zeros_slice + 
                        block_slice + 
                        output_list[two_index:])
            output_list = new_list
            
    elif block_start > two_index:
        # Case: Block is to the right of '2'
        intermediate_slice = output_list[two_index + 1 : block_start]

        # Check if the intermediate slice consists only of zeros and is not empty
        if is_all_zeros(intermediate_slice):
            # Perform swap: Move block next to '2', zeros after block's original end
            zeros_slice = intermediate_slice
            block_slice = output_list[block_start : block_end + 1]

            # Reconstruct the list
            new_list = (output_list[:two_index + 1] +
                        block_slice +
                        zeros_slice +
                        output_list[block_end + 1:])
            output_list = new_list

    # Else (block is adjacent to '2' or separated by non-zeros): No change needed

    # Format output list back into a string
    return " ".join(map(str, output_list))

```
