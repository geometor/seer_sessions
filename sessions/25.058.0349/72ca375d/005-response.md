# 72ca375d • 005 • refine_coder

---
```python
"""
1. Count: Count the number of magenta (6) pixels in the input grid.
2. Square Root: Calculate the integer square root of this count. This determines the dimensions of the output grid.
3. Create Output: Create a new square grid with dimensions equal to the calculated square root.
4. Fill: Fill all the pixels in the created grid with value 6 (magenta).
"""

import numpy as np
import math

def count_pixels(grid, color):
    # Count the number of pixels of a specific color in the grid.
    return np.sum(grid == color)

def transform(input_grid):
    # Count the number of magenta (6) pixels.
    magenta_count = count_pixels(input_grid, 6)

    # Calculate the integer square root.
    side_length = int(math.sqrt(magenta_count))

    # Create an output grid filled with magenta (6).
    output_grid = np.full((side_length, side_length), 6)

    return output_grid
```
