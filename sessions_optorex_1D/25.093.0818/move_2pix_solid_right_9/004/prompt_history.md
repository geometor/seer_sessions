
## train_1

**input:**
```
6 6 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
4 4 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 4 4 4 4 4 0 0
```


**output:**
```
0 0 0 0 0 0 0 4 4 4 4 4
```


## train_4

**input:**
```
0 9 9 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 9 9 9 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 8 8 8 8 8 8 0 0 0
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 8 0
```


## train_6

**input:**
```
0 0 0 5 5 5 5 5 5 5 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 5 5
```


## train_7

**input:**
```
0 0 0 0 0 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 7 7 7 0 0
```

## Perception

The input and output are both sequences (lists or arrays) of integers.
Each sequence consists primarily of zeros (0) and a single contiguous block of identical non-zero digits (e.g., `6 6`, `4 4 4`, `9 9 9`).
The transformation involves relocating this contiguous block of non-zero digits within the sequence.
By comparing the starting position of the non-zero block in the input to its starting position in the output, it's evident that the block is consistently shifted two positions to the right.
The positions vacated by the block become zeros, and the overall length of the sequence remains unchanged.

## Facts


```yaml
objects:
  - name: sequence
    type: list_of_integers
    properties:
      - contains_zeros: true
      - contains_non_zero_block: true
  - name: non_zero_block
    type: sublist_of_integers
    properties:
      - contiguous: true
      - elements_are_identical: true
      - elements_are_non_zero: true
    location:
      - property: start_index_input
      - property: end_index_input
      - property: start_index_output
      - property: end_index_output
  - name: background
    type: integer
    value: 0

actions:
  - name: shift_block
    target: non_zero_block
    properties:
      - direction: right
      - amount: 2_positions

relationships:
  - type: transformation
    from: sequence_input
    to: sequence_output
    rule: shift_non_zero_block_right_by_2
  - type: positional_change
    object: non_zero_block
    details: start_index_output = start_index_input + 2
```


## Natural Language Program

1.  Identify the input sequence of integers.
2.  Locate the contiguous block of identical non-zero integers within the input sequence. Determine its starting and ending indices.
3.  Create a new output sequence of the same length as the input sequence, initially filled with zeros.
4.  Copy the identified non-zero block from the input sequence into the output sequence, placing its starting element at an index two positions greater than its original starting index in the input sequence.
```python
import re # Using regex can simplify finding the block

"""
Identifies a contiguous block of identical non-zero integers within an input sequence 
and shifts this block two positions to the right, filling the vacated positions and 
any other positions with zeros, maintaining the original sequence length.
"""

def find_non_zero_block(int_list):
    """
    Finds the start index, end index, and value of the first contiguous 
    block of identical non-zero numbers in a list.

    Args:
        int_list: A list of integers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (-1, -1, 0).
    """
    start_index = -1
    end_index = -1
    value = 0
    in_block = False

    for i, num in enumerate(int_list):
        if num != 0:
            if not in_block:
                # Start of a potential block
                start_index = i
                value = num
                end_index = i # Initialize end index
                in_block = True
            elif num == value:
                # Continue the current block
                end_index = i
            else:
                 # Found a different non-zero number, stop (shouldn't happen per examples)
                 # Or could be the start of a *new* block if requirements change
                 break 
        elif in_block:
            # Found a zero after starting a block, the block ends at the previous index
            break
            
    if start_index != -1:
        return start_index, end_index, value
    else:
        # No non-zero block found
        return -1, -1, 0

def transform(input_str):
    """
    Transforms the input sequence string by shifting the non-zero block.

    Args:
        input_str: A string representing a space-separated sequence of integers.

    Returns:
        A string representing the transformed space-separated sequence.
    """
    # Parse the input string into a list of integers
    try:
        input_list = [int(x) for x in input_str.split()]
    except ValueError:
        # Handle potential errors if input is not formatted correctly
        print("Error: Input string contains non-integer values.")
        return "" # Or raise an exception

    list_len = len(input_list)
    
    # Initialize the output list with zeros
    output_list = [0] * list_len

    # Find the non-zero block in the input list
    start_index, end_index, value = find_non_zero_block(input_list)

    # If a block was found, proceed with the shift
    if start_index != -1:
        # Calculate the length of the block
        block_length = end_index - start_index + 1
        
        # Calculate the new starting position for the block
        new_start_index = start_index + 2

        # Place the block into the output list at the new position
        for i in range(block_length):
            target_index = new_start_index + i
            # Ensure the target index is within the bounds of the list
            if 0 <= target_index < list_len:
                output_list[target_index] = value
            # If the shift pushes part of the block beyond the end, it's truncated (based on examples)

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str

```
```python
import numpy as np

"""
Identifies a contiguous block of identical non-zero integers within an input array 
and shifts this block two positions to the right within a new array of the same size, 
filling all other positions with zeros.
"""

def find_non_zero_block(int_array):
    """
    Finds the start index, end index, and value of the first contiguous 
    block of identical non-zero numbers in a 1D NumPy array.

    Args:
        int_array: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (-1, -1, 0). Returns the first block found if multiple exist,
        although examples suggest only one exists.
    """
    start_index = -1
    end_index = -1
    value = 0
    in_block = False

    for i, num in enumerate(int_array):
        if num != 0:
            if not in_block:
                # Start of a potential block
                start_index = i
                value = num
                end_index = i # Initialize end index
                in_block = True
            elif num == value:
                # Continue the current block
                end_index = i
            else:
                 # Found a different non-zero number, the first block ends here.
                 # Based on examples, this condition might not be strictly necessary
                 # as there's only one block type per example, but good for robustness.
                 break 
        elif in_block:
            # Found a zero after starting a block, the block ends at the previous index
            break
            
    if start_index != -1:
        return start_index, end_index, value
    else:
        # No non-zero block found
        return -1, -1, 0

def transform(input_grid):
    """
    Transforms the input array by shifting the non-zero block.

    Args:
        input_grid: A 1D NumPy array representing the sequence of integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a numpy array (might be redundant if framework guarantees it)
    input_array = np.array(input_grid)
    
    # Get the length of the input array
    array_len = len(input_array)
    
    # Initialize the output array with zeros
    output_grid = np.zeros(array_len, dtype=input_array.dtype)

    # Find the non-zero block in the input array
    start_index, end_index, value = find_non_zero_block(input_array)

    # If a block was found, proceed with the shift
    if start_index != -1:
        # Calculate the length of the block
        block_length = end_index - start_index + 1
        
        # Calculate the new starting position for the block
        new_start_index = start_index + 2

        # Place the block into the output array at the new position
        # Iterate through the indices of the original block
        for i in range(block_length):
            # Calculate the corresponding target index in the output array
            target_index = new_start_index + i
            
            # Check if the target index is within the bounds of the output array
            if 0 <= target_index < array_len:
                # If within bounds, copy the value to the output array
                output_grid[target_index] = value
            # If the target index is out of bounds (shifted off the end), 
            # the value is implicitly not copied (output remains 0), achieving truncation.

    # Return the transformed array
    return output_grid
```
