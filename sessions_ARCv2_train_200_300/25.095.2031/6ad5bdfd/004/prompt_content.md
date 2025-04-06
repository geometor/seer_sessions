
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 0 0 3 3 0 0 4 4 0 0
2 0 0 0 0 5 0 0 0 0 0
2 0 0 0 0 5 0 0 6 6 0
2 0 0 0 0 0 0 8 0 0 0
2 0 7 7 0 0 0 8 0 0 0
```
Expected Output:
```
2 3 3 4 4 0 0 0 0 0 0
2 5 0 0 0 0 0 0 0 0 0
2 5 6 6 0 0 0 0 0 0 0
2 0 0 8 0 0 0 0 0 0 0
2 7 7 8 0 0 0 0 0 0 0
```
Transformed Output:
```
2 3 3 4 4 0 0 0 0 0 0
2 5 0 0 0 0 0 0 0 0 0
2 5 6 6 0 0 0 0 0 0 0
2 8 0 0 0 0 0 0 0 0 0
2 7 7 8 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 3.6363636363636402

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 0 0 4 0 8
3 0 0 4 0 6
1 1 5 5 8 6
2 2 2 2 2 2
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 3.3333333333333286

## Example 3:
Input:
```
0 4 4 0 0 0 0 0 0 2
0 0 0 5 5 0 0 6 0 2
0 0 0 0 0 0 0 6 0 2
0 9 0 0 8 8 0 0 0 2
0 9 0 0 0 0 0 0 0 2
```
Expected Output:
```
0 0 0 0 0 0 0 4 4 2
0 0 0 0 0 0 5 5 6 2
0 0 0 0 0 0 0 0 6 2
0 0 0 0 0 0 9 8 8 2
0 0 0 0 0 0 9 0 0 2
```
Transformed Output:
```
0 0 0 0 0 0 0 4 4 2
0 0 0 0 0 0 5 5 6 2
0 0 0 0 0 0 0 0 6 2
0 0 0 0 0 0 9 8 8 2
0 0 0 0 0 0 0 0 9 2
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 4.0
