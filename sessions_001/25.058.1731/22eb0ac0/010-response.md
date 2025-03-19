# 22eb0ac0 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Target Rows:** Examine each row in the input grid.
2.  **Check Border Condition:** Determine if a row contains non-zero values *only* at its leftmost and rightmost positions.
3.  **Fill Row:** If the border condition is met, replace all '0' (white) pixels in that row with the value found in the border pixels. All the numbers in the borders are the same in each horizontal line.
4. **Preserve other numbers**: the pixels that are not on a horizontal line at the edges are not modified.
5. **Other Rows:** Rows that don't meet the border criteria remain unchanged and all other pixels maintain the values as it is.
"""

import numpy as np

def check_border_condition(row):
    """Checks if a row has non-zero values only at its borders."""
    if row[0] == 0 or row[-1] == 0:
        return False
    for i in range(1, len(row) - 1):
        if row[i] != 0:
            return False
    return True

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input
    rows, cols = input_grid.shape

    for i in range(rows):
      # identify rows with border conditions
      if check_border_condition(input_grid[i]):
        # fill those rows
        output_grid[i,:] = input_grid[i,0]
    return output_grid
```
