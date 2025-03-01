# 46442a0e • 008 • example_2 • investigate_coder

---
```python
"""
Scale the input grid by a factor of 2 in both dimensions. Then create a 'cross' shape by mirroring
the scaled grid horizontally and vertically.
"""

import numpy as np

def transform(input_grid):
    # Scale the input grid
    scaled_grid = np.repeat(np.repeat(input_grid, 2, axis=0), 2, axis=1)
    
    # Create horizontal mirror
    horizontal_mirror = np.fliplr(scaled_grid)
    
    # Concatenate scaled grid and its horizontal mirror
    top_row = np.concatenate((scaled_grid, horizontal_mirror), axis=1)

    # Create vertical mirror
    vertical_mirror = np.flipud(scaled_grid)

    # Create bottom of cross using vertical mirror of top
    vertical_mirror_hm = np.fliplr(vertical_mirror)
    bottom_row = np.concatenate((vertical_mirror, vertical_mirror_hm), axis=1)

    # Concatenate top and bottom rows to create the final output
    output_grid = np.concatenate((top_row, bottom_row), axis=0)

    return output_grid
```
