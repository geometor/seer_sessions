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
    if not grid: return False # Handle empty grid list
    num_rows = len(grid)
    if num_rows == 0: return False
    
    # Check if grid has rows with elements
    if not grid[0]: 
         # If first row is empty, assume grid is invalid for this check
         # (ARC grids are typically rectangular)
         return False 
             
    num_cols = len(grid[0])
    if col_index < 0:
        col_index = num_cols + col_index # Handle negative index like -1
        
    if not (0 <= col_index < num_cols): return False # Invalid column index

    # Check if all rows have sufficient length before accessing the element
    if not all(len(row) > col_index for row in grid):
         return False # Rows aren't long enough for this column index

    first_val = grid[0][col_index]
    if first_val == 0: return False # Must be non-zero

    # Check consistency across all rows
    for i in range(1, num_rows):
        # Also check row length consistency here
        if len(grid[i]) != num_cols or grid[i][col_index] != first_val:
            return False # Value is not constant or grid is not rectangular

    return True

def _apply_left_shift(grid: List[List[int]]) -> List[List[int]]:
    """Applies the Left Shift Rule (Type 1) to each row."""
    output_grid = []
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
        padding_zeros_count = original_length - 1 - num_non_zeros # -1 for the fixed last element
        
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
         # Handle non-rectangular grids if necessary, maybe return original?
         # For now, assume valid rectangular input based on ARC examples.
         print("Warning: Input grid is not rectangular. Gravity rule might fail.")
         # As a fallback, could return grid or raise error. Let's return grid.
         # return grid # Option 1: Fallback
         raise ValueError("Input grid must be rectangular for Gravity rule.") # Option 2: Error


    num_rows, num_cols = input_np.shape
    # a. Create an output grid initialized with zeros.
    output_np = np.zeros_like(input_np) 

    # b. Process each column.
    for j in range(num_cols):
        # c. Extract non-zero elements from the current column.
        column_data = input_np[:, j]
        non_zeros = column_data[column_data != 0]
        
        # d. Determine the number of non-zero elements.
        num_non_zeros = len(non_zeros)
        
        # e. Place non-zeros at the bottom of the output column.
        if num_non_zeros > 0:
            output_np[num_rows - num_non_zeros:, j] = non_zeros
            
    # Convert back to list of lists for the final output format
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
        
    # 1. Analyze Input Grid: Check first and last columns
    is_first_col_const_nz = _is_column_constant_non_zero(input_grid, 0)
    is_last_col_const_nz = _is_column_constant_non_zero(input_grid, -1)
    
    # 2. Select Transformation Rule & 3. Execute Selected Rule
    if is_first_col_const_nz:
        # Apply Left Shift Rule (Type 1)
        output_grid = _apply_left_shift(input_grid)
    elif is_last_col_const_nz:
        # Apply Right Shift Rule (Type 3)
        output_grid = _apply_right_shift(input_grid)
    else:
        # Apply Gravity Rule (Type 2)
        output_grid = _apply_gravity(input_grid)
        
    # 4. Return Output Grid
    return output_grid