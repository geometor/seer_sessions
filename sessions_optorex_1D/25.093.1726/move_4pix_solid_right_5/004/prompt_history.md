
## train_1

**input:**
```
0 0 0 9 9 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 9 9 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 3 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 3 3
```


## train_3

**input:**
```
0 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 4 4
```


## train_4

**input:**
```
3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 3 3 3 3 3 3 0
```


## train_5

**input:**
```
0 0 0 0 0 0 8 8 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 8 8
```


## train_6

**input:**
```
0 0 0 0 1 1 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 1 0 0
```


## train_7

**input:**
```
0 0 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 8 8 8 8 0
```

*   **Perception:** The input and output are one-dimensional sequences (lists or arrays) of integers, all having the same length (12 elements). Each input sequence consists mostly of zeros ('0') and one contiguous block of identical non-zero digits (e.g., '9 9 9', '3 3', '4 4 4 4 4 4 4'). The output sequence contains the same block of non-zero digits, but shifted to a different position within the sequence, with the remaining positions filled with zeros. The key transformation is the relocation of this non-zero block. By comparing the starting index of the block in the input and output, it appears the block is consistently shifted 4 positions to the right.

*   **Facts:**
    
```yaml
    task_type: sequence_transformation
    input_data:
      type: list_of_integers
      length: 12
      elements:
        - type: zero (background)
        - type: contiguous_block
          properties:
            - digits_are_identical
            - digit_value: non-zero_integer (varies per example)
            - length: variable (varies per example)
            - position: variable (varies per example)
    output_data:
      type: list_of_integers
      length: 12
      elements:
        - type: zero (background)
        - type: contiguous_block (same as input)
          properties:
            - position: shifted_right_by_4
    transformation:
      action: shift_block
      direction: right
      amount: 4_positions
      details: The contiguous block of non-zero identical digits is moved 4 positions to the right. The original positions occupied by the block, and any positions not occupied by the shifted block in the output, are filled with zeros.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous sub-sequence within the input list consisting of identical non-zero digits (the "block"). Note its starting index, length, and the value of the digit.
    2.  Create a new list of the same length as the input list, initialized entirely with zeros.
    3.  Calculate the new starting index for the block by adding 4 to its original starting index in the input list.
    4.  Place the identified block (using its original digit value and length) into the new list, starting at the calculated new starting index.
    5.  The resulting list is the output.
```python
import numpy as np
from typing import List

"""
Identifies a contiguous block of identical non-zero digits in the input list, 
determines its start index, length, and digit value. Creates a new list of 
the same size initialized with zeros. Calculates the new start index by adding 
4 to the original start index. Places the identified block into the new list 
at the calculated new start index.
"""

def find_contiguous_block(data: List[int]):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        data: The input list of integers.

    Returns:
        A tuple containing (start_index, length, value) of the block,
        or (None, 0, None) if no such block is found.
    """
    start_index = None
    length = 0
    value = None
    in_block = False

    for i, digit in enumerate(data):
        if not in_block and digit != 0:
            # Start of a potential block
            start_index = i
            value = digit
            length = 1
            in_block = True
        elif in_block:
            if digit == value:
                # Continue the block
                length += 1
            else:
                # End of the block
                return start_index, length, value
    
    # Handle case where block goes to the end of the list
    if in_block:
        return start_index, length, value

    # No block found
    return None, 0, None

def transform(input_list: List[int]) -> List[int]:
    """
    Shifts a contiguous block of identical non-zero digits 4 positions to the right.

    Args:
        input_list: A list of 12 integers containing zeros and one contiguous block
                   of identical non-zero digits.

    Returns:
        A new list of 12 integers where the block has been shifted 4 positions
        to the right, and other positions are filled with zeros.
    """
    list_length = len(input_list)
    # Initialize output_list with zeros
    output_list = [0] * list_length

    # Find the contiguous block in the input list
    start_index, length, value = find_contiguous_block(input_list)

    # If a block was found
    if start_index is not None:
        # Calculate the new starting index for the block
        new_start_index = start_index + 4

        # Place the block into the output list at the new position
        # Ensure the placement does not go out of bounds (though examples don't show this)
        for i in range(length):
            target_index = new_start_index + i
            if 0 <= target_index < list_length:
                output_list[target_index] = value

    return output_list

```
```python
"""
Accepts a 1D NumPy array of 12 integers. Finds the unique contiguous block of 
identical non-zero digits within the input array. Creates a new 1D NumPy array 
of length 12, initialized to zeros. Calculates the target starting position 
for the block by adding 4 to its original starting position. Copies the block 
(same value and length) into the new array at the target position, respecting 
array boundaries. Returns the new array.
"""

import numpy as np

def find_contiguous_block(data: np.ndarray):
    """
    Finds the first contiguous block of identical non-zero digits in a 1D NumPy array.

    Args:
        data: The input 1D NumPy array of integers.

    Returns:
        A tuple containing (start_index, length, value) of the block.
        Returns (-1, 0, 0) if no such block is found or the array is empty.
        start_index is -1 if no block is found.
    """
    start_index = -1
    length = 0
    value = 0
    if data.size == 0: # Handle empty array case
        return start_index, length, value

    in_block = False
    for i, digit in enumerate(data):
        # Use .item() to get Python scalar for comparison if needed,
        # though direct numpy comparison often works. Assuming direct comparison is ok.
        if not in_block and digit != 0:
            # Start of a potential block
            start_index = i
            value = digit
            length = 1
            in_block = True
        elif in_block:
            if digit == value:
                # Continue the block
                length += 1
            else:
                # End of the block found before end of array
                return start_index, length, value # Return immediately when block ends

    # Handle case where block goes to the end of the list or no block found
    if in_block:
        return start_index, length, value
    else:
        # No block found throughout the array
        return -1, 0, 0


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts a contiguous block of identical non-zero digits 4 positions to the right.

    Args:
        input_grid: A 1D NumPy array of 12 integers containing zeros and one 
                    contiguous block of identical non-zero digits.

    Returns:
        A new 1D NumPy array of 12 integers where the block has been shifted 
        4 positions to the right, and other positions are filled with zeros.
    """
    # Get the size of the input array
    grid_length = input_grid.shape[0]

    # Initialize output_grid with zeros, matching input size and type
    output_grid = np.zeros_like(input_grid)

    # Find the contiguous block in the input grid
    start_index, length, value = find_contiguous_block(input_grid)

    # Proceed only if a valid block was found (start_index is not -1)
    if start_index != -1:
        # Calculate the new starting index for the block by adding 4
        new_start_index = start_index + 4

        # Place the block into the output grid at the new position
        # Loop through the length of the identified block
        for i in range(length):
            # Calculate the target index in the output grid
            target_index = new_start_index + i
            
            # Check if the target index is within the valid bounds of the output grid
            if 0 <= target_index < grid_length:
                # Assign the block's value to the corresponding position in the output grid
                output_grid[target_index] = value

    # Return the modified output grid
    return output_grid
```
