# 99b1bc43 • 008 • example_2 • investigate_coder

---
```python
"""
The input grid is partitioned into two sections: a top section (rows 0-3) and a bottom section (rows 4-8).
The program compares corresponding cells (vertical aligned) in these two sections. If the colors of corresponding
cells are different, the corresponding cell in the output grid is colored green (3). If the colors are the same,
the corresponding cell in the output grid is colored white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid. The output dimensions are given as 4x4 in examples
    output_grid = np.zeros((4, 4), dtype=int)

    # Partition the input grid
    top_section = input_grid[:4]
    bottom_section = input_grid[4:]
    # Compare corresponding cells and update output_grid
    for i in range(4):
        for j in range(4):
            #The bottom section start with an offset of 1 row.
            if bottom_section.shape[0] > i : #make sure the offset is valid.
               if top_section[i, j] != bottom_section[i, j]:
                output_grid[i, j] = 3
               else:
                output_grid[i, j] = 0
            

    return output_grid
```
