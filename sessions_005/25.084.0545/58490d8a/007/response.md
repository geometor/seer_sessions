```python
"""
1.  **Grid Division:** Divide the input grid into non-overlapping 3x3 blocks.  Start from the top-left corner (0,0) and move in steps of 3 along rows and columns.
2.  **Output Grid:** Create an output grid with dimensions (input_rows // 3, input_cols // 3).
3.  **Mapping:** For each cell (i, j) in the output grid:
    *   The corresponding value is taken from the input grid at position (i*3 + 1, j*3 + 1). This effectively takes the *center* element of each 3x3 block in the input grid.
4.  **Populate Output:** Populate each cell in the output grid by applying the mapping in step 3.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Create output grid
    output_rows = rows // 3
    output_cols = cols // 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through the output grid and map from the input
    for i in range(output_rows):
        for j in range(output_cols):
            # Map output cell (i, j) to input cell (i*3 + 1, j*3 + 1)
            output_grid[i, j] = input_grid[i * 3 + 1, j * 3 + 1]

    return output_grid.tolist()
```
