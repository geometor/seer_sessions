# 4522001f • 006 • refine_coder

---
```python
"""
1.  **Replacement:** Change all red (2) pixels in the input grid to green (3).
2.  **Expansion:** The output grid is 4 times the height and 4 times the width of the input grid and filled with black (0) pixels.
3. **Replication**: For each of the green pixels in the modified input grid, create a 4x4 block of green pixels in the output grid, where the top-left pixel of the 4x4 block corresponds to where the green pixel was located in the modified input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Replace red (2) with green (3)
    modified_input = np.where(input_grid == 2, 3, input_grid)

    # Initialize output grid with zeros, 4 times the size of the input
    output_grid = np.zeros((input_grid.shape[0] * 4, input_grid.shape[1] * 4), dtype=int)

    # Iterate through the modified input
    for i in range(modified_input.shape[0]):
        for j in range(modified_input.shape[1]):
            # If the pixel is green (originally red or already green)
            if modified_input[i, j] == 3:
                # Create a 4x4 block of green (3) in the output
                output_grid[i * 4 : i * 4 + 4, j * 4: j * 4 + 4] = 3

    return output_grid.tolist()
```

