# 1b2d62fb • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify the central blue column:** Locate the column in the input grid that contains only blue (value 1) pixels.
2.  **Determine output grid width:** The width of output grid would be number of columns in input grid having same colored pixels on either side of the central blue column, plus one for central column itself.
3.  **Construct output grid:** create a new grid that is the same height as the input grid, and calculated width in step 2.
4.   **Populate the output grid**: Fill all cells in the output grid with white (0). Replace the white at the locations in the output grid corresponding to blue column in the input grid with azure (8).

"""

import numpy as np

def find_blue_column(grid):
    # Find the column index where all elements are blue (1).
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 1):
            return j
    return -1

def calculate_output_width(grid, blue_column_index):
    # input grid width
    width = grid.shape[1]
    # blue column index
    col = blue_column_index
    # if column is on extreme right, output grid of 1 width
    if col == width - 1:
        return 1
    # counter for column
    count = 0
    # loop until either side of column is tested
    while col > 0 and col < width -1:
      #decrement left and increment right columns
      col -= 1
      #check the number of columns having similar pixel colors to its opposite side wrt blue column
      if np.array_equal(grid[:,col], grid[:,width - 1 - count]):
          count+= 1
      else:
          break    
    return count*2 + 1
    

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the central blue column
    blue_column_index = find_blue_column(input_grid)
    
    # Calculate output width
    output_width = calculate_output_width(input_grid, blue_column_index)
     

    # Initialize output grid with all white (0)
    output_grid = np.zeros((input_grid.shape[0], output_width), dtype=int)

    # Identify where the blue column would be mapped in the output grid, mark as azure
    
    output_grid[:, output_width//2] = 8

    return output_grid.tolist()
```
