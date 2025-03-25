```python
"""
1.  **Identify the Target Row:** Find the row in the input grid that contains non-zero digits.
2.  **Iterate through Non-Zero Digits:** For each non-zero digit in the target row:
    *   Determine Expansion Length: In the example provided, the expansion is 5. We need to verify it on more examples.
    *   Expand the Digit: Replicate current digit to left and to the right.
    *   Insert Separator: Place a '5' (grey) in between expanded non-zero objects.
3. **Maintain other rows:** Other rows values are kept the same.
"""

import numpy as np

def find_target_row(grid):
    # Iterate through rows and check for non-zero elements
    for i, row in enumerate(grid):
        if np.any(row != 0):
            return i
    return -1  # No target row found

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # find target row
    target_row_index = find_target_row(input_grid)

    if target_row_index == -1:
        return output_grid # nothing to do

    target_row = input_grid[target_row_index]
    
    #get non zero values and indices
    non_zero_indices = np.where(target_row != 0)[0]
    non_zero_values = target_row[non_zero_indices]

    # calculate expansion and insertion positions
    expansion_length = 5
    output_row = np.zeros(width, dtype=int)
    
    current_pos = 0
    for i, value in zip(non_zero_indices, non_zero_values):      
      # expand digits
      for j in range(expansion_length):
          if current_pos < width:
            output_row[current_pos] = value
            current_pos +=1

      # insert if not last digit
      if i < len(non_zero_indices) - 1 and current_pos < width:
          output_row[current_pos] = 5
          current_pos +=1

    # set row
    output_grid[target_row_index] = output_row

    return output_grid
```