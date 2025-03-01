# 0520fde7 • 012 • refine_coder

---
```python
"""
1.  **Identify Target Columns:** Examine each column in the input grid. If a column contains the value '1', '2' or '8', it is a target column.
2.  **Extract Target Columns:** Create a new grid composed of only the target columns, maintaining their original order.
3.  **Transform Colors:** Within the extracted columns perform these operations:
    *   If a pixel is '1', change it to '2'.
    *   If a pixel is '2', change it to '0'.
    *   If a pixel is '8', change it to '2'.
    *   If a pixel is '5', change it to '0'.
    *   Other colors remain the same.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid based on the observed rules.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # 1. Identify Target Columns (columns containing '1', '2', or '8')
    target_columns = []
    for j in range(cols):
        if 1 in input_array[:, j] or 2 in input_array[:, j] or 8 in input_array[:, j]:
            target_columns.append(j)

    # 2. Extract Target Columns
    extracted_array = input_array[:, target_columns]

    # 3. Transform Colors
    output_array = extracted_array.copy()  # Start with a copy to preserve other colors
    for i in range(output_array.shape[0]):
        for j in range(output_array.shape[1]):
            if output_array[i, j] == 1:
                output_array[i, j] = 2  # Blue (1) to Red (2)
            elif output_array[i, j] == 2:
                output_array[i, j] = 0  # Red (2) to White (0)
            elif output_array[i, j] == 8:
                output_array[i, j] = 2  # Azure (8) to Red (2)
            elif output_array[i,j] == 5:
                output_array[i,j] = 0   # Gray (5) to White (0)

    return output_array.tolist()
```
