```python
"""
The input grid is divided into two sections by a horizontal blue line. The output grid is 4x4 and
is constructed by interleaving the rows of the first four columns of the upper and lower sections.
"""

import numpy as np

def find_blue_line(grid):
    """Finds the row index of the horizontal blue line."""
    for i, row in enumerate(grid):
        if all(pixel == 1 for pixel in row):
            return i
    return -1

def transform(input_grid):
    input_grid = np.array(input_grid)
    blue_line_row = find_blue_line(input_grid)

    # Divide the input grid
    upper_section = input_grid[:blue_line_row, :4]  # First 4 cols above blue line
    lower_section = input_grid[blue_line_row + 1:, :4] # First 4 cols below

    # Initialize the output grid (4x4)
    output_grid = np.zeros((4, 4), dtype=int)

    # Interleave rows and construct output
    for i in range(4):
        if i < upper_section.shape[0]:
          output_grid[i] = upper_section[i]
        if i < lower_section.shape[0]:
          output_grid[i] = lower_section[i]

    # now do interleaving correctly by using a temp grid
    temp_grid = np.zeros((4, 4), dtype=int)
    upper_row = 0
    lower_row = 0
    for i in range(4): # rows
        if upper_row < upper_section.shape[0]:
          temp_grid[i] = upper_section[upper_row]
          upper_row += 1
          i+=1

        if lower_row < lower_section.shape[0] and i < 4: # still have rows
          temp_grid[i] = lower_section[lower_row]
          lower_row += 1

    return temp_grid.tolist()
```