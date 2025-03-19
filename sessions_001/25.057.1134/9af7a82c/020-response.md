# 9af7a82c • 020 • example_4 • investigate_coder

---
```python
"""
Transforms a 4x3 input grid into a 6x3 output grid. Each column in the input
is transformed independently. The transformation involves reordering and
adding zeros. 
- Input column is copied to the output.
- Two additional '0' values are appended to each column.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows + 2, cols), dtype=int)

    # Iterate through each column of the input grid
    for j in range(cols):
        # Extract the current column
        input_column = input_grid[:, j]

        # Transform the column
        output_column = np.concatenate([input_column, [0, 0]])

        # Place the transformed column into the output grid
        output_grid[:, j] = output_column

    return output_grid.tolist()
```
