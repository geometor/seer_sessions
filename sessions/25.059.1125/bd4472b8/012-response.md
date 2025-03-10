# bd4472b8 • 012 • refine_coder

---
```python
"""
Finds a 3x1 object (three horizontally adjacent pixels of the same color) in the second row of the input.
Creates an output grid where the first row is all black, the second row is the identified 3x1 object,
and the remaining rows are pairs of rows, each pair filled with a color from the first row of the input,
in the order they appear.
"""

import numpy as np

def find_3x1_object(input_grid):
    # Find a 3x1 object in the second row
    input_grid = np.array(input_grid)
    for i in range(len(input_grid[1]) - 2):
        if input_grid[1, i] == input_grid[1, i+1] == input_grid[1, i+2]:
            return input_grid[1, i:i+3], i  # Return the object and its starting index
    return None, -1 # Object not found

def transform(input_grid):
    # Initialize output grid
    input_grid = np.array(input_grid)
    object_3x1, start_index = find_3x1_object(input_grid)
    output_height = 2 * len(input_grid[0]) + 2  # +2 for black row and the copied object row
    output_grid = np.zeros((output_height, len(input_grid[0])), dtype=int)


    # Create a black row at the top of output
    output_grid[0, :] = 0

    # Copy the 3x1 object to the second row of output
    if object_3x1 is not None:
      output_grid[1, start_index:start_index+3] = object_3x1

    # Create pairs of rows for each color in the first row of input
    row_index = 2
    for color in input_grid[0, :]:
        output_grid[row_index, :] = color
        row_index += 1
        output_grid[row_index, :] = color
        row_index += 1

    return output_grid.tolist()
```
