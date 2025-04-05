
## train_1

**input:**
```
0 0 3 7 5 6 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 7 5 6 5 0
```


## train_2

**input:**
```
0 4 8 1 8 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 8 1 8 9 0 0
```


## train_3

**input:**
```
0 5 1 7 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 1 7 8 0 0 0
```


## train_4

**input:**
```
4 3 4 3 6 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 3 4 3 6 0 0 0
```


## train_5

**input:**
```
0 8 2 4 2 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 8 2 4 2 8 0 0
```


## train_6

**input:**
```
3 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 9 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 4
```

*   **Perception:** The task operates on fixed-length sequences of 12 integers. Each input sequence contains a single contiguous block of non-zero integers, surrounded by zeros. The transformation involves relocating this non-zero block within the sequence while preserving the block itself and the surrounding zeros. The core action is a rightward shift of the non-zero block by a fixed amount.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input_type: list_of_integers
    output_type: list_of_integers
    sequence_length: 12
    elements:
      - type: zero
        role: padding/background
      - type: non_zero_block
        description: A contiguous subsequence of non-zero integers.
        properties:
          - content: the sequence of non-zero integers
          - start_index_input: the index where the block begins in the input
          - length: the number of elements in the block
    action:
      type: shift
      direction: right
      amount: 4
      target: non_zero_block
    relationship: The output sequence is constructed by taking the input sequence, identifying the non_zero_block, and placing it in a new sequence (initially all zeros) starting at `start_index_input + 4`. The relative order of elements within the non_zero_block is preserved.
    constraints: Assumes only one contiguous non-zero block exists in the input. Assumes the shifted block fits within the sequence length of 12.
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of length 12 with all zeros.
    2.  Scan the input sequence to find the first non-zero integer. Record its index as `start_index`.
    3.  Continue scanning from `start_index` to find the end of the contiguous block of non-zero integers. Record this block of numbers as the `payload`.
    4.  Calculate the `target_start_index` by adding 4 to the `start_index`.
    5.  Place the `payload` into the output sequence, starting at the `target_start_index`.
    6.  Return the output sequence.
```python
"""
Transforms an input sequence of 12 integers by identifying a single contiguous block of non-zero integers and shifting this block 4 positions to the right, preserving the block's content and the surrounding zeros.

1. Initialize an output sequence of length 12 with all zeros.
2. Scan the input sequence to find the first non-zero integer. Record its index as `start_index`.
3. Continue scanning from `start_index` to find the end of the contiguous block of non-zero integers. Record this block of numbers as the `payload`.
4. Calculate the `target_start_index` by adding 4 to the `start_index`.
5. Place the `payload` into the output sequence, starting at the `target_start_index`.
6. Return the output sequence.
"""

import re # Using regex to easily find the non-zero block

def find_non_zero_block(input_list):
    """
    Finds the first contiguous block of non-zero integers in a list.

    Args:
        input_list: A list of integers.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block (or -1 if not found).
        - payload: A list containing the non-zero integers in the block (or empty list if not found).
    """
    start_index = -1
    payload = []
    in_block = False
    for i, num in enumerate(input_list):
        if num != 0 and not in_block:
            start_index = i
            in_block = True
            payload.append(num)
        elif num != 0 and in_block:
            payload.append(num)
        elif num == 0 and in_block:
            # Found the end of the block
            break
        # Handle case where block goes to the end of the list implicitly
    if not payload: # Handle case of all zeros or no block found
        return -1, []
    return start_index, payload


def transform(input_str):
    """
    Applies the described transformation rule to the input string.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Parse input string into a list of integers
    input_list = [int(x) for x in input_str.strip().split()]
    n = len(input_list) # Should be 12 based on examples

    # 1. Initialize an output sequence of length 12 with all zeros.
    output_grid = [0] * n

    # 2. & 3. Find the start index and the payload (non-zero block)
    start_index, payload = find_non_zero_block(input_list)

    # Check if a block was found
    if start_index != -1:
        # 4. Calculate the target_start_index by adding 4 to the start_index.
        target_start_index = start_index + 4

        # 5. Place the payload into the output sequence, starting at the target_start_index.
        # Ensure the placement doesn't go out of bounds (though examples suggest it fits)
        payload_len = len(payload)
        if target_start_index + payload_len <= n:
            for i in range(payload_len):
                output_grid[target_start_index + i] = payload[i]
        else:
            # Handle potential out-of-bounds placement if necessary,
            # though not observed in provided examples.
            # For now, place as much as fits, or raise an error, or wrap around?
            # Based on example 7, it seems it just shifts and fits within bounds.
            # Let's stick to direct placement assuming it fits.
             for i in range(payload_len):
                 if target_start_index + i < n:
                    output_grid[target_start_index + i] = payload[i]


    # 6. Return the output sequence.
    return output_grid
```
```python
"""
Transforms an input NumPy array of 12 integers by identifying a single
contiguous block of non-zero integers and shifting this block 4 positions
to the right, preserving the block's content and the surrounding zeros.

1.  Accept the input sequence as a NumPy array.
2.  Initialize an output NumPy array of the same size with all zeros.
3.  Find the start index and content (`payload`) of the first contiguous
    block of non-zero integers in the input array.
4.  If no non-zero block is found, return the initialized zero array.
5.  Calculate the `target_start_index` by adding 4 to the `start_index`.
6.  Calculate the `target_end_index` based on the target start and payload length.
7.  Copy the `payload` into the output array slice defined by the target
    start and end indices, ensuring it stays within bounds.
8.  Return the output array.
"""

import numpy as np

def find_non_zero_block_np(grid: np.ndarray) -> tuple[int, np.ndarray | None]:
    """
    Finds the first contiguous block of non-zero integers in a NumPy array.

    Args:
        grid: A 1D NumPy array of integers.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block (or -1 if not found).
        - payload: A NumPy array containing the non-zero integers in the block
                   (or None if not found).
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(grid != 0)[0]

    # Handle case with no non-zero elements
    if non_zero_indices.size == 0:
        return -1, None

    # The start index is the first non-zero index
    start_index = non_zero_indices[0]

    # Determine the end index of the first contiguous block
    if non_zero_indices.size == 1:
        # Only one non-zero element
        end_index = start_index
    else:
        # Check for gaps between non-zero indices
        diffs = np.diff(non_zero_indices)
        gaps = np.where(diffs > 1)[0]
        if gaps.size == 0:
            # No gaps, the block extends to the last non-zero element
            end_index = non_zero_indices[-1]
        else:
            # Gaps exist, the first block ends before the first gap
            # gaps[0] is the index *within diffs* where the first gap occurs.
            # The corresponding index in non_zero_indices is non_zero_indices[gaps[0]]
            end_index = non_zero_indices[gaps[0]]

    # Extract the payload (the actual non-zero numbers in the block)
    # Slicing is [start:end+1] to include the element at end_index
    payload = grid[start_index : end_index + 1]

    return start_index, payload


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # Get the size of the input grid
    n = input_grid.shape[0]

    # Initialize an output grid of the same size with all zeros.
    output_grid = np.zeros_like(input_grid)

    # Find the start index and the payload (non-zero block) using the helper function.
    start_index, payload = find_non_zero_block_np(input_grid)

    # Proceed only if a non-zero block was found
    if start_index != -1 and payload is not None:
        # Calculate the target start index for the shift (shift right by 4)
        target_start_index = start_index + 4

        # Calculate the target end index (exclusive) for slicing
        payload_len = payload.shape[0]
        target_end_index = target_start_index + payload_len

        # --- Place the payload into the output grid ---
        
        # Determine the actual slice range within the output grid's bounds [0, n)
        # The starting position of the slice in the output grid cannot be negative or >= n
        actual_start = max(0, target_start_index) 
        actual_start = min(actual_start, n) # Clamp start index to be at most n

        # The ending position of the slice in the output grid cannot exceed n
        actual_end = min(target_end_index, n)
        actual_end = max(actual_start, actual_end) # Ensure end >= start

        # Determine the part of the payload to copy based on the available space in the output slice
        # Calculate how many elements to skip from the beginning of the payload if target_start_index was < 0
        payload_start_offset = max(0, -target_start_index) 
        # Calculate the number of elements that actually fit in the target slice
        payload_copy_len = actual_end - actual_start

        # Check if there's anything to copy
        if payload_copy_len > 0 and payload_start_offset < payload_len:
             # Select the correct part of the payload
             payload_to_copy = payload[payload_start_offset : payload_start_offset + payload_copy_len]
             # Copy the relevant part of the payload to the target slice
             output_grid[actual_start:actual_end] = payload_to_copy

    # Return the transformed grid
    return output_grid
```
```python
"""
Transforms an input sequence of 12 integers by identifying the first
contiguous block of non-zero integers and shifting this block 4 positions
to the right within a new sequence initialized with zeros. If the shifted
block extends beyond the sequence boundaries, only the portion that fits
is placed.
"""

import numpy as np

def find_first_non_zero_block(grid: np.ndarray) -> tuple[int, np.ndarray | None]:
    """
    Finds the first contiguous block of non-zero integers in a NumPy array.

    Args:
        grid: A 1D NumPy array of integers.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block (or -1 if not found).
        - payload: A NumPy array containing the non-zero integers in the block
                   (or None if not found). Returns only the *first* block if
                   multiple disjoint blocks exist.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(grid != 0)[0]

    # Handle case with no non-zero elements
    if non_zero_indices.size == 0:
        return -1, None

    # The start index is the first non-zero index found
    start_index = non_zero_indices[0]

    # Determine the end index of the first contiguous block
    if non_zero_indices.size == 1:
        # Only one non-zero element, block length is 1
        end_index = start_index
    else:
        # Check for gaps between non-zero indices
        diffs = np.diff(non_zero_indices)
        # Find the index *within non_zero_indices* where the first gap occurs
        gaps = np.where(diffs > 1)[0]
        if gaps.size == 0:
            # No gaps, the block extends to the last non-zero element found
            end_index = non_zero_indices[-1]
        else:
            # Gaps exist, the first block ends at the index just before the first gap
            # gaps[0] is the index in `diffs` where the first difference > 1 occurs.
            # This corresponds to the index in `non_zero_indices` *before* the gap.
            end_index = non_zero_indices[gaps[0]]

    # Extract the payload (the actual non-zero numbers in the identified block)
    # Slicing is [start:end+1] to include the element at end_index
    payload = grid[start_index : end_index + 1]

    return start_index, payload


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array (expected length 12).

    Returns:
        A new 1D NumPy array with the first non-zero block shifted right by 4.
    """
    # Get the size of the input grid (should be 12)
    n = input_grid.shape[0]

    # 1. Initialize an output grid of the same size with all zeros.
    output_grid = np.zeros_like(input_grid)

    # 2. Find the start index and the payload (first non-zero block)
    start_index, payload = find_first_non_zero_block(input_grid)

    # 3. Proceed only if a non-zero block was found
    if start_index != -1 and payload is not None:
        # 4. Calculate the target start index for the shift (shift right by 4)
        target_start_index = start_index + 4
        payload_len = payload.shape[0]

        # 5. Calculate the target end index (exclusive) for slicing
        target_end_index = target_start_index + payload_len

        # 6. Determine the actual slice boundaries within the output grid [0, n)
        # Ensure the slice start is not less than 0 or greater than or equal to n
        actual_output_start = max(0, target_start_index)
        actual_output_start = min(actual_output_start, n) # Clamp start to be at most n

        # Ensure the slice end is not greater than n
        actual_output_end = min(n, target_end_index)
        actual_output_end = max(actual_output_start, actual_output_end) # Ensure end >= start

        # 7. Determine the portion of the payload to copy based on boundaries
        # How many elements to skip from the start of payload if target_start_index < 0
        payload_start_offset = max(0, -target_start_index)
        # How many elements actually fit in the calculated output slice
        payload_copy_len = actual_output_end - actual_output_start

        # 8. Copy the relevant part of the payload if there's space and content
        if payload_copy_len > 0 and payload_start_offset < payload_len:
            # Select the correct sub-slice of the payload
            payload_to_copy = payload[payload_start_offset : payload_start_offset + payload_copy_len]
            # Assign the payload slice to the calculated output slice
            output_grid[actual_output_start:actual_output_end] = payload_to_copy

    # 9. Return the transformed grid
    return output_grid
```
