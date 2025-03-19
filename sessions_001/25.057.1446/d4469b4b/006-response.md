# d4469b4b • 006 • refine_coder

---
```python
"""
1.  **Output Dimensions:** The output grid's height and width are each 2 less than the input grid's dimensions.
2.  **Subgrid Iteration:** Consider every possible 2x2 subgrid within the input grid.
3.  **Condensation Rule:**
    *   For each 2x2 subgrid, examine its contents.
    *   If the subgrid contains the color red (pixel value 2), the corresponding pixel in the output grid is gray (pixel value 5).
    *   If the subgrid does *not* contain red, the corresponding output pixel is white/0.
4. **Output:** create the output grid and populate each pixel using the condensation rule.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by condensing 2x2 subgrids into single pixels.
    If a 2x2 subgrid contains red (2), the output pixel is gray (5).
    Otherwise, the output pixel is white (0).
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = rows - 2
    output_cols = cols - 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through all possible 2x2 subgrids
    for i in range(output_rows):
        for j in range(output_cols):
            # Extract the 2x2 subgrid
            subgrid = input_grid[i:i+2, j:j+2]

            # Apply the condensation rule
            if 2 in subgrid:
                output_grid[i, j] = 5  # Set to gray
            else:
                output_grid[i, j] = 0  # Set to white

    return output_grid.tolist()
```

