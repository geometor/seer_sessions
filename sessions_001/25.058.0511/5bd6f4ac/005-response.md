# 5bd6f4ac • 005 • refine_coder

---
```python
"""
1.  **Locate Start:** Find the row and column indices of the first non-white pixel (value not equal to 0) in the input grid. This is the "top-left" coordinate.
2.  **Extract Subgrid:** Extract a 3x3 subgrid from the input grid. The top-left corner of this subgrid is the coordinate found in step 1.
3. **Boundary Check:** if the top-left corrdinate is within 3 rows or 3 columns of any edge, pad with zeros to ensure that the output is 3 x 3.
4.  **Return:** The resulting 3x3 subgrid is the output.
"""

import numpy as np

def find_top_left(input_grid):
    # Iterate through rows and columns
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # Check for non-white pixel
            if input_grid[r, c] != 0:
                return (r, c)
    return None  # Return None if no such pixel is found

def transform(input_grid):
    # Find the top-left corner of the subgrid
    top_left = find_top_left(input_grid)

    # If no non-white pixel is found, return an empty grid
    if top_left is None:
        return np.zeros((3, 3), dtype=int)

    row, col = top_left

    # Extract the 3x3 subgrid
    # Handle boundary conditions: ensure we don't go out of bounds
    rows, cols = input_grid.shape
    end_row = min(row + 3, rows)
    end_col = min(col + 3, cols)
    
    output_grid = input_grid[row:end_row, col:end_col]

    # Pad with zeros if subgrid is less than 3x3
    if output_grid.shape != (3,3):
      temp_grid = np.zeros((3,3),dtype=int)
      temp_grid[:output_grid.shape[0],:output_grid.shape[1]] = output_grid
      output_grid = temp_grid
    
    return output_grid
```
