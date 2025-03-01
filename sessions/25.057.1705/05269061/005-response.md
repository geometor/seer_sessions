# 05269061 • 005 • refine_coder

---
```python
"""
The transformation rule involves creating an output grid with the same dimensions as the input grid and populating it with a repeating sequence of colors: 2 (red), 8 (azure), and 3 (green).  The sequence starts at the top-left corner and continues horizontally and vertically, wrapping as needed.
"""

import numpy as np

def transform(input_grid):
    # Obtain Input Dimensions
    height, width = input_grid.shape

    # Create Output Grid
    output_grid = np.zeros((height, width), dtype=int)

    # Populate with Pattern
    pattern = [2, 8, 3]
    pattern_length = len(pattern)
    pattern_index = 0

    for row in range(height):
        for col in range(width):
            output_grid[row, col] = pattern[pattern_index % pattern_length]
            pattern_index += 1

    return output_grid
```

