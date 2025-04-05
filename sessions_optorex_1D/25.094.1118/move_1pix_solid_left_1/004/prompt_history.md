
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
```python
"""
Transforms an input 1D NumPy array of integers by finding the first 
contiguous block of identical non-zero digits and shifting this block 
one position to the left. The array maintains its original length, and 
positions outside the shifted block are filled with zeros in the output.
"""

import numpy as np

def find_first_block_np(data):
    """
    Finds the start index, end index (exclusive), and value of the first 
    contiguous block of identical non-zero numbers in a NumPy array.

    Args:
        data: A 1D NumPy array of numbers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (None, None, None).
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(data)[0]

    # If no non-zero element found, no block exists
    if len(non_zero_indices) == 0:
        return None, None, None

    # The start index is the first non-zero index
    start_index = non_zero_indices[0]
    block_value = data[start_index]
    
    # Find the end of the block (index after the last element)
    end_index = start_index + 1
    n = len(data)
    while end_index < n and data[end_index] == block_value:
        end_index += 1
        
    # Verify that the block found corresponds to the *first* sequence 
    # of non-zeros. This check is important if there could be multiple 
    # blocks separated by zeros. np.nonzero finds all non-zeros, but we only
    # care about the first contiguous block. The while loop starting from 
    # non_zero_indices[0] ensures this.

    return start_index, end_index, block_value

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the first contiguous block of identical non-zero digits 
    one position to the left within the NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the block shifted, or a copy of the 
        input array if no such block is found or the block is already
        at the beginning.
    """
    # 1. Find the first non-zero block details
    start_index, end_index, block_value = find_first_block_np(input_grid)

    # If no block is found, return a copy of the original grid
    if start_index is None:
        return np.copy(input_grid) 

    # If the block starts at index 0, it cannot be shifted left.
    # Based on examples, this doesn't happen, but handle defensively.
    # The examples show blocks starting at index 1 or later being shifted.
    # If a block starts at 0, the examples suggest no change, but the prompt
    # implies a left shift. Let's assume based on examples that if start_index is 0, 
    # we return the original grid or handle as required if new examples clarify.
    # The test cases provided all shift blocks starting at index >= 1.
    # If start_index is 0, new_start_index would be -1.
    if start_index == 0:
         # Re-evaluate if examples with start_index=0 appear.
         # For now, aligning with the pattern that only blocks NOT at the start move.
         # Example output for input [2, 2, 0] -> [2, 2, 0]? or error? or [2, 0, 0]?
         # Let's assume no change if already at the start, consistent with outputs.
         # Example 5 output implies a shift even if starting at index 1 -> index 0.
         # Example 1 output implies a shift starting at index 1 -> index 0.
         # Ok, the shift should happen even if it means starting at index 0.
         pass # Proceed with the shift calculation.

    # 2. Create a new array initialized with zeros
    output_grid = np.zeros_like(input_grid)

    # 3. Calculate the new starting position and block length
    new_start_index = start_index - 1
    block_length = end_index - start_index

    # Ensure the new start index isn't negative before slicing
    if new_start_index < 0:
        # This case means the block started at index 0.
        # The problem description/examples don't explicitly cover shifting *off* the grid.
        # Based on example 1 & 5, shifting *to* index 0 is expected.
        # If we *must* shift left from index 0, we'd lose the first element.
        # However, let's stick to the observed patterns where the shift target index >= 0.
        # If start_index=0, new_start_index = -1. Let's adjust.
        # The slice `output_grid[-1:block_length-1]` is not intuitive.
        # Let's refine the copy logic for the edge case start_index=0
        
        # If the original block starts at index 0
        # Example: [2, 2, 0, 0] -> shift left -> [2, 0, 0, 0]? lose one '2'?
        # The examples show blocks starting >= 1. Let's assume valid shifts.
        # If an example like [2, 2, ...] -> [2, ...] arises, we'll adapt.
        # The current logic correctly handles shifts resulting in index 0 (e.g., from index 1).
         pass # The slicing below handles the valid cases shown.


    # 4. Copy the block elements to their new positions in the output grid
    # Calculate the actual start and end for slicing in the output array
    output_slice_start = max(0, new_start_index) 
    output_slice_end = new_start_index + block_length
    
    # Calculate the corresponding slice from the original block value
    # If new_start_index is < 0, we start copying from the second element of the block
    block_copy_len = output_slice_end - output_slice_start

    # Place the block value into the output grid slice
    if block_copy_len > 0 and output_slice_start < len(output_grid):
       output_grid[output_slice_start:min(output_slice_end, len(output_grid))] = block_value


    # 5. Return the newly created grid
    return output_grid
```
