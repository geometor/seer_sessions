# 25d8a9c8 • 008 • example_2 • investigate_coder

---
```python
"""
Input grid colors are transformed to either gray (5) or white (0) in the output grid based upon row location. The middle row of the output is all gray, and all the other rows are white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # change output pixels 
    # Middle Row Transformation
    output_grid[1, :] = 5
    
    #Other rows, all white, already initialized to 0.

    return output_grid
```
