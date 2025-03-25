```python
"""
Transforms an input grid by duplicating each cell horizontally and vertically,
and adding a border of zeros to the top and bottom of the entire grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed pattern.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # 1. Horizontal Duplication
    expanded_h = np.repeat(input_array, 2, axis=1)

    # 2. Vertical Duplication
    expanded_v = np.repeat(expanded_h, 2, axis=0)

    # 3. Add Border - top and bottom
    output_rows = rows * 2 + 1
    output_cols = cols * 2
    output_array = np.zeros((output_rows, output_cols), dtype=int)
    
    # Place the expanded_v array into the correct position within output_array
    output_array[1:rows*2 + 1, 0:cols*2] = expanded_v

    return output_array.tolist()
```
