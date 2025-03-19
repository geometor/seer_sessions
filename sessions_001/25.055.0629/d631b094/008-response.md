# d631b094 • 008 • example_2 • investigate_coder

---
```python
"""
Counts the number of red (2) pixels in the input grid and creates a 1xN output grid filled with red pixels, where N is the count of red pixels.
"""

import numpy as np

def transform(input_grid):
    # Count the number of red pixels (value 2) in the input grid.
    red_pixel_count = np.count_nonzero(input_grid == 2)

    # Create a new 1 x N grid, where N is the count of red pixels.
    output_grid = np.full((1, red_pixel_count), 2)

    return output_grid
```
