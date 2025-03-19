# fafffa47 • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify** all pixels with the color maroon (9) in the input grid.
2.  **Replace** the color of these identified pixels with red (2).
3. **Remove** all blue pixels and some white pixels to get a compressed 3x3 grid. There are two maroon colored objects on the top left. The transformation seems to be taking the 3x3 area of the grid that starts on the top left and contains those two original maroon colored objects, and substituting the color of those objects.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a 3x3 numpy array filled with zeros (white)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the top-left 3x3 region of the input grid
    for i in range(3):
        for j in range(3):
            # Check if the current pixel is maroon (9)
            if input_grid[i, j] == 9:
                # Replace maroon (9) with red (2) in the output grid
                output_grid[i, j] = 2
            else:
                output_grid[i,j] = input_grid[i,j]

    return output_grid
```
