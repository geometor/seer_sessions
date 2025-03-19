# 2204b7a8 • 014 • refine_coder

---
```python
"""
The transformation rule is:  All instances of the most common color across the
entire input grid are changed to yellow (4).
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # Find the most common color in the input grid
    color_counts = Counter()
    for i in range(rows):
        for j in range(cols):
            color_counts[output_grid[i, j]] += 1

    most_common_color = color_counts.most_common(1)[0][0]

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            if output_grid[i,j] == most_common_color:
                output_grid[i,j] = 4

    return output_grid
```
