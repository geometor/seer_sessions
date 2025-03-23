```python
"""
1.  **Identify Non-zero Pixels:** Examine the input grid and identify all pixels with values other than 0.
2.  **Extract and Count:** Extract these non-zero pixels, and count the number of times each unique, non-zero value appears.
3. **Construct Output:** Construct a new output grid from this collection. Its length equals to total count of non-zero pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting all non-zero values and creating a new grid.
    """
    # Extract non-zero values
    non_zero_values = []
    for row in input_grid:
        for cell in row:
            if cell != 0:
                non_zero_values.append(cell)

    # if there is no non-zero value return empty grid
    if len(non_zero_values)==0:
        return []

    # Create the output grid
    output_grid = np.array(non_zero_values)

    return output_grid
```