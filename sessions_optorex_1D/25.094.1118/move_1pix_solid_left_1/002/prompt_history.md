
## train_1

**input:**
```
0 2 2 2 2 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 8 8 8 8 8 0 0 0 0
```


**output:**
```
0 0 8 8 8 8 8 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 5 5 5 5 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 5 0 0 0 0 0 0
```


## train_5

**input:**
```
0 7 7 7 7 7 7 7 7 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 0 0 0 0
```


## train_6

**input:**
```
0 5 5 5 5 5 5 5 0 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 6 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are sequences (lists) of single-digit integers.
    *   Each sequence has a fixed length (12 in all examples).
    *   Each input sequence contains a contiguous block of identical non-zero digits. The rest of the elements are zeros.
    *   The output sequence is related to the input sequence by a positional shift of the non-zero block.

*   **YAML Facts:**
    
```yaml
    task_description: Shift the first contiguous block of identical non-zero digits one position to the left within a fixed-length list of integers.
    
    elements:
      - name: sequence
        type: list of integers
        properties:
          - length: fixed (e.g., 12)
          - contains: single-digit integers (0-9)
      - name: non_zero_block
        type: contiguous sub-sequence
        properties:
          - elements: identical non-zero integers
          - location: surrounded by zeros or list boundaries
      - name: zero
        type: integer
        value: 0
        role: padding element, background element
    
    actions:
      - name: identify_first_non_zero_block
        input: sequence
        output: start_index, end_index, block_value
      - name: shift_left
        input: sequence, start_index, end_index
        output: modified_sequence
        details: Moves the elements from start_index to end_index one position to the left.
      - name: pad_end
        input: sequence
        output: modified_sequence
        details: Appends a zero to the end if necessary to maintain original length after shift.
    
    relationships:
      - The output sequence is a transformation of the input sequence.
      - The non_zero_block in the output sequence starts one position earlier (index-1) than in the input sequence.
      - The length of the input and output sequences is identical.
      - The values within the non_zero_block remain unchanged.
      - The relative order of zeros outside the shifted block is maintained, except for the zero potentially displaced by the shift and the zero added at the end.
    ```


*   **Natural Language Program:**
    1.  Receive the input list of integers.
    2.  Find the starting index of the first non-zero element in the list. If no non-zero element exists, return the original list.
    3.  Identify the value of this first non-zero element.
    4.  Determine the end index of the contiguous block of elements that have this same non-zero value, starting from the found starting index.
    5.  Create a new list of the same length as the input list, initially filled with zeros.
    6.  Copy the identified block of non-zero elements into the new list, starting at an index one less than the original starting index.
    7.  Return the new list.
```python
"""
Transforms an input list of integers by finding the first contiguous block of 
identical non-zero digits and shifting this block one position to the left. 
The list maintains its original length, and positions outside the shifted 
block are filled with zeros in the output.
"""

import math

def find_first_block(data):
    """
    Finds the start index, end index (exclusive), and value of the first 
    contiguous block of identical non-zero numbers.

    Args:
        data: A list of numbers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (None, None, None).
    """
    start_index = -1
    block_value = None
    n = len(data)

    # Find the start of the block and its value
    for i in range(n):
        if data[i] != 0:
            start_index = i
            block_value = data[i]
            break

    # If no non-zero element found, no block exists
    if start_index == -1:
        return None, None, None

    # Find the end of the block (index after the last element)
    end_index = start_index + 1
    while end_index < n and data[end_index] == block_value:
        end_index += 1

    return start_index, end_index, block_value

def transform(input_grid):
    """
    Shifts the first contiguous block of identical non-zero digits 
    one position to the left within the list.

    Args:
        input_grid: A list of integers.

    Returns:
        A new list of integers with the block shifted, or a copy of the 
        input list if no such block is found.
    """
    n = len(input_grid)
    
    # 1. & 2. & 3. & 4. Find the first non-zero block details
    # Use a helper function to find the start, end, and value of the block
    start_index, end_index, block_value = find_first_block(input_grid)

    # If no block is found, return a copy of the original list
    if start_index is None:
        return list(input_grid) # Return a copy

    # 5. Create a new list initialized with zeros
    output_grid = [0] * n

    # 6. Calculate the new starting position for the block (shifted left by 1)
    new_start_index = start_index - 1
    
    # Check if the shift is valid (start_index should be > 0 based on examples)
    # If start_index was 0, new_start_index would be -1. The examples provided
    # all have blocks starting at index 1 or later.
    if new_start_index < 0:
        # This case is not represented in the training data.
        # Based on the task description "shift left", we might assume data loss
        # at the beginning or handle it differently if more examples were given.
        # For now, proceed assuming valid shift based on observed examples.
        # A robust implementation might raise an error or have specific logic here.
        pass # Assuming valid shift as per examples

    # Copy the block elements to their new positions in the output grid
    block_length = end_index - start_index
    for i in range(block_length):
        dest_index = new_start_index + i
        # Ensure the destination index is within the bounds of the output grid
        if 0 <= dest_index < n:
            output_grid[dest_index] = block_value # Place the block's value

    # 7. Return the newly created list with the shifted block
    return output_grid
```
