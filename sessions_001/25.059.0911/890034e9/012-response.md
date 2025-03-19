# 890034e9 • 012 • refine_coder

---
```python
"""
1.  **Identify Azure Pixels:** Locate all pixels with color 8 (azure) in the input grid.
2.  **Conditional Replacement:** For *every* azure pixel:
    *   Check for a pixel directly above.
    *   If a pixel exists directly above, replace the azure pixel with the color of the pixel above.
    *   If there's no pixel directly above, retain the original azure color (8).
3. No action for other colours.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            # Check if the current pixel is azure
            if input_grid[row, col] == 8:
                # Check if there's a pixel directly above
                if row > 0:
                    # Replace the azure pixel with the color of the pixel above
                    output_grid[row, col] = input_grid[row - 1, col]

    return output_grid
```
