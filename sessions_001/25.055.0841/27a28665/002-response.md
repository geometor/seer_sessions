# 27a28665 • 002 • example_1 • investigate_coder

---
```python
"""
Counts the number of gray (5) pixels in the input grid.
Output the color blue if count of Gray pixel is greater than the count of white pixels.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((1, 1), dtype=int)

    # Count gray pixels
    gray_count = np.sum(input_grid == 5)
    
    # Count white pixels
    white_count = np.sum(input_grid == 0)

    # change output pixels 
    if gray_count > white_count:
        output_grid[0, 0] = 1

    return output_grid
```
