# 5daaa586 • 002 • example_3 • investigate_coder

---
```python
"""
1. **Identify the Vertical Line:** Locate the vertical line composed entirely of the color 3 (green) in the input grid.
2. **Segment Rows:** Divide the input grid into horizontal rows.
3. **Row Selection and Extraction:** For each row, determine if any horizontal line exist, and select the portion of the row on right of the green line (3).
4. **Rearrange selected rows:** Combine these rows from up to down to create the output grid.
"""

import numpy as np

def find_vertical_line(grid):
    """Finds the column index of the vertical line consisting of only 3s."""
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 3):
            return j
    return -1  # Return -1 if no such line is found

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)
    output_grid = []

    # Find the vertical green line
    green_line_col = find_vertical_line(input_grid)

    # Iterate through each row of the input grid
    for row in input_grid:
      # Check if all pixels in the row have the same value.
      if len(np.unique(row)) > 1 or (len(np.unique(row))== 1 and 0 not in row) :

        # If green vertical line exists, select segment to its right, if exist.
        if green_line_col != -1:
          new_row = row[green_line_col+1:]
          if new_row.size>0:
            output_grid.append(new_row)

    # convert the grid
    if (len(output_grid))==0:
      return []
    
    max_len = max(len(row) for row in output_grid)

    padded_output = []

    for row in output_grid:
      pad_width = max_len - len(row)
      padded_row = np.pad(row, (0,pad_width), 'constant', constant_values=(0))
      padded_output.append(padded_row)
      
    return np.array(padded_output)
```
