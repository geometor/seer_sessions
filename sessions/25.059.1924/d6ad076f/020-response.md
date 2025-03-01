# d6ad076f • 020 • refine_coder

---
```python
"""
1.  **Identify Colored Regions:** Locate the rectangular regions of green (3) at the top and maroon (9) at the bottom of the input grid. Note the all-white (0) rows between them.
2.  **Process Each White Row:** For each all-white row, perform the following:
    a. Determine the available white space. Iterate through the row and find contiguous white pixels.
    b. Calculate Azure Region Width and Position: The width of the azure (8) region appears to be consistently 4 pixels.
    c. Insert Azure Pixels. Locate the center of the white region, and place the azure block around it.

3.  **Preserve Colored Regions:** Keep the locations of the green and maroon regions unchanged. The right-most column is always 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by inserting an azure region into the white space between green and maroon regions.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all white rows
    all_white_rows = []
    for r in range(input_grid.shape[0]):
      if np.all(input_grid[r,:] == 0):
        all_white_rows.append(r)

    # Iterate through white rows
    for row_index in all_white_rows:
      row = input_grid[row_index]
      
      #get white space start and end, considering end of row
      start = 0
      while start < len(row) and row[start] != 0:
          start += 1
      end = start
      while end < len(row) and row[end] == 0:
          end += 1
      
      # Calculate Azure Region placement
      azure_width = 4
      center = (start + end) // 2
      azure_start = center - azure_width // 2
      azure_end = center + azure_width // 2

      #fill azure pixels into output
      for col_index in range(azure_start, azure_end):
          if 0 <= col_index < cols:  # Check bounds
              output_grid[row_index, col_index] = 8

    return output_grid
```
