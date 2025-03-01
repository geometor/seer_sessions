# 834ec97d • 014 • refine_coder

---
```python
"""
1.  **Identify Rows for Transformation:** Examine the input grid. If a row contains *only* white pixels (0) or white pixels and *at least one* magenta pixel(6), and it is *not* a row with *only* a single magenta pixel(6), transform those white pixels into yellow (4) pixels.
2. If a row has only one magenta pixel and no other colors, it should remain untouched.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    for r in range(rows):
        row = input_grid[r, :]
        unique_colors = np.unique(row)
        
        # Check conditions for transformation:
        if (np.all(unique_colors == 0) or  # All white pixels
            (0 in unique_colors and 6 in unique_colors and len(unique_colors) > (1 if 6 in unique_colors else 0) )): # and at least one magenta, plus other color
            
            
            #transform white pixels into yellow
            for c in range(cols):
                if output_grid[r,c] == 0:
                     output_grid[r,c] = 4

        elif (len(unique_colors) == 1 and 6 in unique_colors): #only one magenta
            #Do nothing - keep the original row
            pass




    return output_grid
```
