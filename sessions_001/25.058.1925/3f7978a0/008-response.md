# 3f7978a0 • 008 • refine_coder

---
```python
"""
The transformation rule identifies the smallest rectangular region (bounding box) that encompasses all non-zero pixels within the input grid. It then extracts this sub-grid, effectively removing any rows and columns composed entirely of zeros (whitespace) that surround the non-zero pixels. The extracted sub-grid preserves the original arrangement and values of all non-zero pixels, including any "internal" zeros that fall within the bounding box.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_array = np.array(input_grid)

    # Find rows and columns that contain at least one non-zero element
    non_zero_rows = np.any(input_array != 0, axis=1)
    non_zero_cols = np.any(input_array != 0, axis=0)

    # Extract the sub-grid based on the identified rows and columns.
    # The slicing extracts all rows where non_zero_rows is True,
    # and then from those rows, it extracts all columns where non_zero_cols is True.
    output_array = input_array[non_zero_rows][:, non_zero_cols]

    return output_array.tolist()
```

