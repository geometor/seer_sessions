# 77fdfe62 • 014 • refine_coder

---
```python
"""
1.  **Determine Input Grid Dimensions:** Find the number of rows (`rows`) and columns (`cols`) of the input grid.

2.  **Create Output Grid:** Create a 2x2 output grid.

3.  **Extract Corner Pixels:** Extract the four corner pixels from the input grid and place them into the corresponding positions in the output grid:

    *   **Top-Left:** The element at `input_grid[0][0]` is placed in `output_grid[0][0]`.
    *   **Top-Right:** The element at `input_grid[0][cols - 1]` is placed in `output_grid[0][1]`.
    *   **Bottom-Left:** The element at `input_grid[rows - 1][0]` is placed in `output_grid[1][0]`.
    *   **Bottom-Right:** The element at `input_grid[rows - 1][cols - 1]` is placed in `output_grid[1][1]`.

4. **Return the Output Grid.** Return the populated 2x2 output grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid by extracting the corner elements into a 2x2 output grid."""

    # Get input grid dimensions.
    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Initialize the output grid as a 2x2 numpy array.
    output_grid = np.zeros((2, 2), dtype=int)

    # Extract the corner values from the input grid.
    output_grid[0, 0] = input_grid[0][0]          # Top-left
    output_grid[0, 1] = input_grid[0][cols - 1]   # Top-right
    output_grid[1, 0] = input_grid[rows - 1][0]   # Bottom-left
    output_grid[1, 1] = input_grid[rows - 1][cols - 1] # Bottom-right

    return output_grid
```

