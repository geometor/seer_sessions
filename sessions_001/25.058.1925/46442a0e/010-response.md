# 46442a0e • 010 • example_2 • investigate_coder

---
```python
"""
1. Double the size of the input grid in both width and height (3x3 -> 6x6).
2. The original input grid's pattern is mirrored horizontally and vertically.
    - Duplicate each cell value to be 2x2
    - Horizontally mirror the 2x2 duplicated grid.
    - Vertically mirror the result and concatenate.
"""

import numpy as np

def transform(input_grid):
    # Create a numpy array from the input grid
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_array.shape

    # 1. Duplicate each cell to create a 2x2 block.
    duplicated_array = np.repeat(np.repeat(input_array, 2, axis=0), 2, axis=1)
    
    # 2. Mirror horizontally.
    mirrored_horizontal = np.fliplr(duplicated_array)
    
    # 3. Concatenate the original duplicated array with its horizontal mirror
    intermediate_result = np.hstack((duplicated_array[:,:cols*2], mirrored_horizontal[:,:cols*2]))

    # 4. Mirror vertically.
    mirrored_vertical = np.flipud(intermediate_result)

    # 5. Concatenate the intermediate result with its vertical mirror.
    output_array = np.vstack((intermediate_result, mirrored_vertical))


    return output_array.tolist()
```
