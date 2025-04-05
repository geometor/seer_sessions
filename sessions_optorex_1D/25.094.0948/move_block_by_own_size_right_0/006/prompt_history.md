
## train_1

**input:**
```
0 0 0 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 6 6 6 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 0 0
```


## train_4

**input:**
```
0 0 5 5 5 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 5 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 5
```


## train_6

**input:**
```
4 4 4 4 4 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 0 0
```


## train_7

**input:**
```
5 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 5 5 5 5 5 5
```

## Perception of Task Elements

The input and output are both sequences (or lists) of 12 integers.
Each input sequence contains a single contiguous block of identical non-zero integers, surrounded by zeros. The zeros act as padding or empty space.
The transformation involves moving this block of non-zero integers within the sequence.
The direction of movement is always to the right.
The distance the block moves appears to be directly related to the number of elements in the block (its length).

## Facts


```yaml
Input:
  type: list
  element_type: integer
  length: 12
  contains:
    - zeros: representing empty space
    - object:
        type: contiguous block
        properties:
          value: non-zero integer (consistent within the block)
          length: variable (number of elements in the block)
          start_index: position of the first element of the block
          end_index: position of the last element of the block
Output:
  type: list
  element_type: integer
  length: 12
  structure: derived from input by applying a transformation
Transformation:
  action: shift_right
  target: object (the contiguous block of non-zero integers)
  parameter: shift_distance
  relationship: shift_distance equals the length of the object
  effect:
    - The object moves to a new position.
    - The new start_index = old start_index + shift_distance.
    - The original positions occupied by the object become zeros.
Constraints:
  - The sequence length remains 12.
  - There is only one contiguous block of non-zero numbers in the input.
  - The shift operation occurs within the bounds of the sequence (no wrap-around or truncation observed in examples).
```


## Natural Language Program

1.  **Identify the Object:** Scan the input sequence to find the contiguous block of identical non-zero integers. Note its value, its starting index, and its length (number of elements).
2.  **Calculate Shift Distance:** Determine the shift distance, which is equal to the length of the identified block.
3.  **Create Output Sequence:** Initialize a new sequence of 12 zeros.
4.  **Place Shifted Object:** Calculate the new starting index for the block by adding the shift distance to the original starting index. Copy the identified block of non-zero integers into the new sequence starting at this new calculated index.
5.  **Return Output:** The resulting sequence is the output.
```python
"""
Identifies a contiguous block of identical non-zero integers in the input list.
Shifts this block to the right by a distance equal to its length.
The original positions of the block are replaced with zeros.
The output list has the same length as the input list.
"""

# No external libraries are required for this transformation.

def transform(input_list):
    """
    Transforms the input list by shifting a contiguous block of non-zero numbers.

    Args:
        input_list: A list of integers, expected to contain zeros and one
                    contiguous block of identical non-zero integers.

    Returns:
        A new list of integers representing the transformed state, or a copy
        of the input list if no non-zero block is found.
    """

    # Initialize variables to track the block properties
    start_index = -1
    block_value = 0
    block_length = 0
    list_len = len(input_list) # Cache list length for efficiency

    # --- Step 1: Identify the Object ---
    # Iterate through the input list to find the contiguous block of non-zero integers.
    # Record its starting index, value, and length.
    for i, val in enumerate(input_list):
        if val != 0:
            # Found a non-zero value
            if start_index == -1:
                # This is the first non-zero element found, marking the start of the block
                start_index = i
                block_value = val
                block_length = 1
            elif val == block_value:
                # This non-zero value matches the block's value, extend the block length
                block_length += 1
            else:
                 # Found a non-zero value different from the current block.
                 # Based on the problem constraints (single block), this signifies the end.
                 # Break here assumes the block definition is strict.
                break
        elif start_index != -1:
            # Found a zero after the block has started. This marks the end of the block.
            break
        # If val is 0 and start_index is -1, continue scanning for the block's start.

    # Handle the case where no non-zero block is found in the input list.
    if start_index == -1:
        # Return a copy of the original list as there is nothing to transform.
        return list(input_list)

    # --- Step 2: Calculate Shift Distance ---
    # The distance the block needs to shift is equal to its length.
    shift_distance = block_length

    # --- Step 3: Create Output Sequence ---
    # Initialize a new list of the same size as the input, filled with zeros.
    output_list = [0] * list_len

    # --- Step 4: Place Shifted Object ---
    # Calculate the starting index for the block in the output list.
    new_start_index = start_index + shift_distance

    # Copy the block's value into the output list at the calculated new position.
    # Iterate 'block_length' times to place each element of the block.
    for i in range(block_length):
        # Calculate the target index in the output list for the current element.
        write_index = new_start_index + i

        # Check if the target index is within the bounds of the output list.
        if write_index < list_len:
            # Place the block's value at the valid target index.
            output_list[write_index] = block_value
        # If write_index is out of bounds (>= list_len), the element is shifted
        # off the end of the list and is effectively dropped, which matches
        # the behavior implicitly shown in the examples (no wrap-around).

    # --- Step 5: Return Output ---
    # Return the newly constructed list containing the shifted block.
    return output_list
```
```python
"""
Transforms an input sequence (potentially a NumPy array) containing a single 
contiguous block of identical non-zero integers surrounded by zeros. The 
transformation shifts this block to the right by a distance equal to its length. 
Positions originally occupied by the block become zeros, and elements shifted 
beyond the sequence boundary are discarded.
"""

import numpy as np

def find_block(input_seq):
    """
    Finds the contiguous block of identical non-zero integers in the sequence.

    Args:
        input_seq: A NumPy array of integers.

    Returns:
        A tuple (start_index, block_length, block_value) if a block is found,
        otherwise None. Returns (-1, 0, 0) if no non-zero block found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(input_seq != 0)[0]

    # If no non-zero elements, no block exists
    if len(non_zero_indices) == 0:
        return -1, 0, 0

    # Identify potential start, end, length, and value
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    block_length = len(non_zero_indices)
    block_value = input_seq[start_index]

    # Verify the block is contiguous (indices are sequential)
    # and all values within the identified range are identical to the first non-zero value.
    # Check 1: Indices must form a continuous range (e.g., [2, 3, 4], not [2, 4])
    is_contiguous = (end_index - start_index + 1) == block_length
    # Check 2: All elements within this range [start_index:end_index+1] must equal block_value
    # This also implicitly checks if the original non_zero_indices were indeed identical.
    is_uniform_in_range = np.all(input_seq[start_index : end_index + 1] == block_value)

    if is_contiguous and is_uniform_in_range:
        return start_index, block_length, block_value
    else:
        # This case should not happen based on problem description, but handles unexpected input
        # For robustness, perhaps return the first found block segment or raise error.
        # Following the initial assumption of a single block:
        print(f"Warning: Input {input_seq} does not contain a single contiguous block of identical non-zero numbers.")
        # Return the first detected non-zero element as a block of length 1 for fallback
        # Or return failure indicator:
        return -1, 0, 0 # Indicate failure / no valid block


def transform(input_grid):
    """
    Applies the block shifting transformation.

    Args:
        input_grid: A 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array
    input_seq = np.array(input_grid)
    seq_len = len(input_seq)

    # --- Step 1 & 2: Identify Block and Extract Properties ---
    start_index, block_length, block_value = find_block(input_seq)

    # --- Step 3: Handle No Block Found Case ---
    # If no valid block is found (or input is all zeros), return an array of zeros.
    if start_index == -1:
        return np.zeros_like(input_seq)

    # --- Step 1 (Initialization): Create Output Sequence ---
    # Initialize the output grid with zeros, same size as input
    output_grid = np.zeros_like(input_seq)

    # --- Step 4: Calculate New Position ---
    new_start_index = start_index + block_length

    # --- Step 5: Place Shifted Block ---
    # Iterate 'block_length' times to place each element of the block
    for i in range(block_length):
        # Calculate the target index in the output grid for the current element.
        target_index = new_start_index + i

        # Check if the target index is within the bounds of the output grid.
        if 0 <= target_index < seq_len:
            # Place the block's value at the valid target index.
            output_grid[target_index] = block_value
        # Else: Element is shifted off the end and implicitly discarded (output_grid remains 0)

    # --- Step 6: Return Output ---
    return output_grid
```
```python
"""
Transforms an input 1D sequence (list or NumPy array) containing a single 
contiguous block of identical non-zero integers surrounded by zeros. 
The transformation shifts this block to the right by a distance equal to its length. 
Positions originally occupied by the block become zeros in the output. 
Elements shifted beyond the sequence boundary are discarded.
The output sequence has the same length as the input.
"""

import numpy as np

def find_block_properties(input_seq):
    """
    Identifies the contiguous block of identical non-zero integers.

    Args:
        input_seq: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, block_length, block_value) if a valid block 
        is found, otherwise returns (-1, 0, 0).
        - start_index: The starting index of the block.
        - block_length: The number of elements in the block.
        - block_value: The integer value of the elements in the block.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(input_seq != 0)[0]

    # If no non-zero elements, return failure indicator
    if len(non_zero_indices) == 0:
        return -1, 0, 0

    # Determine potential block boundaries and value from non-zero indices
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    block_value = input_seq[start_index]

    # Calculate the span covered by the potential block
    span_length = end_index - start_index + 1

    # Check 1: Contiguity
    # The number of non-zero elements found must equal the span length.
    # This ensures there are no zeros within the identified block range.
    is_contiguous = (len(non_zero_indices) == span_length)

    if not is_contiguous:
        # print(f"Debug: Non-contiguous non-zero elements found in {input_seq}")
        return -1, 0, 0 # Invalid block

    # Check 2: Uniformity
    # All elements within the identified span [start_index, end_index] must have the same value.
    # Slicing includes the end_index
    is_uniform = np.all(input_seq[start_index : end_index + 1] == block_value)

    if not is_uniform:
        # print(f"Debug: Block is not uniform in {input_seq}")
        return -1, 0, 0 # Invalid block
        
    # If both checks pass, it's a valid block. The length is the span length.
    block_length = span_length
    return start_index, block_length, block_value


def transform(input_grid):
    """
    Applies the block shifting transformation to the input grid.

    Args:
        input_grid: A list or 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array for efficient operations
    input_seq = np.array(input_grid)
    seq_len = len(input_seq)

    # initialize output_grid with zeros, same size as input
    output_grid = np.zeros_like(input_seq)

    # Find the properties of the non-zero block in the input sequence
    start_index, block_length, block_value = find_block_properties(input_seq)

    # If no valid block was found (e.g., all zeros or invalid format)
    if start_index == -1:
        return output_grid # Return the grid of zeros

    # Calculate the new starting position for the block
    # Shift distance is equal to the block length
    new_start_index = start_index + block_length

    # Place the shifted block into the output grid
    # Iterate 'block_length' times to place each element
    for i in range(block_length):
        # Calculate the index in the output grid for the current element
        target_index = new_start_index + i

        # Check if the target index is within the bounds of the grid
        if 0 <= target_index < seq_len:
            # Place the block's value at the target index
            output_grid[target_index] = block_value
        # Else: The element is shifted off the end of the grid and is discarded
        # (the output_grid position remains 0).

    return output_grid
```
