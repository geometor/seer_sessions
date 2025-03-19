# 794b24be • 008 • refine_coder

---
```python
"""
1.  **Examine Input:** Check the input grid for the presence of *any* non-zero pixels.
2.  **Conditional Output:**
    *   **If non-zero pixels exist:** Create an output grid of the *same dimensions* as the input, filled entirely with white (0) pixels. Then, place a single red (2) pixel in the top-left corner (0, 0) of the output grid.
    *   **If NO non-zero pixels exist:** The output grid is *identical* to the input grid (all white/0). The shape and size are preserved.
3. **Output:** Return the modified or identical grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as all zeros with same dimensions as input_grid
    output_grid = np.zeros_like(input_grid)

    # check if any non-zero pixels exist in input_grid
    if np.any(input_grid):
        # set top-left pixel to red (2)
        output_grid[0, 0] = 2
    else:
        # output is identical to input (all zeros)
        output_grid = input_grid.copy()

    return output_grid
```

