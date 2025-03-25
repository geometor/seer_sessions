```python
"""
1.  **Locate Vertical Blue Line:** Scan the input grid to find the column index of a vertical line consisting entirely of blue pixels (color code 1). If no such line is found. Return the original grid unchanged.
2.  **Define Slice Boundaries:** Calculate the start and end column indices for a three-column slice. The slice should include the column with the blue line, one column to its left, and one column to its right. Ensure the slice boundaries stay within the input grid's dimensions.
3.  **Initialize Output:** Create an output grid with the same height as the input grid and a fixed width of 3. Fill the output grid with white (0).
4.  **Extract Slice:** Extract the three-column slice from the input grid, using the calculated boundaries.
5.  **Color Substitution (in Slice):** Within the extracted *slice*,
    *   Replace all occurrences of maroon (9) with azure (8).
    *   Replace all other colors (excluding the maroon just transformed) with white (0).
6.  **Copy to Output:** Copy the *transformed* slice to the output grid, populating the grid from left to right.
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

    # Copy the transformed slice to the output grid, aligning to the right.
    slice_width = transformed_slice.shape[1]
    output_grid[:, :slice_width] = transformed_slice


    return output_grid
```