```python
"""
1.  **Locate the Vertical Line:** Find the column index of the vertical line composed entirely of blue pixels (value 1) within the input grid.
2.  **Define Output Slice:** Determine the boundaries of a three-column slice within the input grid. This slice includes the column containing the blue line, one column to its immediate left, and one column to its immediate right.
3. **Create output**: Create output grid of same height as the input, and width of 3.
4.  **Extract and Transform Slice:** Extract the defined three-column slice from the input grid.
5.  **Color Substitution:** Within the extracted slice, replace all occurrences of maroon (value 9) with azure (value 8). All other values in the slice are replaced with white (value 0).
6. **Copy to output:** Populate the ouput grid with the values.
"""

import numpy as np

def find_vertical_line(grid, value):
    # Find the column index of the vertical line with the specified value.
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] != value:
                break
        else:
            return j
    return -1  # Return -1 if no such line is found.

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the column index of the vertical line of '1's.
    line_col = find_vertical_line(input_grid, 1)

    # Handle the case where no vertical line of '1's is found.
    if line_col == -1:
        return input_grid # Or some other default behavior

    # Determine the slice boundaries.
    rows, cols = input_grid.shape
    start_col = max(0, line_col - 1)
    end_col = min(cols, line_col + 2)
    
    # Initialize the output grid with zeros and correct dimensions.
    output_grid = np.zeros((rows, 3), dtype=int)
    
    # Extract the relevant slice from the input grid.
    input_slice = input_grid[:, start_col:end_col]

    # Apply color substitution: 9 -> 8, others -> 0
    transformed_slice = np.where(input_slice == 9, 8, 0)

    # Copy the transformed slice to the output grid.
    output_grid[:, :transformed_slice.shape[1]] = transformed_slice


    return output_grid
```