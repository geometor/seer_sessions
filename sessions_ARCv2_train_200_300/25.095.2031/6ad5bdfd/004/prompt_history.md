
## train_1

**input:**
```
2 0 0 3 3 0 0 4 4 0 0
2 0 0 0 0 5 0 0 0 0 0
2 0 0 0 0 5 0 0 6 6 0
2 0 0 0 0 0 0 8 0 0 0
2 0 7 7 0 0 0 8 0 0 0
```


**output:**
```
2 3 3 4 4 0 0 0 0 0 0
2 5 0 0 0 0 0 0 0 0 0
2 5 6 6 0 0 0 0 0 0 0
2 0 0 8 0 0 0 0 0 0 0
2 7 7 8 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 8 8
3 0 0 4 0 0
3 0 0 4 0 0
0 0 0 0 0 6
1 1 0 0 0 6
0 0 0 0 0 0
0 0 5 5 0 0
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 0 0 4 8 8
3 0 0 4 0 6
1 1 5 5 0 6
2 2 2 2 2 2
```


## train_3

**input:**
```
0 4 4 0 0 0 0 0 0 2
0 0 0 5 5 0 0 6 0 2
0 0 0 0 0 0 0 6 0 2
0 9 0 0 8 8 0 0 0 2
0 9 0 0 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 4 4 2
0 0 0 0 0 0 5 5 6 2
0 0 0 0 0 0 0 0 6 2
0 0 0 0 0 0 9 8 8 2
0 0 0 0 0 0 9 0 0 2
```

Okay, let's analyze the `train_1` example pair.

**Perception of Elements:**

*   The input and output are grids (represented as lines of space-separated integers), likely representing rows of a 2D structure or individual 1D arrays. For `train_1`, each line seems to be processed independently.
*   Each line contains integer values, primarily single digits, including zero.
*   The core operation appears to involve rearranging the non-zero elements within each line while keeping the very first element fixed.
*   Zeroes seem to act as empty space or placeholders.

**YAML Facts:**


```yaml
task_name: shift_non_zeros_left_preserving_first
data_type: grid_of_integers
dimensionality: primarily_1D_processing # Each row/list processed independently
objects:
  - name: grid_row
    properties:
      - elements: list_of_integers
      - length: integer
  - name: element
    properties:
      - value: integer
      - position: index (integer)
      - is_zero: boolean
      - is_first: boolean
relationships:
  - type: spatial
    between: elements
    details: elements are ordered sequentially within a row
actions:
  - name: identify_fixed_element
    inputs: grid_row
    outputs: element (the first one)
  - name: filter_non_zeros
    inputs: grid_row (excluding the first element)
    outputs: list_of_non_zero_elements (maintaining relative order)
  - name: construct_output_row
    inputs:
      - fixed_element
      - filtered_non_zero_elements
      - original_row_length
    outputs: new_grid_row
    process: place fixed_element at start, append filtered_non_zero_elements, pad with zeros to match original length
constraints:
  - The first element of each input row remains in the first position of the output row.
  - The relative order of the non-zero elements (excluding the first) is preserved.
  - The length of the output row is the same as the length of the input row.
```


**Natural Language Program:**

For each input row:
1.  Store the value of the first element.
2.  Create a list containing all non-zero elements from the second position to the end of the input row, maintaining their original relative order.
3.  Construct the output row by starting with the stored first element.
4.  Append the list of non-zero elements (from step 2) immediately after the first element.
5.  Append zeros to the end of the output row until its length matches the length of the original input row.
```python
import collections

"""
For each input row (list of integers):
1. Store the value of the first element.
2. Create a new list containing all non-zero elements from the second position 
   to the end of the input row, maintaining their original relative order.
3. Construct the output row by starting with the stored first element.
4. Append the list of non-zero elements (from step 2) immediately after the 
   first element.
5. Append zeros to the end of the output row until its length matches the length
   of the original input row.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms each row of the input grid by moving all non-zero elements 
    (except the first) to the left, immediately following the first element,
    and padding the rest with zeros.
    """
    output_grid = [] # Initialize the output grid

    # Process each row individually
    for input_row in input_grid:
        # Handle empty rows if necessary, though examples don't show them
        if not input_row:
            output_grid.append([])
            continue

        # 1. Store the value of the first element.
        first_element = input_row[0]
        original_length = len(input_row)

        # 2. Create a list containing all non-zero elements from the second 
        #    position onwards, maintaining relative order.
        non_zeros_after_first = [
            element for element in input_row[1:] if element != 0
        ]

        # 3. Construct the output row starting with the stored first element.
        new_row = [first_element]

        # 4. Append the list of non-zero elements.
        new_row.extend(non_zeros_after_first)

        # 5. Append zeros until the length matches the original input row length.
        padding_zeros_count = original_length - len(new_row)
        new_row.extend([0] * padding_zeros_count)

        # Add the transformed row to the output grid
        output_grid.append(new_row)

    return output_grid
```
```python
import numpy as np
from typing import List

"""
Transforms an input grid of integers based on the properties of its first and last columns.

1. Analyzes the input grid's first and last columns.
2. If the first column consists of a single, non-zero value repeated for all rows, 
   apply the 'Left Shift Rule'.
3. Else if the last column consists of a single, non-zero value repeated for all rows,
   apply the 'Right Shift Rule'.
4. Otherwise (neither condition is met), apply the 'Gravity Rule'.

Rule Descriptions:
- Left Shift Rule: For each row, keep the first element fixed. Move all other 
  non-zero elements immediately to the right of the first element, preserving 
  their relative order. Fill the remaining positions in the row with zeros.
- Right Shift Rule: For each row, keep the last element fixed. Move all other 
  non-zero elements immediately to the left of the last element, preserving 
  their relative order. Fill the remaining positions at the beginning of the 
  row with zeros.
- Gravity Rule: For each column, move all non-zero elements downwards to occupy 
  the lowest possible rows within that column, preserving their relative vertical order. 
  Fill the positions above them in the column with zeros.
"""

def _is_column_constant_non_zero(grid: List[List[int]], col_index: int) -> bool:
    """Checks if a specific column is constant and the constant value is non-zero."""
    if not grid or not grid[0]: # Handle empty grid
        return False
    num_rows = len(grid)
    if num_rows == 0:
        return False
        
    # Adjust col_index for negative indexing (like -1 for last column)
    num_cols = len(grid[0])
    if col_index < 0:
        col_index = num_cols + col_index
        
    if not (0 <= col_index < num_cols): # Invalid column index
        return False

    first_val = grid[0][col_index]
    if first_val == 0:
        return False # Constant value must be non-zero

    for i in range(1, num_rows):
        if len(grid[i]) <= col_index or grid[i][col_index] != first_val:
            return False # Not constant or row is too short

    return True

def _apply_left_shift(grid: List[List[int]]) -> List[List[int]]:
    """Applies the Left Shift Rule."""
    output_grid = []
    for input_row in grid:
        if not input_row:
            output_grid.append([])
            continue
        
        original_length = len(input_row)
        first_element = input_row[0]
        
        # Collect non-zero elements from the rest of the row
        non_zeros_after_first = [
            element for element in input_row[1:] if element != 0
        ]
        
        # Construct the new row
        new_row = [first_element]
        new_row.extend(non_zeros_after_first)
        
        # Pad with zeros
        padding_zeros_count = original_length - len(new_row)
        new_row.extend([0] * padding_zeros_count)
        
        output_grid.append(new_row)
    return output_grid

def _apply_right_shift(grid: List[List[int]]) -> List[List[int]]:
    """Applies the Right Shift Rule."""
    output_grid = []
    for input_row in grid:
        if not input_row:
            output_grid.append([])
            continue

        original_length = len(input_row)
        if original_length == 0:
             output_grid.append([])
             continue
             
        last_element = input_row[-1]
        
        # Collect non-zero elements before the last element
        non_zeros_before_last = [
            element for element in input_row[:-1] if element != 0
        ]
        
        # Calculate padding
        num_non_zeros = len(non_zeros_before_last)
        padding_zeros_count = original_length - 1 - num_non_zeros
        
        # Construct the new row
        new_row = [0] * padding_zeros_count
        new_row.extend(non_zeros_before_last)
        new_row.append(last_element)
        
        output_grid.append(new_row)
    return output_grid

def _apply_gravity(grid: List[List[int]]) -> List[List[int]]:
    """Applies the Gravity Rule using NumPy for easier column manipulation."""
    if not grid or not grid[0]:
        return [] # Handle empty grid case

    input_np = np.array(grid, dtype=int)
    num_rows, num_cols = input_np.shape
    output_np = np.zeros_like(input_np) # Initialize output with zeros

    # Process each column
    for j in range(num_cols):
        # Extract non-zero elements from the current column
        column_data = input_np[:, j]
        non_zeros = column_data[column_data != 0]
        
        # Place non-zeros at the bottom of the output column
        num_non_zeros = len(non_zeros)
        if num_non_zeros > 0:
            output_np[num_rows - num_non_zeros:, j] = non_zeros
            
    # Convert back to list of lists for the final output format
    return output_np.tolist()

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on analyzing its first and last columns.
    Selects and applies one of three rules: Left Shift, Right Shift, or Gravity.
    """
    
    # Handle edge case of completely empty input
    if not input_grid:
        return []
        
    # --- Condition Check ---
    is_first_col_const_nz = _is_column_constant_non_zero(input_grid, 0)
    is_last_col_const_nz = _is_column_constant_non_zero(input_grid, -1)
    
    # --- Rule Selection and Execution ---
    if is_first_col_const_nz:
        # Apply Left Shift Rule (Type 1)
        output_grid = _apply_left_shift(input_grid)
    elif is_last_col_const_nz:
        # Apply Right Shift Rule (Type 3)
        output_grid = _apply_right_shift(input_grid)
    else:
        # Apply Gravity Rule (Type 2)
        output_grid = _apply_gravity(input_grid)
        
    return output_grid
```
