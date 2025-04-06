```python
import numpy as np
from typing import List

"""
Transforms an input grid of integers based on the properties of its first and last columns.

1. Analyzes the input grid's first and last columns to determine the transformation type.
2. If the first column consists of a single, non-zero value repeated for all rows, 
   apply the 'Left Shift Rule'.
3. Else if the last column consists of a single, non-zero value repeated for all rows,
   apply the 'Right Shift Rule'.
4. Otherwise (neither condition is met), apply the 'Gravity Rule'.

Rule Descriptions:
- Left Shift Rule (Row-wise): For each row, keep the first element fixed. Move all other 
  non-zero elements immediately to the right of the first element, preserving 
  their relative order. Fill the remaining positions in the row with zeros.
- Right Shift Rule (Row-wise): For each row, keep the last element fixed. Move all other 
  non-zero elements immediately to the left of the last element, preserving 
  their relative order. Fill the remaining positions at the beginning of the 
  row with zeros.
- Gravity Rule (Column-wise): For each column, move all non-zero elements downwards 
  to occupy the lowest possible rows within that column, preserving their relative 
  vertical order. Fill the positions above them in the column with zeros.
"""

# --- Helper Functions ---

def _is_column_constant_non_zero(grid: List[List[int]], col_index: int) -> bool:
    """Checks if a specific column is constant and the constant value is non-zero."""
    # Handle empty grid list
    if not grid: return False 
    num_rows = len(grid)
    if num_rows == 0: return False
    
    # Check if grid has rows with elements (assume rectangular based on ARC)
    if not grid[0]: return False 
             
    num_cols = len(grid[0])
    # Handle negative index like -1 for last column
    if col_index < 0:
        col_index = num_cols + col_index 
        
    # Check if column index is valid
    if not (0 <= col_index < num_cols): return False 

    # Check if all rows have sufficient length and are rectangular
    if not all(len(row) == num_cols for row in grid):
         # Grid is not rectangular, cannot reliably check column constancy
         return False 

    # Get the value from the first row for comparison
    first_val = grid[0][col_index]
    # The constant value must be non-zero
    if first_val == 0: return False 

    # Check consistency across all other rows
    for i in range(1, num_rows):
        if grid[i][col_index] != first_val:
            return False # Value is not constant

    # If all checks pass, the column is constant and non-zero
    return True

def _apply_left_shift(grid: List[List[int]]) -> List[List[int]]:
    """Applies the Left Shift Rule (Type 1) to each row."""
    output_grid = []
    # Process each row independently
    for input_row in grid:
        # Handle potentially empty rows within the grid if necessary
        if not input_row:
            output_grid.append([])
            continue
        
        original_length = len(input_row)
        # a. Store the first element (fixed element).
        first_element = input_row[0]
        
        # b. Create a list of all non-zero elements from the second position onwards.
        non_zeros_after_first = [
            element for element in input_row[1:] if element != 0
        ]
        
        # c. Construct the output row starting with the fixed element.
        new_row = [first_element]
        
        # d. Append the list of non-zero elements.
        new_row.extend(non_zeros_after_first)
        
        # e. Append zeros until the length matches the original input row length.
        padding_zeros_count = original_length - len(new_row)
        new_row.extend([0] * padding_zeros_count)
        
        # f. Add the transformed row to the output grid.
        output_grid.append(new_row)
    return output_grid

def _apply_right_shift(grid: List[List[int]]) -> List[List[int]]:
    """Applies the Right Shift Rule (Type 3) to each row."""
    output_grid = []
    # Process each row independently
    for input_row in grid:
        # Handle potentially empty rows
        if not input_row:
            output_grid.append([])
            continue

        original_length = len(input_row)
        if original_length == 0:
             output_grid.append([])
             continue
             
        # a. Store the last element (fixed element).
        last_element = input_row[-1]
        
        # b. Create a list of all non-zero elements before the last element.
        non_zeros_before_last = [
            element for element in input_row[:-1] if element != 0
        ]
        
        # c. Calculate the number of zeros needed for padding at the beginning.
        num_non_zeros = len(non_zeros_before_last)
        # -1 accounts for the fixed last element
        padding_zeros_count = original_length - 1 - num_non_zeros 
        
        # d. Construct the output row starting with padding zeros.
        new_row = [0] * padding_zeros_count
        
        # e. Append the list of non-zero elements.
        new_row.extend(non_zeros_before_last)
        
        # f. Append the fixed (last) element.
        new_row.append(last_element)
        
        # g. Add the transformed row to the output grid.
        output_grid.append(new_row)
    return output_grid

def _apply_gravity(grid: List[List[int]]) -> List[List[int]]:
    """Applies the Gravity Rule (Type 2) using NumPy for column manipulation."""
    # Handle empty grid case
    if not grid or not grid[0]:
        return [] 

    try:
        # Convert to NumPy array for easier column slicing
        input_np = np.array(grid, dtype=int)
    except ValueError:
         # Handle non-rectangular grids - this rule expects rectangular structure
         # Raising an error might be appropriate, or returning the input unchanged.
         # Based on ARC task format, assume rectangularity or raise error.
         raise ValueError("Input grid must be rectangular for Gravity rule.")

    num_rows, num_cols = input_np.shape
    # a. Create an output grid initialized with zeros.
    output_np = np.zeros_like(input_np) 

    # b. Process each column.
    for j in range(num_cols):
        # c. Extract non-zero elements from the current input column.
        column_data = input_np[:, j]
        non_zeros = column_data[column_data != 0]
        
        # d. Determine the number of non-zero elements.
        num_non_zeros = len(non_zeros)
        
        # e. Place non-zeros at the bottom of the corresponding output column.
        if num_non_zeros > 0:
            start_row_index = num_rows - num_non_zeros
            output_np[start_row_index:, j] = non_zeros
            
    # Convert back to list of lists for the standard ARC format
    return output_np.tolist()

# --- Main Transform Function ---

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the appropriate transformation rule (Left Shift, Right Shift, or Gravity)
    to the input grid based on the properties of its first and last columns.
    """
    
    # Handle edge case of completely empty input list
    if not input_grid:
        return []
        
    # 1. Analyze Input Grid: Check first and last columns for constancy and non-zero value
    is_first_col_const_nz = _is_column_constant_non_zero(input_grid, 0)
    is_last_col_const_nz = _is_column_constant_non_zero(input_grid, -1)
    
    # 2. Select Transformation Rule & 3. Execute Selected Rule
    if is_first_col_const_nz:
        # Apply Left Shift Rule (Type 1)
        # This rule applies if the first column is constant and non-zero.
        output_grid = _apply_left_shift(input_grid)
    elif is_last_col_const_nz:
        # Apply Right Shift Rule (Type 3)
        # This rule applies if the first column condition is false, 
        # AND the last column is constant and non-zero.
        output_grid = _apply_right_shift(input_grid)
    else:
        # Apply Gravity Rule (Type 2)
        # This is the default rule if neither the first nor the last column 
        # meets the specific conditions for Type 1 or Type 3 rules.
        output_grid = _apply_gravity(input_grid)
        
    # 4. Return Output Grid
    return output_grid

```