
## train_1

**input:**
```
0 9 9 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 9 9 9 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 5 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 5 5 0
```


## train_3

**input:**
```
0 0 1 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 4 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 4 0 0
```


## train_5

**input:**
```
0 0 0 0 0 6 6 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 6 6 6
```


## train_6

**input:**
```
0 0 0 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 0 0 0 0
```


## train_7

**input:**
```
0 4 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 0 0
```

## Perception

The input consists of a sequence of 12 single-digit integers. The sequence is characterized by containing mostly zeros and a single contiguous block of identical non-zero digits. The length of this non-zero block varies across examples.

The output is also a sequence of 12 single-digit integers. It retains the same non-zero digits and the same number of zeros as the input. The key difference is the position of the non-zero block.

The transformation involves identifying the contiguous block of non-zero digits in the input sequence and shifting this entire block exactly 4 positions to the right. The positions originally occupied by the block become zeros, and the positions where the block moves to adopt the non-zero digit values. All other zero positions remain unchanged.

## Facts


```yaml
objects:
  - name: sequence
    type: list
    properties:
      - length: 12
      - elements: single-digit integers (0-9)
  - name: non_zero_block
    type: sub-sequence
    properties:
      - elements: identical non-zero digits
      - contiguous: true
      - location: variable within the input sequence
      - length: variable (1 or more)
  - name: zero_elements
    type: integer
    value: 0
    role: padding/background

actions:
  - name: identify_block
    actor: system
    input: input sequence
    output: non_zero_block (value, start_index, end_index)
  - name: shift_block
    actor: system
    object: non_zero_block
    properties:
      - direction: right
      - distance: 4 positions
  - name: generate_output
    actor: system
    input:
      - input sequence
      - identified non_zero_block
      - shift parameters (direction=right, distance=4)
    output: output sequence
    process: Create a new sequence of the same length filled with zeros, then place the non_zero_block at the new shifted position.

relationships:
  - type: positional_change
    subject: non_zero_block
    details: The start and end indices of the non_zero_block increase by 4 from input to output.
  - type: value_preservation
    subject: non_zero_block
    details: The digits and length of the non_zero_block remain the same between input and output.
  - type: structure_preservation
    subject: sequence
    details: The length of the sequence (12) remains the same between input and output.
```


## Natural Language Program

1.  Receive the input sequence of 12 integers.
2.  Identify the contiguous sub-sequence composed of identical non-zero digits (the "block"). Record the value of the digit, the starting index, and the ending index of this block.
3.  Create a new output sequence of 12 integers, initially filled with zeros.
4.  Calculate the new starting index for the block by adding 4 to the original starting index.
5.  Calculate the new ending index for the block by adding 4 to the original ending index.
6.  Place the identified block (using its original digit value and length) into the output sequence starting at the new starting index and ending at the new ending index.
7.  Return the resulting output sequence.
```python
import collections

"""
Identifies a contiguous block of identical non-zero digits in a 12-element list 
and shifts this block 4 positions to the right, filling the original positions 
and other positions with zeros.
"""

# No external imports needed beyond standard Python collections/types if necessary.

def find_non_zero_block(input_list):
    """
    Helper function to find the first contiguous block of identical non-zero digits.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple (block_val, start_index, block_length) if a block is found,
        otherwise (None, -1, 0).
    """
    start_index = -1
    block_val = 0
    block_length = 0
    n = len(input_list)

    for i in range(n):
        # Find the start of the first non-zero sequence
        if input_list[i] != 0:
            start_index = i
            block_val = input_list[i]
            block_length = 1
            # Continue checking for the same value to find the length/end
            for j in range(i + 1, n):
                if input_list[j] == block_val:
                    block_length += 1
                else:
                    # Block ends here as the value changed or became zero
                    break
            # Found the first block, so we can stop searching
            break 
            
    if start_index != -1:
        return block_val, start_index, block_length
    else:
        # No non-zero block found
        return None, -1, 0

def transform(input_grid):
    """
    Transforms the input grid (list of 12 integers) by identifying the 
    contiguous block of non-zero identical digits and shifting it 4 positions 
    to the right.

    Args:
        input_grid: A list of 12 integers.

    Returns:
        A list of 12 integers representing the transformed grid.
    """
    # Determine the size of the grid (assumed fixed based on examples)
    n = 12 
    if len(input_grid) != n:
        # Handle potential size mismatch if necessary, though examples are fixed size
        # For now, assume input is always length 12
        pass 

    # Initialize the output grid with zeros
    output_grid = [0] * n

    # 1. Identify the non-zero block using the helper function
    block_val, start_index, block_length = find_non_zero_block(input_grid)

    # 2. If a block was found, calculate its new position and place it
    if block_val is not None: # Check if a block was actually found (block_val is not None)
        
        # Calculate the new starting index for the block
        # The shift distance is fixed at 4 positions to the right
        shift_distance = 4
        new_start_index = start_index + shift_distance
        
        # Place the identified block into the output sequence at the new position
        # We iterate for the determined length of the block
        for i in range(block_length):
            # Calculate the target index in the output grid
            target_index = new_start_index + i
            
            # Ensure the target index is within the bounds of the output grid
            # Based on examples, the shifted block always fits
            if target_index < n:
                 output_grid[target_index] = block_val
            # else: # This case doesn't seem to occur in the provided examples
                 # print(f"Warning: Block element at index {target_index} out of bounds")
                 # pass

    # 3. Return the resulting output sequence
    # If no block was found, the output_grid remains all zeros, which is correct
    return output_grid

```
```python
import collections

"""
Identifies the single contiguous block of identical non-zero digits in a 
12-element input list and shifts this block exactly 4 positions to the right 
to create the output list. All other positions in the output list are zeros.
"""

# No external imports needed beyond standard Python collections/types if necessary.

def find_non_zero_block(input_list):
    """
    Helper function to find the first contiguous block of identical non-zero digits.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple (block_val, start_index, block_length) if a block is found,
        otherwise (None, -1, 0).
    """
    start_index = -1
    block_val = 0
    block_length = 0
    n = len(input_list)

    # Search for the start of the first non-zero sequence
    for i in range(n):
        if input_list[i] != 0:
            start_index = i
            block_val = input_list[i]
            block_length = 1
            # Continue checking for the same value to find the length/end of the block
            for j in range(i + 1, n):
                if input_list[j] == block_val:
                    block_length += 1
                else:
                    # Block ends here as the value changed or became zero
                    break
            # Found the first block, so we can stop the outer search
            break 
            
    if start_index != -1:
        # A block was found
        return block_val, start_index, block_length
    else:
        # No non-zero block found in the input list
        return None, -1, 0

def transform(input_grid):
    """
    Transforms the input grid (list of 12 integers) by identifying the 
    contiguous block of non-zero identical digits and shifting it 4 positions 
    to the right.

    Args:
        input_grid: A list of 12 integers.

    Returns:
        A list of 12 integers representing the transformed grid.
    """
    # Define the fixed parameters based on observations
    sequence_length = 12 
    shift_distance = 4

    # Initialize the output grid with zeros
    output_grid = [0] * sequence_length

    # Step 1: Find the non-zero block in the input grid
    block_val, start_index, block_length = find_non_zero_block(input_grid)

    # Step 2: If a block was successfully found, proceed to shift it
    if block_val is not None: 
        
        # Step 3: Calculate the new starting index for the block in the output grid
        new_start_index = start_index + shift_distance
        
        # Step 4: Place the identified block into the output sequence at the new position
        # Iterate for the determined length of the block
        for i in range(block_length):
            # Calculate the target index in the output grid for the current element of the block
            target_index = new_start_index + i
            
            # Ensure the target index is within the bounds of the output grid
            # (Although based on examples, the shifted block always fits)
            if 0 <= target_index < sequence_length:
                 output_grid[target_index] = block_val
            # else: # Handle edge case if block shifts out of bounds (not observed here)
                 # pass 

    # Step 5: Return the resulting output sequence
    # If no block was found in Step 1, the output_grid remains all zeros, which is correct.
    return output_grid
```
