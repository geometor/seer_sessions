# 67e8384a • 002 • example_1 • investigate_coder

---
```python
"""
The input grid is expanded by mirroring each row and then mirroring the resulting block of rows vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by mirroring rows and then mirroring the columns.
    """
    # Mirror Rows
    mirrored_rows = []
    for row in input_grid:
        mirrored_row = np.concatenate((row, row[::-1]))
        mirrored_rows.append(mirrored_row)
    mirrored_rows = np.array(mirrored_rows)

    # Mirror Columns
    output_grid = np.concatenate((mirrored_rows, mirrored_rows[::-1]), axis=0)

    return output_grid
```

