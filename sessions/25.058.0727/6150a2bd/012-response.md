# 6150a2bd • 012 • refine_coder

---
```python
"""
1.  **Rotate**: Rotate the entire input grid 90 degrees counter-clockwise.
2.  **Identify Source Column:** Find the right-most column in the *original* input grid that contains *any* non-zero values.
3.  **Transfer to Row**: The non-zero values from that identified column, are copied into the last row of the *rotated* output grid which contains any non-zero values. Empty cells in the row are skipped.
4.  **Fill Remaining with Zeroes:** All the remaining cells of the rotated output grid are 0.
"""

import numpy as np

def rotate_grid(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    return np.rot90(grid, k=1)

def find_rightmost_nonzero_column(grid):
    """Finds the index of the rightmost column with non-zero values."""
    grid = np.array(grid)
    for j in range(grid.shape[1] - 1, -1, -1):
        if np.any(grid[:, j] != 0):
            return j
    return -1  # Return -1 if no non-zero column is found

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    input_grid = np.array(input_grid) # convert to numpy array
    rotated_grid = rotate_grid(input_grid)  # Rotate the grid
    output_grid = np.zeros_like(rotated_grid) # initialize to all zeros

    # Find the rightmost non-zero column in the original grid
    source_column_index = find_rightmost_nonzero_column(input_grid)

    if source_column_index != -1:
        # Extract non-zero values from the source column
        source_column_values = [val for val in input_grid[:, source_column_index] if val != 0]

        # Find last non-zero row from the rotated grid
        target_row = -1
        for i in range(rotated_grid.shape[0] -1, -1, -1):
            if np.any(rotated_grid[i] != 0):
                target_row = i
                break;
        if target_row == -1:
          target_row = rotated_grid.shape[0] -1

        # Copy values to target_row of output, skipping empty cells
        k=0
        for j in range(output_grid.shape[1]):
          if k < len(source_column_values):
            output_grid[target_row, j] = source_column_values[k]
            k = k+1

    return output_grid.tolist() # return as list
```
