# f2829549 • 008 • refine_coder

---
```python
"""
1.  **Locate:** Find the column in the input grid that contains all blue (1) pixels.
2.  **Extract:** Extract this column and the two columns immediately to its right. This forms a sub-grid.
3.  **Replace:** Within this sub-grid, replace all non-zero values with the value 3 (green).
4.  **Output:** The resulting sub-grid is the output.
"""

import numpy as np

def find_column_of_ones(grid):
    # Iterate through columns to find the one with all 1s
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 1):
            return j
    return -1  # Return -1 if no such column is found

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the column with all 1s
    ones_column_index = find_column_of_ones(input_grid)

    # Extract the relevant columns
    if ones_column_index != -1 and ones_column_index + 2 < input_grid.shape[1]:
        extracted_grid = input_grid[:, ones_column_index:ones_column_index + 3]
    else:
      # Handle the case where no column of all 1s is found, or there are not two columns after it
      # return the input unchanged for now, but we can experiment
      return input_grid.tolist()

    # Create a copy to modify for output
    output_grid = extracted_grid.copy()
    
    # replace non zero cells with 3
    output_grid[output_grid != 0] = 3
    

    return output_grid.tolist()
```
