# beb8660c • 012 • refine_coder

---
```python
"""
The transformation involves rearranging rows based on whether they contain objects or not. Empty rows at the top of the input grid are preserved. Rows containing objects (non-background pixels) are moved below the empty rows, maintaining their original relative order.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the row rearrangement rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Empty Rows and Object Rows
    empty_rows = []
    object_rows = []
    for i, row in enumerate(input_grid):
        if np.all(row == 0):  # Check if the row is all background color
            empty_rows.append(i)
        else:
            object_rows.append(i)

    # 2. Preserve Top Empty Rows
    top_empty_count = 0
    for i in empty_rows:
        if i == top_empty_count:
          top_empty_count += 1
        else:
          break;

    # 3. Reorder Object Rows (preserving relative order)
    new_row_index = top_empty_count
    for row_index in object_rows:
        output_grid[new_row_index] = input_grid[row_index]
        new_row_index += 1

    return output_grid.tolist()
```

