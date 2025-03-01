# 963e52fc • 008 • refine_coder

---
```python
"""
The width of the grid is doubled. Each row is processed independently. Rows containing only zeros (white) are extended. Rows with colored pixels have the contiguous non-zero colored block identified, replicated, and appended to the end of the original colored block.
"""

import numpy as np

def get_colored_block(row):
    # Helper to extract the start and end indices of the colored block in a row
    start = -1
    end = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start == -1:
                start = i
            end = i
    return start, end

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols * 2), dtype=int)

    # Iterate through each row
    for i, row in enumerate(input_grid):
        # check if it's a white row
        if np.all(row == 0):
            # extend white row
            output_grid[i, :cols] = row  # Corrected white row handling: Only copy, don't double
        else:
            # Process colored rows
            start, end = get_colored_block(row)
            colored_block = row[start:end+1]

            # Copy and append the colored block.
            output_grid[i, :end + 1] = row[:end+1] # original sequence up to end of colored block
            output_grid[i, end + 1:end + 1 + len(colored_block)] = colored_block # append replicated block


    return output_grid.tolist()
```
