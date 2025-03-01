# bd4472b8 • 008 • refine_coder

---
```python
"""
1.  **Input:** A 2D grid of colors.
2.  **Determine Output Dimensions:** The output grid has the same number of columns as the input grid. The output grid's height is twice the number of replicated rows.
3.  **Iterate through Input Rows:** For each row in the input grid, check its index.
4.  **Select Rows:** Only rows with odd indices (0-indexed) are replicated.
5.  **Replicate Selected Rows:** Copy the selected rows from the input grid into the output grid. Repeat this copy a second time immediately below.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating rows with odd indices.
    """
    # Determine which rows to replicate (odd indices).
    rows_to_replicate = [i for i in range(input_grid.shape[0]) if i % 2 == 0]

    # Determine output dimensions.
    output_height = 2 * len(rows_to_replicate)
    output_width = input_grid.shape[1]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate selected rows.
    output_row_index = 0
    for row_index in rows_to_replicate:
        output_grid[output_row_index] = input_grid[row_index]
        output_grid[output_row_index + 1] = input_grid[row_index]
        output_row_index += 2

    return output_grid
```
