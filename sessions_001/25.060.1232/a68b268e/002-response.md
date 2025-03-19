# a68b268e • 002 • example_6 • investigate_coder

---
```python
"""
1. **Identify the Dividing Line:** Locate the horizontal line of '1's (blue pixels) within the input grid.
2. **Focus on the Upper Section:** Consider only the section of the input grid *above* the horizontal line.
3.  **Extract Non-Zero and Non-One:** identify the non-zero and non-one color values in the section of the grid defined in step 2.
4. **Arrange Colors:** arrange into a new 4x4 grid, where:
    * the first column contains the rightmost non-zero, non-one element of each row, moving top to bottom, stopping after 4 elements.
    * the second, third, and fourth columns contain the first three unique non-zero, non-one element of each column, moving left to right, stopping after 4 elements.
"""

import numpy as np

def find_dividing_line(grid):
    # Find the row index where all elements are 1.
    for i, row in enumerate(grid):
        if all(pixel == 1 for pixel in row):
            return i
    return -1  # Return -1 if no such line is found

def extract_upper_section(grid, dividing_line_row):
    # Extract the portion of the grid above the dividing line.
    return grid[:dividing_line_row]

def extract_colors(upper_section):
    # find the non-zero and non-one elements per row
    rows = []
    for row in upper_section:
      elements = []
      for x in row:
        if x != 0 and x != 1:
          elements.append(x)
      rows.append(elements)

    # find first three unique non-zero, non-one element per columns
    cols = []
    transposed_section = upper_section.T
    for col in transposed_section:
      elements = []
      for x in col:
        if x != 0 and x != 1 and x not in elements:
          elements.append(x)
        if len(elements) == 3:
          break
      cols.append(elements)
    return rows, cols

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    grid = np.array(input_grid)

    # Find the row index of the dividing line (all 1s).
    dividing_line_row = find_dividing_line(grid)

    # Extract the section of the grid above the dividing line.
    upper_section = extract_upper_section(grid, dividing_line_row)

    # Extract non-zero, and non-one
    rows, cols = extract_colors(upper_section)

    # Initialize the output grid as a 4x4 array filled with zeros.
    output_grid = np.zeros((4, 4), dtype=int)

    # first column: rightmost non-zero, non-one
    col1 = []
    for r in rows:
      if len(r) > 0:
        col1.append(r[-1])

    # fill up to the size of output grid
    col1 = col1 + [0] * (4 - len(col1))
    output_grid[:, 0] = col1[:4]  # keep within bounds

    # Assign colors from cols.
    output_grid[0, 1:4] = cols[0][:3] if len(cols) > 0 else [0] * 3  # keep within bounds
    output_grid[1, 1:4] = cols[1][:3] if len(cols) > 1 else [0] * 3
    output_grid[2, 1:4] = cols[2][:3] if len(cols) > 2 else [0] * 3
    output_grid[3, 1:4] = cols[3][:3] if len(cols) > 3 else [0] * 3


    return output_grid.tolist()
```
