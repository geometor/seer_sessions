# 8f2ea7aa • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify**: Find all azure (8) pixels in the input grid.
2.  **Mirror**: For each azure pixel at position (r, c), create a mirrored pixel at position (r, 9-1-c), i.e., by mirroring each column about a vertical line drawn through the very middle of the grid (column #4 for a grid with 9 columns)
3. **Shift Down and Right**: Move all the original and mirrored positions, down and right, one grid unit
4. **Wrap**: If an original element hits the bottom, top or right-most border when moved, wrap down and right one unit
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    input_np = np.array(input_grid)
    rows, cols = input_np.shape
    output_np = np.zeros_like(input_np)

    # 1. Identify azure pixels
    azure_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == 8:
                azure_pixels.append((r, c))

    # 2. Mirror and 3. Shift, and 4. Wrap
    for r, c in azure_pixels:
        # Mirror
        mirrored_c = cols - 1 - c
        
        # Shift and wrap original
        new_r = (r + 1) % rows
        new_c = (c + 1) % cols
        output_np[new_r, new_c] = 8

        # Shift and wrap mirrored
        new_mirrored_r = (r + 1) % rows
        new_mirrored_c = (mirrored_c + 1) % cols
        output_np[new_mirrored_r, new_mirrored_c] = 8

    return output_np.tolist()
```
