# d631b094 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Count:** Count the number of cells with the value '1' (blue cells) in the input grid.
2.  **Create Output Grid:** Create a new grid. The dimensions will be 1 x N, where N is the count obtained in step 1.
3.  **Fill:** Fill all the cells of the new grid with the value '1' (make them blue).
"""

import numpy as np

def transform(input_grid):
    # Count the number of cells with value '1' in the input grid.
    count_of_ones = np.count_nonzero(input_grid == 1)

    # Create a new grid with dimensions 1 x N, where N is the count of ones.
    output_grid = np.ones((1, count_of_ones), dtype=int)

    # The output grid is already filled with '1's due to np.ones().

    return output_grid
```
