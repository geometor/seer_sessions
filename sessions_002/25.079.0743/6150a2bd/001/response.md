```python
"""
The input grid is transposed. This means the rows of the input grid become the columns of the output grid, and vice-versa. 
Or put differently, the matrix is flipped over its main diagonal.
After swapping rows and columns perform the following value mappings:
    3 becomes 8.
    8 becomes 3
    5 becomes 5
    7 becomes 7
    1 becomes 1
    2 becomes 2
The numbers which become themselves do not matter as much as the ones that do not in trying to construct a mapping program.
"""

import numpy as np

def transform(input_grid):
    # Transpose the input grid using numpy
    transposed_grid = np.transpose(np.array(input_grid)).tolist()

    # Apply the value mapping
    output_grid = []
    for row in transposed_grid:
        new_row = []
        for val in row:
            if val == 3:
                new_row.append(8)
            elif val == 8:
                new_row.append(3)
            else:
                new_row.append(val)
        output_grid.append(new_row)
    
    return output_grid
```
