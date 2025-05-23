# 0520fde7 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Columns of Interest:** Examine the input grid and identify the columns that contain the value '1' (blue).
2.  **Extract Columns:** Create a new grid by extracting only the columns from step 1 in the input.
3.  **Map Colors:** In the new grid, transform the pixel values based on the following rules:
    *   '1' (blue) becomes '2' (red).
    *   '0' (white) remains '0' (white).
    *    '5'(gray) becomes '0'(white)
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid based on the observed rules.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # 1. Identify Columns of Interest (columns containing '1')
    columns_of_interest = []
    for j in range(cols):
        if 1 in input_array[:, j]:
            columns_of_interest.append(j)

    # 2. Extract Columns
    extracted_array = input_array[:, columns_of_interest]

    # 3. Map Colors
    output_array = np.zeros_like(extracted_array)
    for i in range(extracted_array.shape[0]):
        for j in range(extracted_array.shape[1]):
            if extracted_array[i, j] == 1:
                output_array[i, j] = 2  # Blue (1) to Red (2)
            elif extracted_array[i,j] == 5:
                output_array[i, j] = 0  # Gray(5) becomes white(0)
            # else, it remains 0 (white), which is the default initialization

    return output_array.tolist()
```
