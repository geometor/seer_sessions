```python
"""
The transformation doubles the width of the input grid. Each row is processed independently. 
Orange pixels (7) are duplicated. White pixels (0) are expanded to fill the remaining space.
If a 7 is present in the input row, it is also added at the mirrored position from the end of the expanded output row.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with twice the width of the input grid
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros((input_rows, input_cols * 2), dtype=int)

    # Iterate through each row of the input grid
    for row_index, row in enumerate(input_grid):
        # build output row and use it to fill output_grid
        output_row = []

        # Iterate through original input
        for i in range(len(row)):
            if row[i] == 7:
                output_row.append(7)
            else:
                output_row.append(0)

        # insert original white and oranges
        output_grid[row_index, :len(output_row)] = output_row

        # Add mirrored 7s
        for i in range(len(row)):
          if row[i] == 7:
            output_grid[row_index, output_grid.shape[1] - 1 - i] = 7


    return output_grid
```