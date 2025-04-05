
## train_1

**input:**
```
0 0 1 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 0 0 0 0 0 0
```


## train_2

**input:**
```
7 4 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 7 4 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 4 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 5 0 0 0 0 0
```


## train_5

**input:**
```
0 1 5 9 9 3 4 8 9 0 0 0
```


**output:**
```
0 0 0 0 1 5 9 9 3 4 8 9
```


## train_6

**input:**
```
0 7 7 3 4 4 1 2 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 3 4 4 1 2 0
```


## train_7

**input:**
```
0 0 0 0 0 0 8 6 6 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 6 6
```

*   **Perception of Task Elements:**
    *   The input and output are both sequences (lists) of integers.
    *   All provided examples have sequences of length 12.
    *   The core transformation involves relocating a contiguous block of non-zero numbers within the sequence.
    *   The relative order and values of the non-zero numbers are preserved.
    *   The block of non-zero numbers is consistently shifted 3 positions to the right.
    *   The output sequence is padded with zeros in the positions not occupied by the shifted block.
    *   The length of the sequence remains constant (12).

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: input_list
        properties:
          - type: list
          - contains: integers
          - length: fixed (e.g., 12)
      - object: output_list
        properties:
          - type: list
          - contains: integers
          - length: same as input_list
          - derived_from: input_list
      - object: non_zero_block
        properties:
          - type: sublist
          - derived_from: input_list
          - content: sequence of elements starting from the first non-zero element to the last non-zero element in the input_list
          - relative_order: preserved from input_list
          - values: preserved from input_list
      - object: zero_padding
        properties:
          - value: 0
          - role: fills positions in output_list not occupied by the non_zero_block
    actions:
      - name: identify_block
        input: input_list
        output: non_zero_block, start_index, end_index
        description: Find the first and last non-zero elements in the input_list to define the block and its original indices. If no non-zero elements exist, the block is empty.
      - name: calculate_new_position
        input: start_index, end_index, shift_amount (constant: 3)
        output: new_start_index, new_end_index
        description: Add the shift_amount to the original start and end indices.
      - name: construct_output
        input: non_zero_block, new_start_index, new_end_index, list_length
        output: output_list
        description: Create a new list of the specified length, filled initially with zeros. Place the non_zero_block at the calculated new_start_index. Ensure indices stay within bounds.
    relationships:
      - type: transformation
        from: input_list
        to: output_list
        rule: shift non_zero_block right by 3 positions
      - type: positional_shift
        object: non_zero_block
        direction: right
        amount: 3 positions
    constants:
      - shift_amount: 3
      - padding_value: 0
    ```


*   **Natural Language Program:**
    1.  Receive the input list of integers.
    2.  Initialize an output list of the same length as the input list, filled entirely with zeros.
    3.  Identify the index of the first non-zero element in the input list (`first_nz_index`). If no non-zero elements exist, the output list remains all zeros; proceed to step 7.
    4.  Identify the index of the last non-zero element in the input list (`last_nz_index`).
    5.  Extract the sublist (the "block") from the input list starting at `first_nz_index` and ending at `last_nz_index` (inclusive).
    6.  Place this extracted block into the output list, starting at index `first_nz_index + 3`. Ensure the elements are placed correctly relative to this new starting position.
    7.  Return the constructed output list.
```python
import math
import numpy as np # Using numpy for easier array manipulation if needed, though list slicing is sufficient here

"""
Identifies the contiguous block of non-zero numbers in the input list, 
shifts this block 3 positions to the right, and places it into an 
output list of the same size, padded with zeros elsewhere.
"""

def _find_non_zero_indices(data_list):
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.
    Returns (None, None) if no non-zero numbers are found.
    """
    first_nz_index = None
    last_nz_index = None
    for i, val in enumerate(data_list):
        if val != 0:
            if first_nz_index is None:
                first_nz_index = i
            last_nz_index = i
    return first_nz_index, last_nz_index

def transform(input_list):
    """
    Transforms the input list by shifting the block of non-zero numbers 3 positions to the right.

    Args:
        input_list: A list of integers.

    Returns:
        A new list of integers with the non-zero block shifted.
    """
    # Determine the length of the list
    list_length = len(input_list)

    # Initialize output_list with zeros, same length as input
    output_list = [0] * list_length

    # 1. Find the start and end indices of the non-zero block
    first_nz_index, last_nz_index = _find_non_zero_indices(input_list)

    # 2. Check if a non-zero block was found
    if first_nz_index is not None:
        # 3. Extract the non-zero block
        non_zero_block = input_list[first_nz_index : last_nz_index + 1]

        # 4. Calculate the new starting position for the block
        new_start_index = first_nz_index + 3
        
        # 5. Place the block into the output list at the new position
        # Ensure we don't write past the end of the output list
        block_len = len(non_zero_block)
        end_placement_index = new_start_index + block_len
        
        # Calculate how much of the block fits
        elements_to_place = block_len
        if end_placement_index > list_length:
             elements_to_place = list_length - new_start_index
             
        if elements_to_place > 0 and new_start_index < list_length:
             output_list[new_start_index : new_start_index + elements_to_place] = non_zero_block[:elements_to_place]


    # 6. Return the constructed output list
    return output_list

```
```python
import math
# No external libraries like numpy needed based on the core logic identified.

"""
Identifies a contiguous block of non-zero numbers within an input list, 
shifts this block 3 positions to the right, and places it into an 
output list of the same size, padded with zeros elsewhere. Handles cases 
where the shifted block might extend beyond the list boundaries by truncating 
the block. If the input list contains only zeros, the output list will also 
contain only zeros.
"""

def _find_non_zero_indices(data_list):
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.
    
    Args:
        data_list: A list of numbers.

    Returns:
        A tuple (start_index, end_index). Returns (None, None) if no 
        non-zero numbers are found.
    """
    first_nz_index = None
    last_nz_index = None
    # Iterate through the list with index and value
    for i, val in enumerate(data_list):
        # Check if the value is not zero
        if val != 0:
            # If this is the first non-zero found, record its index
            if first_nz_index is None:
                first_nz_index = i
            # Always update the last non-zero index found
            last_nz_index = i
            
    # Return the found indices (or None if none were found)
    return first_nz_index, last_nz_index

def transform(input_list):
    """
    Transforms the input list by shifting the block of non-zero numbers 
    3 positions to the right.

    Args:
        input_list: A list of integers.

    Returns:
        A new list of integers with the non-zero block shifted, or a list 
        of zeros if no non-zero block exists in the input.
    """
    # Ensure input is a standard list, in case it's passed as another iterable type
    input_list = list(input_list) 
    
    # Determine the length of the list
    list_length = len(input_list)

    # Initialize output_list with zeros, same length as input
    output_list = [0] * list_length

    # Find the start and end indices of the non-zero block using the helper function
    first_nz_index, last_nz_index = _find_non_zero_indices(input_list)

    # Check if a non-zero block was actually found
    if first_nz_index is not None:
        # Extract the non-zero block using list slicing
        # Note: slicing is exclusive of the end index, so add 1 to last_nz_index
        non_zero_block = input_list[first_nz_index : last_nz_index + 1]

        # Calculate the new starting position for the block (shift right by 3)
        new_start_index = first_nz_index + 3
        
        # Determine the length of the extracted block
        block_len = len(non_zero_block)
        
        # Calculate the index where the placement would end
        end_placement_index = new_start_index + block_len

        # Determine how many elements from the block can actually be placed
        # without going out of bounds of the output list.
        elements_to_place = block_len
        if end_placement_index > list_length:
            # If the block overflows, calculate how many elements fit
            elements_to_place = list_length - new_start_index
            # If the adjusted count is negative (meaning the start index is already out of bounds), set to 0
            if elements_to_place < 0:
                elements_to_place = 0

        # Place the block (or the portion that fits) into the output list
        # Ensure the new start index is within the list bounds and there are elements to place
        if new_start_index < list_length and elements_to_place > 0:
            # Slice the output list and assign the appropriate slice of the non_zero_block
             output_list[new_start_index : new_start_index + elements_to_place] = non_zero_block[:elements_to_place]

    # Return the constructed output list (either modified or still all zeros)
    return output_list
```
```python
import numpy as np

"""
Transforms an input grid (list of lists or 2D NumPy array) by identifying a 
contiguous vertical block of rows containing at least one non-zero element. 
This block is then shifted downwards by 3 rows within a new grid of the same 
dimensions. Rows outside the shifted block are filled with zeros. If the shifted 
block extends beyond the grid boundaries, it is truncated. If no non-zero 
elements are found in any row, the output grid remains filled with zeros.
"""

def _find_non_zero_row_indices(grid):
    """
    Finds the start and end row indices of the first contiguous block of 
    rows containing at least one non-zero element.

    Args:
        grid: A NumPy array representing the input grid.

    Returns:
        A tuple (start_index, end_index). Returns (None, None) if no 
        non-zero rows are found.
    """
    first_nz_row_index = None
    last_nz_row_index = None
    # Iterate through each row index
    for i in range(grid.shape[0]):
        row = grid[i, :]
        # Check if any element in the row is non-zero
        if np.any(row != 0):
            # If this is the first non-zero row found, record its index
            if first_nz_row_index is None:
                first_nz_row_index = i
            # Always update the last non-zero row index found
            last_nz_row_index = i
            
    # Return the found indices (or None if none were found)
    return first_nz_row_index, last_nz_row_index

def transform(input_grid):
    """
    Applies the row-block shifting transformation to the input grid.

    Args:
        input_grid: A list of lists or a 2D NumPy array representing the grid.

    Returns:
        A 2D NumPy array representing the transformed grid.
    """
    # Convert input to NumPy array for consistent handling and array operations
    input_grid_np = np.array(input_grid)
    
    # Get grid dimensions (rows N, columns M)
    if input_grid_np.ndim == 1:
        # Handle case where input might be flattened but represents rows of size 1
        num_rows = input_grid_np.shape[0]
        num_cols = 1
        # Reshape into N x 1 explicitly for consistent indexing
        input_grid_np = input_grid_np.reshape((num_rows, num_cols))
    elif input_grid_np.ndim == 2:
        num_rows, num_cols = input_grid_np.shape
    else:
        # Handle unexpected dimensions if necessary, though examples suggest 2D
        raise ValueError("Input grid must be interpretable as 2D.")

    # Initialize output_grid with zeros, same dimensions as input
    output_grid = np.zeros_like(input_grid_np)

    # Find the start and end indices of the non-zero row block
    first_nz_row_index, last_nz_row_index = _find_non_zero_row_indices(input_grid_np)

    # Check if a non-zero row block was actually found
    if first_nz_row_index is not None:
        # Extract the block of rows using NumPy slicing
        # Note: slicing is exclusive of the end index, so add 1
        non_zero_row_block = input_grid_np[first_nz_row_index : last_nz_row_index + 1, :]

        # Calculate the new starting row index for the block (shift down by 3)
        new_start_row_index = first_nz_row_index + 3
        
        # Determine the number of rows in the extracted block
        block_height = non_zero_row_block.shape[0]
        
        # Calculate the index where the placement would end
        end_placement_index = new_start_row_index + block_height

        # Determine how many rows from the block can actually be placed
        # without going out of bounds of the output grid.
        rows_to_place = block_height
        if end_placement_index > num_rows:
            # If the block overflows, calculate how many rows fit
            rows_to_place = num_rows - new_start_row_index
            # If the adjusted count is negative (start index out of bounds), set to 0
            if rows_to_place < 0:
                rows_to_place = 0
        
        # Slice the block if it needs truncation
        truncated_block = non_zero_row_block[:rows_to_place, :]

        # Place the block (or the truncated portion) into the output grid
        # Ensure the new start index is within the grid bounds and there are rows to place
        if new_start_row_index < num_rows and rows_to_place > 0:
            output_grid[new_start_row_index : new_start_row_index + rows_to_place, :] = truncated_block

    # Return the constructed output grid
    return output_grid
```
