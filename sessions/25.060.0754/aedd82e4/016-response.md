# aedd82e4 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation involves changing a single pixel's color from red (2) to blue (1). The pixel to be changed is located at the grid coordinates (2, 3) - which is the third row and fourth column, if we 0-index (which means we start counting rows and columns from zero not one) . All other pixels in the grid remain unchanged. The input is scanned, the pixel located at (2,3) is selected. It is changed to blue and the modified grid returned as output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # change the pixel at (2, 3) to blue (1)
    output_grid[2, 3] = 1

    return output_grid
```
