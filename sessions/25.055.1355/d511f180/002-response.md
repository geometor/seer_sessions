# d511f180 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Target Pixels:** Find all pixels of color 8 (azure) in the input grid.

2.  **Invert and Swap:**
    *   Change any identified color 8 (azure) pixels to color 5 (gray).
    *   Change any color 5 (gray) pixels to color 8 (azure)

3. **Selective Swap.**
    *   Change any identified color 6 (magenta) pixel to color 8 (azure) if its immediate left neighbor is color 5 (gray).

4.  **Preserve Other Colors:** All other pixels retain their original colors.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Change color 8 (azure) to 5 (gray)
            if input_grid[r, c] == 8:
                output_grid[r, c] = 5
            # Change color 5 (gray) to 8 (azure)
            elif input_grid[r, c] == 5:
                output_grid[r, c] = 8
            # Change color 6 (magenta) to 8 (azure) if left neighbor is 5 (gray)
            elif input_grid[r, c] == 6:
                if c > 0 and input_grid[r, c-1] == 5:
                    output_grid[r, c] = 8

    return output_grid
```

