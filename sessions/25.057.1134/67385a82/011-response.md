# 67385a82 • 011 • refine_coder

---
```python
"""
1.  **Identify Contiguous Green Sequences:** Locate all sequences of horizontally adjacent green (3) pixels within the input grid. A sequence must have a minimum length of 2.
2.  **Replace with Azure:** Replace all pixels within each identified contiguous green sequence with azure (8) pixels.
3.  **Preserve other Pixels:** All other pixels that are not part of a contiguous green sequence remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing certain green pixels with azure pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is green (3)
            if input_grid[r, c] == 3:
                # Check for horizontal contiguity
                is_contiguous = False
                if c > 0 and input_grid[r, c - 1] == 3:
                    is_contiguous = True
                if c < cols - 1 and input_grid[r, c + 1] == 3:
                    is_contiguous = True

                # Replace with azure (8) if contiguous
                if is_contiguous:
                    output_grid[r, c] = 8

    return output_grid
```

