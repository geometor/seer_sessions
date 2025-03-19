# d631b094 • 002 • example_4 • investigate_coder

---
```python
"""
The output grid contains all non-zero digits from the input grid, repeated as many times as they appear.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = []

    # Find non-zero elements and their counts
    unique, counts = np.unique(input_grid, return_counts=True)
    counts_dict = dict(zip(unique, counts))
    
    # Create output grid
    for value, count in counts_dict.items():
        if value != 0:
            output_grid.extend([value] * count)

    return np.array(output_grid)
```
