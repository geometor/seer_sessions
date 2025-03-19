# 995c5fa3 • 026 • refine_coder

---
```python
"""
1.  **Determine Output Grid Size:** The output grid's dimensions are based on the input grid's dimensions. The output dimensions are calculated as `2 * input_dimension + 1`.

2.  **Create Output Grid:** Create an output grid of the size calculated.

3.  **Fill the top row with red (color 2).**

4. **Fill all rows except the top and bottom rows with yellow (color 4).**

5.  **Fill the bottom row with red (color 2).**
"""

import numpy as np

def transform(input_grid):
    # Determine output grid size based on input grid dimensions.
    input_rows, input_cols = input_grid.shape
    output_rows = 2 * input_rows + 1
    output_cols = 2 * input_cols + 1

    # Create output grid of the calculated size.
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Fill the top row with red (color 2).
    output_grid[0, :] = 2

    # Fill all rows except the top and bottom rows with yellow (color 4).
    for i in range(1, output_rows - 1):
        output_grid[i, :] = 4

    # Fill the bottom row with red (color 2).
    output_grid[-1, :] = 2

    return output_grid
```
