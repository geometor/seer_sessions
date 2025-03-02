# 794b24be • 036 • refine_coder

---
```python
"""
1.  **Identify blue pixels:** Iterate through each pixel in the input grid and check if its color is blue (1).
2.  **Conditional Replacement (Row 0):** If a pixel is in the first row (row index 0) and its color is blue, change its color to red (2).
3. **Conditional Replacement (Other rows):** If a pixel is NOT in the first row and its color is blue, change its color to white/0.
4.  **Preserve white pixels:** All the white pixels remain unchanged.
5. The result of the transformation is the output grid
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is blue
            if output_grid[i, j] == 1:
                # Conditional replacement based on row index
                if i == 0:
                    output_grid[i, j] = 2  # Change to red
                else:
                    output_grid[i,j] = 0

    return output_grid
```

